from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.PloneGetPaid.interfaces import IBuyableMarker
from getpaid.core.interfaces import IBuyableContent


class BoutiqueView(BrowserView):
    """
    Related methods for Shop layout
    """

    def getBoutiqueItems(self):
        """
        return the boutique items
        """
        cat = getToolByName(self.context, 'portal_catalog')
        results = cat.searchResults(portal_type='BoutiqueItem',
                                    review_state='published')
        boutiqueItems = []
        for brain in results:
            item = brain.getObject()
            if IBuyableMarker.providedBy(item):
                boutiqueItems.append(item)
        return boutiqueItems

    def getPrice(self, item):
        """ return the price of a buyable item """
        payable = IBuyableContent(item)
        return "%.2f" % payable.price
