import re
from plone.registry import field
from plone.registry.record import Record
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from string import replace

from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.utils import getToolByName

from uwosh.snippets.snippetmanager import SnippetManager

class SnippetParser():

	def __init__(self):
		self.sm = SnippetManager()

	snippetRegex = '<span(?=.*?data-type="snippet_tag"\s*)(?=.*?data-snippet-id="([a-zA-Z0-9_-]+?)"\s*).*?><\/span>'

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
