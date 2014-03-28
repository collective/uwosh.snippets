import unittest2 as unittest
import pdb

from Products.CMFCore.utils import getToolByName

from uwosh.snippets.testing import BaseTest

from uwosh.snippets.testing import \
    UWOSH_SNIPPETS_INTEGRATION_TESTING

from plone.app.testing import setRoles, login, TEST_USER_NAME
from uwosh.snippets.snippet import Snippet
from uwosh.snippets.snippetmanager import SnippetManager


class TestSnippetManager(BaseTest):

    layer = UWOSH_SNIPPETS_INTEGRATION_TESTING

    def test_init(self):
    	sm = SnippetManager()
    	self.assertEqual(self.folder.getId(), sm.folder.getId())

    def test_create_snippet(self):
        sm = SnippetManager()
        sm.createSnippetDoc('new')

        self.assertTrue('new' in self.folder)

    def test_delete_snippet(self):
    	sm = SnippetManager()
    	sm.deleteSnippet('testDoc')

    	self.assertFalse('testDoc' in self.folder)

    def test_get_snippet(self):
    	sm = SnippetManager()

    	snippet = sm.getSnippet('testDoc')
    	self.assertTrue(snippet.getId() == 'testDoc')

    def test_get_snippets(self):
    	sm = SnippetManager()

    	snippets = sm.getSnippets()
    	self.assertTrue(len(snippets) == 2)

