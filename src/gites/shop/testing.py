from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import gites.shop


GITES_SHOP = PloneWithPackageLayer(
    zcml_package=gites.shop,
    zcml_filename='testing.zcml',
    gs_profile_id='gites.shop:testing',
    name="GITES_SHOP")

GITES_SHOP_INTEGRATION = IntegrationTesting(
    bases=(GITES_SHOP, ),
    name="GITES_SHOP_INTEGRATION")

GITES_SHOP_FUNCTIONAL = FunctionalTesting(
    bases=(GITES_SHOP, ),
    name="GITES_SHOP_FUNCTIONAL")
