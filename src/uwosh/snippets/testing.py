# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_NAME, PLONE_FIXTURE, login, \
    IntegrationTesting, PloneSandboxLayer, applyProfile, setRoles, \
    TEST_USER_ID, TEST_USER_PASSWORD


from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from Products.CMFCore.utils import getToolByName

import unittest2 as unittest

from plone.testing import z2

from zope.configuration import xmlconfig

from uwosh.snippets.parser import SnippetParser
from uwosh.snippets.snippetmanager import SnippetManager


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

        if not portal['.snippets']:
            portal.invokeFactory('Folder', '.snippets')

        folder = portal['.snippets']
        self.folder = folder
        folder.invokeFactory('Document', 'testDoc')
        self.doc = self.folder['testDoc']

        folder.invokeFactory('Folder', 'testFolder')
        folder2 = folder['testFolder']
        folder2.invokeFactory('Document', 'testDoc2')
        self.doc2 = folder2['testDoc2']

        #########Test Strings###########################

        #Control case. No plugs whatsoever
        self.normalString = "This is a test! Or is it?"

        #Normal test case, with 1 valid plug
        self.testSingle = 'This is a <span data-type="snippet_tag" data-snippet-id="testDoc"></span> test! Or is it?'

        #need to verify that the regex will catch more than 1
        self.testMultiple = 'This is a <span data-type="snippet_tag" data-snippet-id="testDoc"></span> test! Or is it <span data-type="snippet_tag" data-snippet-id="testDoc"></span>?'

        #An example of a string with an invalid snippet ID
        self.testJunk = 'This is a <span data-type="snippet_tag" data-snippet-id="JunkID"></span> test! Or is it <span data-type="snippet_tag" data-snippet-id="JunkID"></span>?'

        #An example where the JS failed to remove handle the in-editor snippet. 
        self.testDeadSnippet = 'This is a <span data-type="snippet_tag" data-snippet-id="oldDoc">meaningless</span> test! Or is it?'

        #An example where a snippet is inside another span. This verifies the parser's RegEx's ability to correctly pull out snippets.
        self.benignSpan = 'This is a <span style="text-decoration: blink;"><span data-type="snippet_tag" data-snippet-id="testDoc"></span> test!</span> Or is it?'

        #An example where a snippet contains a span. Since the span is inserted after the regex runs, this *shouldn't* be an issue, 
        #but it never hurts to be careful
        self.innerSpan = 'This is a <span data-type="snippet_tag" data-snippet-id="testDoc2"></span> test! Or is it?'

        #An example with 2 different plugs
        self.differentPlugs = 'This is a <span data-type="snippet_tag" data-snippet-id="testDoc2"></span> test! Or is it <span data-type="snippet_tag" data-snippet-id="testDoc"></span>?'

        ################################################


        self.doc.setText("meaningless")
        self.doc.setTitle("Meaningless")

        self.doc2.setText("<span style=\"text-decoration: blink;\">stupid</span>")

        wft = getToolByName(portal, 'portal_workflow')
        wft.setDefaultChain('simple_publication_workflow')

    def tearDown(self):
        portal = self.layer['portal']
