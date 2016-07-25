from Products.CMFPlone.utils import validate_json
from zope import schema
from zope.interface import Interface

import json


class ISnippetsLayer(Interface):
    pass


class ISnippetsSettings(Interface):

    related_items_options = schema.Text(
        title=u'Related items settings',
        description=u"Pattern options for related items widget used for snippet selection",
        required=False,
        constraint=validate_json,
        default=json.dumps({
            'selectableTypes': ['Document'],
            'baseCriteria': [{
                u'i': u'portal_type',
                u'v': [u'Document', u'Folder'],
                u'o': u'plone.app.querystring.operation.selection.any'
            }],
            "browsing": True,
            "basePath": "/.snippets"
        }, indent=4).decode('utf8'),
    )

    code_display_expression = schema.TextLine(
        title=u'Code display expression',
        description=u'TALs expression for what is displayed for the snippet when '
                    u'editing with TinyMCE. This can be html. '
                    u'Available variables: context, uid, header',
        default=u'string:Snippet:[ID=${context/@@uuid}]'
    )

    render_expression = schema.TextLine(
        title=u'Render expression',
        description=u'TALs expression for what is rendered on the page for the snippet',
        default=u'context/text/output|context/getText|nothing'
    )
