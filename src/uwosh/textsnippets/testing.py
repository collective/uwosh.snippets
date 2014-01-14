from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class UwoshtextsnippetsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import uwosh.textsnippets
        xmlconfig.file(
            'configure.zcml',
            uwosh.textsnippets,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'uwosh.textsnippets:default')

UWOSH_TEXTSNIPPETS_FIXTURE = UwoshtextsnippetsLayer()
UWOSH_TEXTSNIPPETS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(UWOSH_TEXTSNIPPETS_FIXTURE,),
    name="UwoshtextsnippetsLayer:Integration"
)
UWOSH_TEXTSNIPPETS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(UWOSH_TEXTSNIPPETS_FIXTURE, z2.ZSERVER_FIXTURE),
    name="UwoshtextsnippetsLayer:Functional"
)
