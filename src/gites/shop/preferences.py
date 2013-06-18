# -*- coding: utf-8 -*-
from zope.interface import Interface
from getpaid.core import interfaces as core_interfaces
from getpaid.core.options import FormSchemas
from Products.PloneGetPaid.member import ContactInfo
from gites.shop.interfaces import IBillingAddress, IShippingAddress
from gites.shop.member import GitesBillAddressInfo, GitesShipAddressInfo, GitesBillingInfo


class GitesFormSchemas(FormSchemas):

    interfaces = {
        'billing_address': IBillingAddress,
        'shipping_address': IShippingAddress,
        'contact_information': core_interfaces.IUserContactInformation,
        'payment': Interface}

    bags = {
        'billing_address': GitesBillAddressInfo,
        'shipping_address': GitesShipAddressInfo,
        'contact_information': ContactInfo,
        'payment': GitesBillingInfo}
