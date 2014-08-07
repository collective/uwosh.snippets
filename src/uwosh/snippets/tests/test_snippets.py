# -*- coding: utf-8 -*-
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

    def test_get_id(self):
    	sm = SnippetManager()
    	
        snippet = sm.getSnippet(self.doc.getId())
        self.assertEqual(self.doc.getId(), snippet.getId())

    def test_get_title(self):
        sm = SnippetManager()

        snippet = sm.getSnippet(self.doc.getId())
        self.assertEqual(self.doc.Title(), snippet.getTitle())

    def test_get_text(self):
        sm = SnippetManager()

        snippet = sm.getSnippet(self.doc.getId())
        self.assertEqual(self.doc.getRawText(), snippet.getText())

    def test_set_id(self):
        sm = SnippetManager()

        snippet = sm.getSnippet(self.doc.getId())
        newId = "words"
        snippet.setId(newId)
        self.assertEqual(newId, snippet.getId())

    def test_set_title(self):
        sm = SnippetManager()

        snippet = sm.getSnippet(self.doc.getId())
        newTitle = "words"
        snippet.setTitle(newTitle)
        self.assertEqual(newTitle, snippet.getTitle())

    def test_set_text(self):
        sm = SnippetManager()

        snippet = sm.getSnippet(self.doc.getId())
        newText = " words words words"
        self.assertEqual(self.doc.getRawText(), snippet.getText())

