from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.i18nl10n import utranslate
from Products.PloneGetPaid.browser.checkout import CheckoutAddress
from Products.PloneGetPaid.interfaces import INamedOrderUtility
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gites.shop import interfaces
from getpaid.core.interfaces import (IUserPaymentInformation,
                                     IOrderManager,
                                     IPaymentProcessor,
                                     IShoppingCartUtility,
                                     IFormSchemas,
                                     keys)
from Products.PloneGetPaid.browser.widgets import CountrySelectionWidget
from Products.PloneGetPaid.browser.checkout import (CheckoutReviewAndPay,
                                                    OrderFormatter)
from Products.PloneGetPaid.browser.cart import formatLinkCell
from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
import Products.PloneGetPaid.browser.cart as cart_core

from zc.table import column
from zope.formlib import form
from AccessControl import getSecurityManager
from zope import component
from getpaid.core import options
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

MyContactInfo.initclass( interfaces.IUserContactInformation )
MyBillingInfo.initclass( IUserPaymentInformation )
MyShipAddressInfo.initclass( interfaces.IShippingAddress )
MyBillAddressInfo.initclass( interfaces.IBillingAddress )


class GDWCheckoutAddress(CheckoutAddress):
    template = ZopeTwoPageTemplateFile("templates/checkout-address.pt")

    form_fields = form.Fields( interfaces.IBillingAddress,
                               interfaces.IShippingAddress,
                               interfaces.IUserContactInformation )
    form_fields['ship_country'].custom_widget = CountrySelectionWidget
    form_fields['bill_country'].custom_widget = CountrySelectionWidget

    actions = CheckoutAddress.actions.copy()

    def setupDataAdapters( self ):
        self.adapters = {}
        user = getSecurityManager().getUser()
        contact_info = component.queryAdapter( user, interfaces.IUserContactInformation )
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
        self.adapters[ interfaces.IUserContactInformation ] = contact_info
        self.adapters[ interfaces.IShippingAddress ] = shipping_address
        self.adapters[ interfaces.IBillingAddress ] = billing_address
        return

class GDWCheckoutReviewAndPay(CheckoutReviewAndPay):
    template = ZopeTwoPageTemplateFile("templates/checkout-review-pay.pt")

    columns = [
        column.GetterColumn(name="Quantity", title=_(u"Quantity"), getter=cart_core.LineItemColumn("quantity")),
        column.GetterColumn(name="Name", title=_(u"Name"), getter=cart_core.lineItemURL, cell_formatter=formatLinkCell),
        column.GetterColumn(name="Price", title=_(u"Price"), getter=cart_core.lineItemPrice),
        column.GetterColumn(name="Total", title=_(u"Total"), getter=cart_core.lineItemTotal),
       ]

    def customise_widgets(self, fields):
        pass

    def renderCart(self):
        cart = component.getUtility(IShoppingCartUtility).get(self.context)
        if not cart:
            return _(u"N/A")

        for column in self.columns:
            if hasattr(column, 'title'):
                column.title = utranslate(domain='plonegetpaid',
                                          msgid=column.name,
                                          context=self.request)

        # create an order so that tax/shipping utilities have full order information
        # to determine costs (ie. billing/shipping address ).
        order = self.createTransientOrder()
        formatter = OrderFormatter( order,
                                    self.request,
                                    cart.values(),
                                    prefix=self.prefix,
                                    visible_column_names = [c.name for c in self.columns],
                                    #sort_on = ( ('name', False)
                                    columns = self.columns )

        formatter.cssClasses['table'] = 'listing'
        return formatter()

    @form.action(_(u"Make Payment"), name="make-payment")#, condition=form.haveInputWidgets )
    def makePayment( self, action, data ):
        """ create an order, and submit to the processor
        """
        siteroot = getToolByName(self.context, "portal_url").getPortalObject()
        manage_options = IGetPaidManagementOptions(siteroot)
        processor_name = manage_options.payment_processor

        if not processor_name:
            raise RuntimeError( "No Payment Processor Specified" )

        processor = component.getAdapter( siteroot,
                                          IPaymentProcessor,
                                          processor_name )

        adapters = self.wizard.data_manager.adapters

        order = self.createOrder()
        order.processor_id = processor_name
        order.finance_workflow.fireTransition( "create" )
        # extract data to our adapters

        formSchemas = component.getUtility(IFormSchemas)
        last4 = None
        if adapters[formSchemas.getInterface('payment')].credit_card:
            last4 = adapters[formSchemas.getInterface('payment')].credit_card[-4:]
        order.user_payment_info_last4 = last4
        order.name_on_card = adapters[formSchemas.getInterface('payment')].name_on_card
        order.bill_phone_number = adapters[formSchemas.getInterface('payment')].bill_phone_number
        result = processor.authorize( order, adapters[formSchemas.getInterface('payment')] )
        if result is keys.results_async:
            # shouldn't ever happen, on async processors we're already directed to the third party
            # site on the final checkout step, all interaction with an async processor are based on processor
            # adapter specific callback views.
            pass
        elif result is interfaces.keys.results_success:
            order_manager = component.getUtility( IOrderManager )
            order_manager.store( order )
            order.finance_workflow.fireTransition("authorize")
            template_key = 'order_template_entry_name'
            order_template_entry = self.wizard.data_manager.get(template_key)
            del self.wizard.data_manager[template_key]
            # if the user submits a name, it means he wants this order named
            if order_template_entry:
                uid = getSecurityManager().getUser().getId()
                if uid != 'Anonymous':
                    named_orders_list = component.getUtility(INamedOrderUtility).get(uid)
                    if order_template_entry not in named_orders_list:
                        named_orders_list[order.order_id] = order_template_entry
            # kill the cart after we create the order
            component.getUtility( IShoppingCartUtility ).destroy( self.context )
            self._next_url = self.getNextURL( order )
        else:
            order.finance_workflow.fireTransition('reviewing-declined')
            self.status = result
            self.form_reset = False
            self._next_url = self.getNextURL( order )

