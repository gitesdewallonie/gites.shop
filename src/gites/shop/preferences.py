# -*- coding: utf-8 -*-
from zope.interface import Interface
from getpaid.core.options import FormSchemas
from gites.shop.interfaces import IBillingAddress, IShippingAddress, IUserContactInformation
from gites.shop.member import GitesBillAddressInfo, GitesShipAddressInfo, GitesBillingInfo, GitesContactInfo


class GitesFormSchemas(FormSchemas):

    interfaces = {
        'billing_address': IBillingAddress,
        'shipping_address': IShippingAddress,
        'contact_information': IUserContactInformation,
        'payment': Interface}

    bags = {
        'billing_address': GitesBillAddressInfo,
        'shipping_address': GitesShipAddressInfo,
        'contact_information': GitesContactInfo,
        'payment': GitesBillingInfo}
