# -*- coding: utf-8 -*-
import unittest2 as unittest
import pdb

from Products.CMFCore.utils import getToolByName

from uwosh.snippets.testing import BaseTest

from uwosh.snippets.testing import \
	UWOSH_SNIPPETS_INTEGRATION_TESTING

from plone.app.testing import setRoles, login, TEST_USER_NAME

from uwosh.snippets.parser import SnippetParser


class TestSnippetParser(BaseTest):

	layer = UWOSH_SNIPPETS_INTEGRATION_TESTING

	#This is just a test to assure that the parser doesn't murder a helpless, unadourned string, just minding it's own business.
	def test_normal(self):
		sp = SnippetParser()
		text = sp.parsePage(self.normalString)

		correct = "This is a test! Or is it?"

		self.assertTrue( text != '' )
		self.assertEqual(text, correct)

	#This is a normal test to see if the parser works under normal circumstanes
	def test_single(self):
		sp = SnippetParser()
		text = sp.parsePage(self.testSingle)

		correct = "This is a meaningless test! Or is it?"

		self.assertTrue( text != '' )
		self.assertEqual(text, correct)

	#In this test, we're checking that the parser won't leave a snippet with a bad ID in the output.
	def test_bad_ids(self):
		sp = SnippetParser()
		text = sp.parsePage(self.testJunk)

		correct = "This is a  test! Or is it ?"

		self.assertTrue( text != '' )
		self.assertEqual(text, correct)

	#In this test, we check if the parser will catch the rare event where the JS fails to properly handle snippets on save.
	#Essentially, we're catching what is displayed to the user on the Edit page. The snippet plugs should never be in this form 
	#anywhere but the edit page.
	def test_dead_ids(self):
		sp = SnippetParser()
		text = sp.parsePage(self.testDeadSnippet)

		correct = "This is a  test! Or is it?"

		self.assertTrue( text != '' )
		self.assertEqual(text, correct)

	#This test assures that the parser will catch multiple instances of the same snippet
	def test_multiple_ids(self):
		sp = SnippetParser()
		text = sp.parsePage(self.testMultiple)

		correct = "This is a meaningless test! Or is it meaningless?"

		self.assertTrue( text != '' )
		self.assertEqual(text, correct)

	#This test assures that the parser doesn't grab a string with just an ordinary span in it
	def test_benign_span(self):
		sp = SnippetParser()
		text = sp.parsePage(self.benignSpan)

		correct = "This is a <span style=\"text-decoration: blink;\">meaningless test!</span> Or is it?"

		self.assertTrue( text != '' )
		self.assertEqual(text, correct)

	#This test assures that the parser will properly replace the snippet span with a normal span.
	#
	#....there's doesn't rely on the regex at all, so I don't see why it would possibly fail, but...eh
	def test_inner_span(self):
		sp = SnippetParser()
		text = sp.parsePage(self.innerSpan)

		correct = "This is a <span style=\"text-decoration: blink;\">stupid</span> test! Or is it?"

		self.assertTrue( text != '' )
		self.assertEqual(text, correct)

	#This test assures that the parser will properly handle multiple, DIFFERENT snippets in the same string
	def test_multiple_different(self):
		sp = SnippetParser()
		text = sp.parsePage(self.differentPlugs)

		correct = "This is a <span style=\"text-decoration: blink;\">stupid</span> test! Or is it meaningless?"

		self.assertTrue( text != '' )
		self.assertEqual(text, correct)
