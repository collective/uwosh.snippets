from plone.directives.form import SchemaAddForm, SchemaEditForm
import zope.interface
from plone.autoform.form import AutoExtensibleForm
from five import grok
from Products.CMFCore.interfaces import ISiteRoot
import z3c
from Products.statusmessages.interfaces import IStatusMessage
from uwosh.snippets.snippetmanager import SnippetManager
from uwosh.snippets.browser.interfaces import ISnippet

_ = zope.i18nmessageid.MessageFactory(u'uwosh.snippets')

class SnippetForm(SchemaAddForm):

	schema = ISnippet
	label = u'Create a new snippet'

	@z3c.form.button.buttonAndHandler(_('Save'), name='save')
	def handleAdd(self, action):
		data, errors = self.extractData()
		if errors:
			self.status = self.formErrorsMessage
			return
		obj = self.createAndAdd(data)
		if obj is not None:
			# mark only as finished if we get the new object
			self._finishedAdd = True			
			IStatusMessage(self.request).addStatusMessage(_(u"Snippet saved"), "info")

	@z3c.form.button.buttonAndHandler(_(u'Cancel'), name='cancel')
	def handleCancel(self, action):
		IStatusMessage(self.request).addStatusMessage(_(u"Add New Snippet operation cancelled"), "info")
		self.request.response.redirect(self.nextURL())


	def create(self, data):
		sm = SnippetManager()

		#TODO:
		#Include support for different folders from this form.
		snippet = sm.createSnippet(data['title'], None ,data)
		

		return snippet

	def add(self, object):
		#Since, for now, snippets are based upon ATDocuments, their creation is fairly staight-forward.
		#So, we don't really need separate Add/Create steps.
		return

	def nextURL(self):

		return self.context.absolute_url() + '/@@create-snippet'


class SnippetEditForm(SchemaEditForm):

	schema = ISnippet

	label = u'Edit a snippet'
	def getContent(self):
		snippetId = self.request.get('snippet-id')
		sm = SnippetManager()
		snippet = sm.getSnippet(snippetId)

		return snippet

	
