from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from uwosh.snippets.snippet import SnippetManager

class SnippetList(BrowserView):
	window_template = ViewPageTemplateFile('templates/snippet-window.pt')
	browser_template = ViewPageTemplateFile('templates/snippet-browser.pt')

	def __call__(self):

		if self.request.get('list-view'):
			return self.browser_template()
		else:
			return self.window_template()

	def getSnippets(self):
		sm = SnippetManager()

		snippets = sm.getSnippets()
		out = []
		for snippet in snippets:
			out.append(snippet)

		return out