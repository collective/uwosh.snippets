from plone.directives import form
import zope.schema
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.autoform.directives import widget

class ISnippet(form.Schema):

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