# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.textfield.value import RichTextValue
from plone.testing import z2
from Products.CMFCore.utils import getToolByName
from zope.configuration import xmlconfig

import unittest


class UwoshsnippetsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML

        import plone.app.contenttypes
        self.loadZCML(package=plone.app.contenttypes)

        import uwosh.snippets
        xmlconfig.file(
            'configure.zcml',
            uwosh.snippets,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'uwosh.snippets:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        wft = getToolByName(portal, 'portal_workflow')
        wft.setDefaultChain('simple_publication_workflow')


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
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ('Member', 'Manager'))

    def _create_page(self, _id='test-snippet', title='Test Snippet', text='<p>foobar</p>'):
        page = api.content.create(type='Document', id=_id, title=title,
                                  container=self.portal,
                                  text=RichTextValue(text, 'text/html', 'text/html'))
        return page
