from Products.Five.viewlet.manager import ViewletManager
import os
from Products.Five.browser import BrowserView
from gites.shop.interfaces import IGDWOrderDetailsManager

OrderDetailsManager = ViewletManager(
    "OrderDetails",
    IGDWOrderDetailsManager,
    os.path.join( os.path.dirname( __file__ ),
                  "templates",
                  "viewlet-manager.pt")
    )


class OrderDetails( BrowserView ):
    """ an order view
    """

    def __call__( self ):
        self.manager = OrderDetailsManager( self.context, self.request, self )
        self.manager.update()
        return super( OrderDetails, self).__call__()
 
