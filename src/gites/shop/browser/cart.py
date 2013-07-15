from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from Products.PloneGetPaid.browser.cart import ShoppingCartActions
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.PloneGetPaid.i18n import _
from Products.PloneGetPaid.browser.cart import CartFormatter
from zope.formlib import form
from Products.CMFCore.utils import getToolByName


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
