from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

class Snippet():

	def getDescription(self):
		return self.description

	def getId(self):
		return self.id

	def getText(self):
		return self.text

	def getTitle(self):
		return self.title

	def setDescription(self, description):
		self.description = description

	def setId(self, snippetId):
		self.id = snippetId

	def setText(self, snippetText):
		self.text = snippetText

	def setTitle(self, snippetTitle):
		self.title = snippetTitle

class SnippetManager():

	folderName = '.snippets'

	def __init__(self):

		portal = getSite()
		pt = getToolByName(portal, 'portal_url')
		path = pt.getPortalObject()

		if not self.folderName in path:
			path.invokeFactory("Folder", self.folderName)

		self.folder = path[self.folderName]

		if not self.folder.getExcludeFromNav():
			self.folder.setExcludeFromNav('true')

	def createSnippet(self, snippetId, folder=False):

		if not folder:
			folder = self.folder

		if not snippetId in folder:
			return folder.invokeFactory("Document", snippetId)
		else:
			raise LookupError(u'Invalid or duplicate id: ' + snippetId)

	def deleteSnippet(self, snippetId, folder=False):

		if not folder:
			folder = self.folder

		if snippetId in folder:
			folder.manage_delObjects(snippetId)

	def getSnippet(self, snippetId, folder=False):

		if not folder:
			folder = self.folder

		if snippetId in folder:
			snippet = Snippet()
			snippet.setId(snippetId)
			doc = folder[snippetId]

			snippet.setText(doc.getRawText())
			snippet.setTitle(doc.Title())
			snippet.setDescription(doc.Description())

			return snippet
		else:
			raise LookupError(u'Invalid id: ' + snippetId)

	def getSnippets(self, asDict=False, folder=False, snippets=False):
		
		"""
		Recursively finds all the snippet documents within the 
		folder, and all sub-folders.
		"""

		if not folder:
			folder = self.folder
		
		items = folder.contentItems()

		if not snippets:
			if asDict:
				snippets = {}
			else:
				snippets = []

		for item in items:
			if( item[1].Type() == u'Page' ):

				if asDict:
					snippets[item[0]] = self.getSnippet(item[0], folder)
				else:
					snippets.append(self.getSnippet(item[0], folder))
			elif( item[1].Type() == u'Folder' ):
				snippets = self.getSnippets(asDict, item[1], snippets)

		return snippets