#    def setupDataAdapters( self ):
#        self.adapters = {}
#        self.adapters[ IUserContactInformation ] = MyContactInfo()
#        self.adapters[ interfaces.IBillingAddress ] = MyBillAddressInfo()
#        self.adapters[ interfaces.IShippingAddress ] = MyShipAddressInfo()
#        self.adapters[ IUserPaymentInformation ] = MyBillingInfo(self.context)
#
#        # extract data that was passed through in the request, using edit widgets
#        # for marshalling value extraction. we'll basically throw an error here
#        # if the values aren't found, but that shouldn't happen in normal operation
#        data = {}
#        widgets = form.setUpEditWidgets( self.passed_fields, self.prefix, self.context,
#                                         self.request, adapters=self.adapters,
#                                         ignore_request=False )
#        form.getWidgetsData( widgets, self.prefix, data )
#        # save the data to the adapters, we're not an edit form so we won't automatically
#        # be storing to them, and we don't want to use the values as object attributes
#        self.extractData( data )
#
#    def createOrder( self ):
#        order_manager = component.getUtility( IOrderManager )
#        order = Order()
#
#        shopping_cart = component.getUtility( IShoppingCartUtility ).get( self.context )
#
#        # shopping cart is attached to the session, but we want to switch the storage to the persistent
#        # zodb, we pickle to get a clean copy to store.
#
#        order.shopping_cart = loads( dumps( shopping_cart ) )
#        order.shipping_address = ShippingAddress.frominstance( self.adapters[ interfaces.IShippingAddress ] )
#        order.billing_address = BillingAddress.frominstance( self.adapters[ interfaces.IBillingAddress ] )
#        order.contact_information = ContactInformation.frominstance( self.adapters[ IUserContactInformation ] )
#
#        order.order_id = self.getOrderId()
#        order.user_id = getSecurityManager().getUser().getId()
#        notify( ObjectCreatedEvent( order ) )
#        return order
#
#    @form.action(_(u"Make Payment"), name="make-payment")
#    def makePayment( self, action, data ):
#        """ create an order, and submit to the processor
#        for async processors we never even got here.???
#        """
#        manage_options = IGetPaidManagementOptions( self.context )
#        processor_name = manage_options.payment_processor
#        if not processor_name:
#            raise RuntimeError( "No Payment Processor Specified" )
#        processor = component.getAdapter( self.context,
#                                          IPaymentProcessor,
#                                          processor_name )
#        self.extractData( data )
#        order = self.createOrder()
#        order.processor_id = processor_name
#        order.finance_workflow.fireTransition( "create" )
#
#        # extract data to our adapters
#
#        result = processor.authorize( order, None )

