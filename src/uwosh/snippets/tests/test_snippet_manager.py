# -*- coding: utf-8 -*-
import unittest2 as unittest
import pdb

from Products.CMFCore.utils import getToolByName

from uwosh.snippets.testing import BaseTest

from uwosh.snippets.testing import \
    UWOSH_SNIPPETS_INTEGRATION_TESTING

from plone.app.testing import setRoles, login, TEST_USER_NAME, applyProfile
from uwosh.snippets.snippet import Snippet
from uwosh.snippets.snippetmanager import SnippetManager


class TestSnippetManager(BaseTest):

    layer = UWOSH_SNIPPETS_INTEGRATION_TESTING

    #This test verifies that the snippet manager is setting up properly. 
    #It's testing whether or not it grabs the correct folder for it's 
    #base directory.
    def test_init(self):
    	sm = SnippetManager()
    	self.assertEqual(self.folder.getId(), sm.folder.getId())

    #This test just verifies if the manager will properly create a snippet
    #Specifically, it's looking for the document holding the data for the snippet
    def test_create_snippet(self):
        sm = SnippetManager()
        sm.createSnippetDoc('new')

        self.assertTrue('new' in self.folder)

    #This test verifies that the manager will not try to create multiple snippets
    #with an identical ID. This scenario shouldn't be encounterd IRL, since the
    #form schema for the snippets doesn't allow duplicates.
    def test_create_dup_snippet(self):
        sm = SnippetManager()
        try:
            out = sm.createSnippetDoc('testDoc')
        except LookupError:
            out = "exception"

        self.assertEqual( out, "exception" )

    #This test verfies that the manager will correctly delete
    #the document representing a snippet
    def test_delete_snippet(self):
    	sm = SnippetManager()
    	sm.deleteSnippet('testDoc')

    	self.assertFalse('testDoc' in self.folder)

    #This test verifies if the manager will grab/create a snippet from an ID
    def test_get_snippet(self):
    	sm = SnippetManager()

    	snippet = sm.getSnippet('testDoc')
    	self.assertTrue(snippet.getId() == 'testDoc')

    #This test verifies that the manager throws an exception when it's asked to get a snippet that doesn't exist.
    #This shouldn't ever happen IRL because the UI doesn't have any form of "get snippet by name" feature
    def test_get_inv_snippet(self):
        sm = SnippetManager()

        try:
            snippet = sm.getSnippet('Junk')
        except LookupError:
            snippet = "exception"

        self.assertEqual(snippet, "exception")

    #This test verifies that the manager will return all the snippets at once, when requested.
    def test_get_snippets(self):
    	sm = SnippetManager()

    	snippets = sm.getSnippets()
    	self.assertTrue(len(snippets) == 2)

