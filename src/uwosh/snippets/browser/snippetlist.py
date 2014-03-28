from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from uwosh.snippets.snippetmanager import SnippetManager
import json

class SnippetList(BrowserView):
	window_template = ViewPageTemplateFile('templates/snippet-window.pt')
	browser_template = ViewPageTemplateFile('templates/snippet-browser.pt')

	def __call__(self):

		if self.request.get('list-view'):
			return self.browser_template()
		elif self.request.get('json'):
			if self.request.get('snippet_id'):
				sm = SnippetManager()
				snippet = sm.getSnippet(self.request.get('snippet_id'))

				return self.getSnippetAsJSON(snippet)
		else:
			return self.window_template()

	def getSnippets(self):
		sm = SnippetManager()

		snippets = sm.getSnippets()
		out = []
		for snippet in snippets:
			out.append(snippet)

		return out

	def getSnippetAsJSON(self, snippet):
		return json.dumps(snippet, default=lambda o: o.__dict__, sort_keys=True, indent=4)
