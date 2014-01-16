import unittest2 as unittest
import pdb

from Products.CMFCore.utils import getToolByName

from uwosh.textsnippets.testing import BaseTest

from uwosh.textsnippets.testing import \
    UWOSH_TEXTSNIPPETS_INTEGRATION_TESTING

from plone.app.testing import setRoles, login, TEST_USER_NAME
from uwosh.textsnippets.snippet import SnippetManager, Snippet


class TestSnippetManager(BaseTest):

    layer = UWOSH_TEXTSNIPPETS_INTEGRATION_TESTING

    def test_create_snippet(self):
        sm = SnippetManager()
        sm.createSnippet('new')

        self.assertTrue('new' in self.folder)

