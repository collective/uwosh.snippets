from Products.Five.browser import BrowserView
from uwosh.snippets.snippetmanager import SnippetManager

from AccessControl import Unauthorized, getSecurityManager
from Products.CMFCore import permissions

class DeleteSnippet(BrowserView):

	def __call__(self):

		if self.request.get('snippet-id'):
			sm = SnippetManager()
			sm.deleteSnippet(self.request.get('snippet-id'))
			return True

	def render(self):
		"""
		Breaking things, because I can
		"""
		return 