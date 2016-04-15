from zope import schema
from gites.locales import GitesMessageFactory as _
from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager
from getpaid.core.fields import PhoneNumber, emailValidator
from getpaid.core.interfaces import EmailFormatPreferenceVocabulary


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


class IUserContactInformation(Interface):

    name = schema.TextLine(title=_(u"Your Name"))

    phone_number = PhoneNumber(title=_(u"Phone Number"),
                               description=_(u"Only digits allowed - e.g. 3334445555 and not 333-444-5555 "))

    email = schema.TextLine(title=_(u"Email"),
                            description=_(u"Contact Information"),
                            constraint=emailValidator)

    marketing_preference = schema.Bool(title=_(u"Can we contact you with offers?"),
                                       required=False)

    email_html_format = schema.Choice(title=_(u"Email Format"),
                                      description=_(u"Would you prefer to receive rich html emails or only plain text"),
                                      vocabulary=EmailFormatPreferenceVocabulary,
                                      default=True)

    birth_date = schema.Date(title=_(u"Birthday"))
