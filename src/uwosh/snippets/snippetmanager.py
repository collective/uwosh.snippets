from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from uwosh.snippets.snippet import Snippet
import re

class SnippetManager():
	#TODO: Get rid of the current folder scheme and 
	#make it automated

	folderName = '.snippets'

	def __init__(self):

		portal = getSite()
		pt = getToolByName(portal, 'portal_url')
		path = pt.getPortalObject()

		self.folder = path[self.folderName]

		if not self.folder.getExcludeFromNav():
			self.folder.setExcludeFromNav('true')

		self.index = self.indexSnippets()

	def createSnippetDoc(self, snippetId, folder=False):

		if not folder:
			folder = self.folder

		if not snippetId in folder:
			return folder.invokeFactory("Document", snippetId)
		else:
			raise LookupError(u'Invalid or duplicate id: ' + snippetId)

	def createSnippet(self, snippetId, folder=False, data=False):

		if not folder:
			folder = self.folder

		self.createSnippetDoc(snippetId, folder) 

		doc = self.folder[snippetId]
		if data['title']:
			doc.setTitle(data['title'])

		if data['description']:
			doc.setDescription(data['description'])

		if data['text']:
			doc.setText(data['text'])

		self.index = self.indexSnippets()

		#this returns the actual snippet object, not the document
		return self.getSnippet(snippetId)

	def deleteSnippet(self, snippetId):

		folder = self.index[snippetId].aq_parent
		folder.manage_delObjects(snippetId)

	def getSnippet(self, snippetId):

		snippet = Snippet()
		snippet.setId(snippetId)
		doc = self.index[snippetId]

		snippet.setText( doc.getRawText() )
		snippet.setTitle(doc.Title())
		snippet.setDescription(doc.Description())

		portal = getSite()
		wf = getToolByName(portal, 'portal_workflow')
		wfs = wf.getInfoFor(doc, 'review_state')
		snippet.setWorkflowState(wfs)

		return snippet

	def getSnippets(self, asDict=False):
		
		"""
		Recursively finds all the snippet documents within the 
		folder, and all sub-folders.
		"""
		
		items = self.index

		if asDict:
			snippets = {}
		else:
			snippets = []

		for item in items:

				if asDict:
					snippets[item] = self.getSnippet(item)
				else:
					snippets.append(self.getSnippet(item))

		return snippets

	def indexSnippets(self, snippets=False, folder=False):
		
		if not snippets:
			snippets = {}

		if not folder:
			folder = self.folder

		items = folder.contentItems()

		for item in items:
			if( item[1].Type() == u'Page' ):

				snippets[item[0]] = item[1]
			elif( item[1].Type() == u'Folder' ):
				snippets = self.indexSnippets(snippets, item[1])

		return snippets


	def updateDoc(self, snippetId, data):
		
		#This updates the underlying ATDocument after
		#z3c.form.EditForm updates the Snippet object
		#See uwosh.snippets.browser.addsnippet.SnippetEditForm

		doc = self.index[snippetId]

		if 'title' in data:
			doc.setTitle(data['title'])

		if 'description' in data:
			doc.setDescription(data['description'])

		if 'text' in data:
			doc.setText(data['text'])



