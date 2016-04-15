# -*- extra stuff goes here -*-
import member

from zc.datetimewidget.datetimewidget import DateWidget
DateWidget._format = '%d/%m/%Y'


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
