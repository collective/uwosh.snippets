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

	#regEx to catch a string tagged like !{{id=this}}!
	#Eventually, needs support for international versions of youtube
	snippetRegex = '!{{\s*id\s*=\s*([a-zA-Z0-9_-]+?)\s*}}!'
	youtubeRegex = '!{{\s*youtube\s*=\s*([a-zA-Z0-9_.?=:/-]+?)\s*}}!'
	urlCheckRegex = '(http://|)?(www.youtube.com|youtu.be)/(watch\?v=|)?([a-zA-Z0-9_.?=/-]+)'

	def parsePage(self, pageText):
		result = self.parseSnippets(pageText)
		result = self.parseYouTubeLinks(result)

		return result

	def parseSnippets(self, pageText):
		pattern = re.compile(self.snippetRegex)
		matches = pattern.finditer(pageText)

		snippets = self.sm.getSnippets(True)

		ids = []

		for match in matches:
			pageText = replace(pageText, match.group(0), snippets[match.group(1)].getText())

		return pageText

	def parseYouTubeLinks(self, pageText):
		snippetPattern = re.compile(self.youtubeRegex)
		matches = snippetPattern.finditer(pageText)

		urlPattern = re.compile(self.urlCheckRegex)

		vids = []
		iframeStart = '<iframe width="560" height="315" src="//www.youtube.com/embed/'
		iframeEnd = '" frameborder="0" allowfullscreen></iframe>'

		for m in matches:
			url = urlPattern.match(m.group(1))
			if url:
				link = iframeStart + url.group(4) + iframeEnd
				pageText = replace(pageText, m.group(0), link)

		return pageText
