from Products.Five.browser import BrowserView
from uwosh.snippets.snippetmanager import SnippetManager

from AccessControl import Unauthorized, getSecurityManager
from Products.CMFCore import permissions
import urllib, re

class DeleteSnippet(BrowserView):

	def __call__(self):

		if self.request.get('snippet-id'):
			sm = SnippetManager()
			snippetId = self.request.get('snippet-id')
			try:
				sm.deleteSnippet(snippetId)
				return True
			except KeyError:
				try:
					snippetId = re.sub(r'\W', '', self.request.get('snippet-id'))
					sm.deleteSnippet(snippetId)
				except KeyError:
					return False		


	def render(self):
		"""
		Breaking things, because I can
		"""
		return 