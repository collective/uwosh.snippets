from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from uwosh.snippets.snippet import SnippetManager

class SnippetList(BrowserView):
	template = ViewPageTemplateFile('templates/snippet-list.pt')

	def __call__(self):
		return self.template()

	def getSnippets(self):
		sm = SnippetManager()

		snippets = sm.getSnippets()
		out = []
		for snippet in snippets:
			out.append(snippet)

		return out