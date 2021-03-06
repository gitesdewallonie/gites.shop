# -*- coding: utf-8 -*-
from zope.interface import Interface
from Products.PloneGetPaid.browser.checkout import BillingInfo
from Products.PloneGetPaid.member import BillAddressInfo, ShipAddressInfo, ContactInfo
from gites.shop.interfaces import IBillingAddress, IShippingAddress, IUserContactInformation


class GitesBillAddressInfo(BillAddressInfo):
    pass

GitesBillAddressInfo.initclass(IBillingAddress)


class GitesShipAddressInfo(ShipAddressInfo):
    pass

GitesShipAddressInfo.initclass(IShippingAddress)


class GitesBillingInfo(BillingInfo):
    pass

GitesBillingInfo = GitesBillingInfo.makeclass(Interface)


class GitesContactInfo(ContactInfo):
    pass

GitesContactInfo.initclass(IUserContactInformation)
