from Products.PloneGetPaid.browser.admin_order import (OrderSummaryComponent,
                                                       AdminOrderManagerBase,
                                                       AllItems,
                                                       renderItemId,
                                                       renderItemCost,
                                                       renderItemPrice,
                                                       AttrColumn)
from Products.Five.browser import BrowserView
import os
from Products.PloneGetPaid.i18n import _
from zc.table import column
from gites.shop.interfaces import IGDWAdminOrderManager
from Products.Five.viewlet import manager as viewlet_manager
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from zope import component
from Products.CMFCore.utils import getToolByName
from getpaid.core import interfaces

def renderItemCode( item, formatter ):
    plone = component.getSiteManager().context
    uid_cat = getToolByName(plone, 'uid_catalog')
    brains = uid_cat(UID=item.item_id)
    if brains:
        try:
            article = brains[0].getObject()
        except:
            return ''
        payableArticle = interfaces.IPayable(article, None)
        if payableArticle:
            return payableArticle.product_code
    return ''

def renderItemName( item, formatter ):
    content = item.resolve()
    if not content:
        return _(u"N/A")
    content_url = content.absolute_url()
    title = unicode(content.Title(), "utf-8")
    return u'<a href="%s">%s</a>'%( content_url, title )

class GDWAllItems( AllItems ):
    """
    """
    columns = [
        column.SelectionColumn( lambda item: item.item_id, name="selection"),
        column.GetterColumn( title=_(u"Item Id"), getter=renderItemId ),
        column.GetterColumn( title=_(u"Name"), getter=renderItemName ),
        column.GetterColumn( title=_(u"Item Code"), getter=renderItemCode ),
        column.GetterColumn( title=_(u"Price"), getter=renderItemCost ),        
        column.GetterColumn( title=_(u"Quantity"), getter=AttrColumn("quantity" ) ),
        column.GetterColumn( title=_(u"Total"), getter=renderItemPrice ),        
        column.GetterColumn( title=_(u"Status"), getter=AttrColumn("fulfillment_state" ) ),
        ]


class GDWOrderSummaryComponent( OrderSummaryComponent ):
    """ workflow actions and details on order summary
    """
    template = ZopeTwoPageTemplateFile('templates/order-summary.pt')

    def getContactInfos(self):
        infos = self.order.contact_information
        return {'email': infos.email,
                'phone_number': infos.phone_number}

    def getShippingAddress(self):
        infos = self.order.shipping_address
        return {'ship_first_line': infos.ship_first_line,
                'ship_second_line': infos.ship_second_line,
                'ship_city': infos.ship_city,
                'ship_country': self.vocab_countries.getTerm(infos.ship_country).title,
                'ship_state': self.vocab_states.getTerm(infos.ship_state).title,
                'ship_postal_code': infos.ship_postal_code}

    def getBillingAddress(self):
        infos = self.order.billing_address
        #if infos.ship_same_billing:
        #    return "Same as billing"
        return {'bill_first_line': infos.bill_first_line,
                'bill_second_line': infos.bill_second_line,
                'bill_city': infos.bill_city,
                'bill_country': self.vocab_countries.getTerm(infos.bill_country).title,
                'bill_state': self.vocab_states.getTerm(infos.bill_state).title,
                'bill_postal_code': infos.bill_postal_code,
                'vat_number': infos.vat_number}

AdminOrderManager = viewlet_manager.ViewletManager(
    "AdminOrder",
    IGDWAdminOrderManager,
    os.path.join( os.path.dirname( __file__ ),
                  "templates",
                  "viewlet-manager.pt"),
    bases=( AdminOrderManagerBase, )
    )

class AdminOrder( BrowserView ):
    """ an order view
    """

    def __init__( self, context, request ):
        self.context = context
        self.request = request

    def __call__( self ):
        self.manager = AdminOrderManager( self.context, self.request, self )
        self.manager.update()
        return super( AdminOrder, self).__call__()
