from plone.app.testing import TEST_USER_NAME, PLONE_FIXTURE, login, \
    IntegrationTesting, PloneSandboxLayer, applyProfile, setRoles, \
    TEST_USER_ID, TEST_USER_PASSWORD


from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import unittest2 as unittest

from plone.testing import z2

from zope.configuration import xmlconfig

from uwosh.snippets.parser import SnippetParser
from uwosh.snippets.snippet import SnippetManager


class UwoshsnippetsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import uwosh.snippets
        xmlconfig.file(
            'configure.zcml',
            uwosh.snippets,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'uwosh.snippets:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])

UWOSH_SNIPPETS_FIXTURE = UwoshsnippetsLayer()
UWOSH_SNIPPETS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(UWOSH_SNIPPETS_FIXTURE,),
    name="UwoshsnippetsLayer:Integration"
)
UWOSH_SNIPPETS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(UWOSH_SNIPPETS_FIXTURE, z2.ZSERVER_FIXTURE),
    name="UwoshsnippetsLayer:Functional"
)


class BaseTest(unittest.TestCase):

    def setUp(self):
        portal = self.layer['portal']
        app = self.layer['app']

        portal.invokeFactory('Folder', '.snippets')
        folder = portal['.snippets']
        self.folder = folder
        folder.invokeFactory('Document', 'testDoc')
        self.doc = self.folder['testDoc']

        folder.invokeFactory('Folder', 'testFolder')
        folder2 = folder['testFolder']
        folder2.invokeFactory('Document', 'testDoc2')

        #need to verify that the regex will catch more than 1
        self.testString = "This is a !{{testDoc}}! test! Or is it !{{testDoc}}!?"

        self.doc.setText("meaningless")
        self.doc.setTitle("Meaningless")

    def tearDown(self):
        portal = self.layer['portal']
