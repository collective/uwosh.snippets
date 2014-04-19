from plone.directives.form import SchemaAddForm, SchemaEditForm
from plone.autoform.form import AutoExtensibleForm
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from uwosh.snippets.browser.interfaces import ISnippet
from uwosh.snippets.snippetmanager import SnippetManager

from z3c.form.interfaces import ActionExecutionError
from zope.interface import Invalid

import re
import zope
import z3c

_ = zope.i18nmessageid.MessageFactory(u'uwosh.snippets')

class SnippetForm(SchemaAddForm):

	schema = ISnippet
	label = u'Create a new snippet'
	template = ViewPageTemplateFile('templates/snippet-create.pt')

	@z3c.form.button.buttonAndHandler(_('Save'), name='save')
	def handleAdd(self, action):

		data, errors = self.extractData()

		sm = SnippetManager()
		index = sm.indexSnippets()

		if 'title' in data:
			if data['title'] in index:
				raise ActionExecutionError(Invalid(u"This title is already in use."))

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

	template = ViewPageTemplateFile('templates/snippet-create.pt')
	schema = ISnippet

	label = u'Edit a snippet'
	def getContent(self):
		try:
			snippetId = self.request.form['form.widgets.id']
		except KeyError:
			snippetId = self.request.get('snippet-id')

		if snippetId is None:
			return False

		sm = SnippetManager()
		snippet = sm.getSnippet(snippetId)

		return snippet

	def applyChanges(form, data):
		sm = SnippetManager()
		snippet = sm.getSnippet(data['id'])

		changes = {}
		for item in data:
			attribute = getattr(snippet, item)
			if item == 'text':
				#For whatever reason, tinyMCE loves using the \xc2\xa0 code 
				data[item] = str(data[item]).replace('\xc2\xa0', ' ')

			if attribute == data[item]:
				continue
			else:
				changes[item] = data[item]

		sm.updateDoc(data['id'], changes)

		return changes


	
