# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from uwosh.snippets.snippet import Snippet
from zope.component.hooks import getSite

try:
    from plone.app.textfield.value import RichTextValue
except ImportError:
    pass


class SnippetManager():
    # The SnippetManager class organizes, collects, and creates all the snippets.
    # It is in charge of create the Snippet objects from the ATDocument objects
    # representing them. It also handles creation/deletion of ATDocument objects.

    folderName = '.snippets'

    def __init__(self):

        portal = getSite()
        pt = getToolByName(portal, 'portal_url')
        path = pt.getPortalObject()

        self.folder = path[self.folderName]

        self.index = self.indexSnippets()

    def createSnippetDoc(self, snippetId, folder=False):

        if not folder:
            folder = self.folder

        if snippetId not in folder:
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
            if hasattr(doc, 'setText'):
                doc.setText(data['text'])
            else:
                doc.text = RichTextValue(data['text'], mimeType='text/html',
                                         outputMimeType='text/x-html-safe')

        self.index = self.indexSnippets()

        # this returns the actual snippet object, not the document
        return self.getSnippet(snippetId)

    def deleteSnippet(self, snippetId):

        folder = self.index[snippetId].aq_parent
        folder.manage_delObjects(snippetId)
        self.indexSnippets()

    def getSnippet(self, snippetId):

        snippet = Snippet()
        snippet.setId(snippetId)
        doc = self.index[snippetId]

        if hasattr(doc, 'getRawText'):
            # archetypes
            snippet.setText(doc.getRawText())
        else:
            snippet.setText(doc.text.output)

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

        for item in items.keys():

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
            if item[1].portal_type == 'Document':

                snippets[item[0]] = item[1]
            elif item[1].portal_type == u'Folder':
                snippets = self.indexSnippets(snippets, item[1])

        return snippets

    def updateDoc(self, snippetId, data):

        # This updates the underlying ATDocument after
        # z3c.form.EditForm updates the Snippet object
        # See uwosh.snippets.browser.addsnippet.SnippetEditForm

        doc = self.index[snippetId]

        if 'title' in data:
            doc.setTitle(data['title'])

        if 'description' in data:
            doc.setDescription(data['description'])

        if 'text' in data:
            if hasattr(doc, 'setText'):
                doc.setText(data['text'])
            else:
                doc.text = RichTextValue(data['text'], mimeType='text/html',
                                         outputMimeType='text/x-html-safe')
