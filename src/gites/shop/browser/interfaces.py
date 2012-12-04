from zope.interface import Interface

class IBoutiqueView(Interface):
    """
    Related methods for Shop layout
    """

    def getBoutiqueItems():
        """
        return the boutique items
        """

    def getPrice(item):
        """ return the price of a buyable item """

class IBoutiqueItemView(Interface):
    """
    Related methods for BoutiqueItem layout
    """

    def isPayable(self):
        """
        does the boutique item is payable ?
        """

    def getPrice(self):
        """
        return the price
        """

