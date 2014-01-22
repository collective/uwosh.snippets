import unittest2 as unittest
import pdb

from Products.CMFCore.utils import getToolByName

from uwosh.snippets.testing import BaseTest

from uwosh.snippets.testing import \
    UWOSH_SNIPPETS_INTEGRATION_TESTING

from plone.app.testing import setRoles, login, TEST_USER_NAME
from uwosh.snippets.snippet import SnippetManager, Snippet


class TestSnippetManager(BaseTest):

    layer = UWOSH_SNIPPETS_INTEGRATION_TESTING

    def test_create_snippet(self):
        sm = SnippetManager()
        sm.createSnippet('new')

        self.assertTrue('new' in self.folder)

