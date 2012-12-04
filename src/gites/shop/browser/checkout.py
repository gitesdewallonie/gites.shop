from Products.PloneGetPaid.browser.checkout import CheckoutAddress
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gites.shop import interfaces
from gites.shop.browser.payment import (ShippingAddress,
                                                BillingAddress,
                                                ContactInformation)
from getpaid.core.interfaces import (IUserContactInformation,
                                     IUserPaymentInformation,
                                     IOrderManager,
                                     IPaymentProcessor,
                                     IShoppingCartUtility)
from Products.PloneGetPaid.browser.widgets import CountrySelectionWidget, StateSelectionWidget
from Products.PloneGetPaid.browser.checkout import CheckoutReviewAndPay
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from zope.lifecycleevent import ObjectCreatedEvent

from zope.formlib import form
from AccessControl import getSecurityManager
from zope import component
from getpaid.core import options
from getpaid.core.order import Order
from cPickle import loads, dumps
from zope.event import notify
from Products.PloneGetPaid.i18n import _

##############################
# Some Property Bags - transient adapters

class MyBillingInfo( options.PropertyBag ):
    title = "Billing Information"

    def __init__(self, context):
        # need a context to be able to get the current available credit
        # cards.
        self.context = context

class MyShipAddressInfo( options.PropertyBag ):
    title = "Shipping Information"

class MyBillAddressInfo( options.PropertyBag ):
    title = "Payment Information"

class MyContactInfo( options.PropertyBag ):
    title = "Contact Information"

MyContactInfo.initclass( IUserContactInformation )
MyBillingInfo.initclass( IUserPaymentInformation )
MyShipAddressInfo.initclass( interfaces.IShippingAddress )
MyBillAddressInfo.initclass( interfaces.IBillingAddress )

class GDWCheckoutAddress(CheckoutAddress):
    template = ZopeTwoPageTemplateFile("templates/checkout-address.pt")

    form_fields = form.Fields( interfaces.IBillingAddress,
                               interfaces.IShippingAddress,
                               IUserContactInformation )
    form_fields['ship_country'].custom_widget = CountrySelectionWidget
    form_fields['bill_country'].custom_widget = CountrySelectionWidget
    form_fields['ship_state'].custom_widget = StateSelectionWidget
    form_fields['bill_state'].custom_widget = StateSelectionWidget

    actions = CheckoutAddress.actions.copy()

    def setupDataAdapters( self ):
        self.adapters = {}
        user = getSecurityManager().getUser()
        contact_info = component.queryAdapter( user, IUserContactInformation )
        if contact_info is None:
            contact_info = MyContactInfo()

        billing_address = component.queryAdapter(user,
                                                interfaces.IBillingAddress)
        if billing_address is None:
            billing_address = MyBillAddressInfo()

        shipping_address = component.queryAdapter(user,
                                                  interfaces.IShippingAddress)
        if shipping_address is None:
            shipping_address = MyShipAddressInfo()

        self.adapters[ IUserContactInformation ] = contact_info
        self.adapters[ interfaces.IShippingAddress ] = shipping_address
        self.adapters[ interfaces.IBillingAddress ] = billing_address
        return

class GDWCheckoutReviewAndPay(CheckoutReviewAndPay):
    form_fields = []

    passed_fields = form.Fields( interfaces.IBillingAddress ) + \
                    form.Fields( interfaces.IShippingAddress ) + \
                    form.Fields( IUserContactInformation )

    template = ZopeTwoPageTemplateFile("templates/checkout-review-pay.pt")

    actions = CheckoutReviewAndPay.actions.copy()

    def setupDataAdapters( self ):
        self.adapters = {}
        self.adapters[ IUserContactInformation ] = MyContactInfo()        
        self.adapters[ interfaces.IBillingAddress ] = MyBillAddressInfo()
        self.adapters[ interfaces.IShippingAddress ] = MyShipAddressInfo()
        self.adapters[ IUserPaymentInformation ] = MyBillingInfo(self.context)

        # extract data that was passed through in the request, using edit widgets
        # for marshalling value extraction. we'll basically throw an error here
        # if the values aren't found, but that shouldn't happen in normal operation
        data = {}
        widgets = form.setUpEditWidgets( self.passed_fields, self.prefix, self.context,
                                         self.request, adapters=self.adapters,
                                         ignore_request=False )
        form.getWidgetsData( widgets, self.prefix, data )
        # save the data to the adapters, we're not an edit form so we won't automatically
        # be storing to them, and we don't want to use the values as object attributes
        self.extractData( data )

    def setUpWidgets( self, ignore_request=False ):
        self.adapters = self.adapters is not None and self.adapters or {}

        # display widgets for bill/ship address
        self.widgets = form.setUpEditWidgets(
            self.passed_fields,  self.prefix, self.context, self.request,
            adapters=self.adapters, for_display=True, ignore_request=ignore_request
            )

    def createOrder( self ):
        order_manager = component.getUtility( IOrderManager )
        order = Order()

        shopping_cart = component.getUtility( IShoppingCartUtility ).get( self.context )

        # shopping cart is attached to the session, but we want to switch the storage to the persistent
        # zodb, we pickle to get a clean copy to store.

        order.shopping_cart = loads( dumps( shopping_cart ) )
        order.shipping_address = ShippingAddress.frominstance( self.adapters[ interfaces.IShippingAddress ] )
        order.billing_address = BillingAddress.frominstance( self.adapters[ interfaces.IBillingAddress ] )
        order.contact_information = ContactInformation.frominstance( self.adapters[ IUserContactInformation ] )

        order.order_id = self.getOrderId()
        order.user_id = getSecurityManager().getUser().getId()
        notify( ObjectCreatedEvent( order ) )
        return order

    @form.action(_(u"Make Payment"), name="make-payment")
    def makePayment( self, action, data ):
        """ create an order, and submit to the processor
        for async processors we never even got here.???
        """
        manage_options = IGetPaidManagementOptions( self.context )
        processor_name = manage_options.payment_processor
        if not processor_name:
            raise RuntimeError( "No Payment Processor Specified" )
        processor = component.getAdapter( self.context,
                                          IPaymentProcessor,
                                          processor_name )
        self.extractData( data )
        order = self.createOrder()
        order.processor_id = processor_name
        order.finance_workflow.fireTransition( "create" )

        # extract data to our adapters

        result = processor.authorize( order, None )

