from zope import schema
from gites.locales import GitesMessageFactory as _
from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


class IGDWOrderDetailsManager(IViewletManager):
        """ viewlet manager for a single order
            """


class IGDWAdminOrderManager(IViewletManager):
        """ viewlet manager for a single order
            """


class IBillingAddress(Interface):
    """ where to bill
    """
    ship_same_billing = schema.Bool(title=_(u"Same as shipping address"),
                                    required=False)

    bill_first_line = schema.TextLine(title=_(u"First Line"))
    bill_second_line = schema.TextLine(title=_(u"Second Line"),
                                       required=False)
    bill_city = schema.TextLine(title=_(u"City"))
    bill_country = schema.Choice(title=_(u"Country"),
                                 vocabulary="getpaid.countries",
                                 default=u'BE')
    bill_postal_code = schema.TextLine(title=_(u"Zip Code"))
    vat_number = schema.TextLine(title=_(u"VAT Number"),
                                 required=False)


class IShippingAddress(Interface):
    """ where to send goods
    """
    ship_first_line = schema.TextLine(title=_(u"First Line"))
    ship_second_line = schema.TextLine(title=_(u"Second Line"),
                                       required=False)
    ship_city = schema.TextLine(title=_(u"City"))
    ship_country = schema.Choice(title=_(u"Country"),
                                 vocabulary="getpaid.countries",
                                 default=u'BE')
    ship_postal_code = schema.TextLine(title=_(u"Zip Code"))
