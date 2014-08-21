# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from uwosh.snippets.snippetmanager import SnippetManager
from Products.CMFCore.utils import getToolByName
import json
import urllib

from AccessControl import getSecurityManager, Unauthorized
from Products.CMFCore.permissions import AddPortalContent, ModifyPortalContent, DeleteObjects

class SnippetList(BrowserView):
	window_template = ViewPageTemplateFile('templates/snippet-window.pt')
	browser_template = ViewPageTemplateFile('templates/snippet-browser.pt')

	def __call__(self):

		if self.request.get('list-view'):
			return self.browser_template()
		elif self.request.get('json'):
			if self.request.get('snippet_id'):
				self.request.response.setHeader('Content-Type', 'application/JSON;;charset="utf-8"')
				sm = SnippetManager()

				snippetId = self.request.get('snippet_id')
				snippetId = urllib.unquote(snippetId)

				snippetList = snippetId.split(',')

				snippet = self.getSnippetList(snippetList)

				return snippet
		else:
			return self.window_template()

	#Used by templates to check if the user has the rights to create/update/delete snippets
	def getAllowed(self):
		security = getSecurityManager()
		sm = SnippetManager()

		if security.checkPermission(AddPortalContent, sm.folder):
			return True
		else:
			return False

	def getMemberPortal(self):
		return getToolByName(self, 'portal_membership')
	
	def getSnippets(self):
		sm = SnippetManager()

		snippets = sm.getSnippets()
		out = []
		for snippet in snippets:

			security = getSecurityManager()
			doc = sm.folder[snippet.getId()]

			if security.checkPermission(ModifyPortalContent, doc):
				snippet.w = True
			else:
				snippet.w = False

			if security.checkPermission(DeleteObjects, doc):
				snippet.d = True
			else:
				snippet.d = False

			out.append(snippet)

		return out

	def getSnippetAsJSON(self, snippet):
		return json.dumps(snippet, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def getSnippetList(self, snippetList):
		sm = SnippetManager()

		out = []

		for snippet in snippetList:
			try:
				item = sm.getSnippet(snippet)

			except KeyError:
				#Getting here means the request snippetID doesn't exist
				#Setting the items "dead" tells the AJAX handler to remove the snippet tag,
				#if one exsists
				item = { 
					'id': snippet,
					'dead': True
				}

			out.append( item )

		return self.getSnippetAsJSON( out )

	def siteUrl(self):
		portal_url = getToolByName(self.context, "portal_url")
		portal = portal_url.getPortalObject()
		return portal.absolute_url()

	def render(self):
		"""
		Breaking things, because I can
		"""
		return
