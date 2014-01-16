from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

class Snippet():

	def __init__(self, snippetId):
		id = snippetId

	def getId(self):
		return self.id

	def getText(self):
		return self.text

	def getTitle(self):
		return self.title

	def setText(self, snippetText):
		self.text = snippetText

	def setTitle(self, snippetTitle):
		self.title = snippetTitle

class SnippetManager():

	folderName = '.textsnippets'

	def __init__(self):

		portal = getSite()
		pt = getToolByName(portal, 'portal_url')
		path = pt.getPortalObject()

		if not self.folderName in path:
			path.invokeFactory("Folder", folderName)

		self.folder = path[self.folderName]

		if not self.folder.getExcludeFromNav():
			self.folder.setExcludeFromNav('true')

	def createSnippet(self, snippetId):
		if not snippetId in self.folder:
			return self.folder.invokeFactory("Document", snippetId)
		else:
			raise IndexError(u'Invalid or duplicate id: %s') % snippetId

	def deleteSnippet(self, snippetId):
		if snippetId in self.folder:
			self.folder.manage_delObject(snippetId)

	def getSnippet(self, snippetId):
		if snippetId in self.folder:
			snippet = Snippet(snippetId)
			doc = self.folder[snippetId]

			snippet.setText(doc.getRawText())
			snippet.setTitle(doc.Title())

			return snippet
		else:
			raise LookupError(u'Invalid Snippet id: %s') % snippetId

	def getSnippets(self):
		items = self.folder.contentItems()

		snippets = {}

		for item in items:
			snippets[item[0]] = self.getSnippet(item[0])

		return snippets

	def snippetExists(self, snippetId):
		return snippetId in self.folder





