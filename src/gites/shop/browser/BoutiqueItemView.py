from Products.Five import BrowserView
from getpaid.core.interfaces import IBuyableContent
from zope.component import queryAdapter

class BoutiqueItemView(BrowserView):
    """
    Related methods for BoutiqueItem layout
    """

    def isPayable(self):
        """
        does the boutique item is payable ?
        """
        return queryAdapter(self.context, IBuyableContent) is not None

    def getPrice(self):
        """
        return the price
        """
        return IBuyableContent(self.context).price


