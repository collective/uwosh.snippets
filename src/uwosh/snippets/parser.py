# -*- coding: utf-8 -*-
import re
from plone.registry import field
from plone.registry.record import Record
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from string import replace

from Products.CMFCore.utils import getToolByName

from uwosh.snippets.snippetmanager import SnippetManager

class SnippetParser():
	#The SnippetParser class handles the finding/replacing of snippets within a pages content.
	#The page content is passed to a Parser object, and it then tries to pattern match 
	#the <span> tags used to represent snippets. If it finds a valid snippet tag, 
	#it replaces it with the appropriate snippet text. 

	def __init__(self):
		self.sm = SnippetManager()

	snippetRegex = '<span(?=[^>]*?data-type="snippet_tag"\s*)(?=[^>]*?data-snippet-id="([a-zA-Z0-9\s_-]+?)"\s*)[^>]+?>[^<>]*?<\/span>'

	def parsePage(self, pageText):
		result = self.parseSnippets(pageText)

		return result

	def parseSnippets(self, pageText):
		pattern = re.compile(self.snippetRegex)
		matches = pattern.finditer(pageText)

		snippets = self.sm.getSnippets(True)
		for match in matches:
			try:
				pageText = replace(pageText, match.group(0), snippets[match.group(1)].getText())
			except KeyError:
				#The snippetID was invalid
				pageText = replace(pageText, match.group(0), '')

		return pageText
