import re
from plone.registry import field
from plone.registry.record import Record
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from string import replace

from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.utils import getToolByName

from uwosh.snippets.snippet import SnippetManager

class SnippetParser():

	def __init__(self):
		self.sm = SnippetManager()

	#regEx to catch a string tagged like !{{this}}!
	regex = '!{{([a-zA-Z0-9_-]+?)}}!'

	def findIds(self, pageText):
		pattern = re.compile(self.regex)
		matches = pattern.finditer(pageText)

		ids = []

		for match in matches:
			ids.append( match.group(1) )

		return ids

	def replaceIds(self, pageText):
		snippets = self.sm.getSnippets(True)

		ids = self.findIds(pageText)

		for i in ids:
			if( i in snippets ):
				slug = '!{{' + i + '}}!'
				pageText = replace(pageText, slug, snippets[i].getText())

		return pageText
