from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from getpaid.core import interfaces
from Products.PloneGetPaid.browser.cart import ShoppingCartActions
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.PloneGetPaid.i18n import _
from Products.PloneGetPaid.browser.cart import (CartFormatter,
                                                ShoppingCartListing,
                                                lineItemURL,
                                                formatLinkCell,
                                                lineItemPrice,
                                                lineItemTotal)
from zope.formlib import form
from Products.CMFPlone.i18nl10n import utranslate
from Products.CMFCore.utils import getToolByName

from zc.table import column


# override template
CartFormatter.renderExtra = ViewPageTemplateFile('templates/cart-listing-extras.pt')


class GDWShoppingCartActions(ShoppingCartActions):
    """
    """
    template = ZopeTwoPageTemplateFile('templates/cart-actions.pt')

    @form.action(_("Continue Shopping"), name='continue-shopping')
    def handle_continue_shopping(self, action, data):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        boutique = getattr(portal, 'shop')
        return self.request.RESPONSE.redirect(boutique.absolute_url())

    @form.action(_("Checkout"), condition="doesCartContainItems", name="Checkout")
    def handle_checkout(self, action, data):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        url = portal.absolute_url() + '/@@getpaid-checkout-wizard'
        return self.request.RESPONSE.redirect(url)


class GDWShoppingCartListing(ShoppingCartListing):
    """
    """
    template = ZopeTwoPageTemplateFile('templates/cart-listing.pt')

    columns = [
        column.SelectionColumn(lambda item: item.item_id, name="selection"),
        column.FieldEditColumn(_(u"Quantity"), 'edit', interfaces.ILineItem['quantity'], lambda item: item.item_id, name="Quantity"),
        column.GetterColumn(title=_(u"Name"), name="Name", getter=lineItemURL, cell_formatter=formatLinkCell),
        column.GetterColumn(title=_(u"Price"), name="Price", getter=lineItemPrice),
        column.GetterColumn(title=_(u"Total"), name="Total", getter=lineItemTotal),
       ]

    def update(self):
        for column in self.columns:
            if column.name == 'selection':
                continue
            if hasattr(column, 'title'):
                column.title = utranslate(domain='plonegetpaid',
                                          msgid=column.name,
                                          context=self.request)
        super(ShoppingCartListing, self).update()
