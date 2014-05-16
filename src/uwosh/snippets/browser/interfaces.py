from plone.directives import form
import zope.schema
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.autoform.directives import widget
from zope.interface import Interface

class ISnippet(form.Schema):

	#Hidden field for the snippetId. This actually represents the 
	#ID of the document storing the snippet. Since the ATDocument factory
	#sets its own ID based on the title, we don't need to set it ourselves in the Add form
	form.mode(id='hidden')
	id = zope.schema.TextLine(title=u'Hidden ID field', required=False)

	title = zope.schema.TextLine(
	                             title=u'Title',
	                             description=u'The title to associate with the snippet.',
	                             required=True)

	description = zope.schema.Text(
	                             title=u'Description',
	                             description=u'A short explanation of the snippet.',
	                             required=True)

	form.widget(text=WysiwygFieldWidget)
	text = zope.schema.Text(
	                             title=u'Body',
	                             description=u'The actual content to be rendered on the page.',
	                             required=True)

class SnippetsLayer(Interface):
	pass