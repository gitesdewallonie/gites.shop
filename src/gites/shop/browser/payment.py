from gites.shop import interfaces
from zope import interface
from getpaid.core import options
from getpaid.core.interfaces import IUserContactInformation

class ShippingAddress( options.PersistentBag ):
    interface.implements( interfaces.IShippingAddress )
    schema = interfaces.IShippingAddress

class BillingAddress( options.PersistentBag ):
    interface.implements( interfaces.IBillingAddress )
    schema = interfaces.IBillingAddress

class ContactInformation( options.PersistentBag ):
    interface.implements( IUserContactInformation )
    schema = IUserContactInformation

