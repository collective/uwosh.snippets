# -*- coding: utf-8 -*-
from lxml import etree
from plone.uuid.interfaces import IUUID
from lxml.html import fromstring
from plone import api
from plone.app.uuid.utils import uuidToObject
from plone.registry.interfaces import IRegistry
from plone.transformchain.interfaces import ITransform
from Products.CMFCore.Expression import Expression
from repoze.xmliter.utils import getHTMLSerializer
from uwosh.snippets.interfaces import ISnippetsLayer
from uwosh.snippets.utils import ExpressionEvaluator
from uwosh.snippets.utils import get_header_from_text
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from zope.interface import Interface


class SnippetTransform(object):
    implements(ITransform)
    adapts(Interface, ISnippetsLayer)

    order = 9000

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def transformBytes(self, result, encoding):
        return result

    def transformUnicode(self, result, encoding):
        return result

    def transformIterable(self, result, encoding):
        if self.request['PATH_INFO'].endswith('edit'):
            return result

        contentType = self.request.response.getHeader('Content-Type')
        if contentType is None or not contentType.startswith('text/html'):
            return None

        ce = self.request.response.getHeader('Content-Encoding')
        if ce and ce in ('zip', 'deflate', 'compress'):
            return None
        try:
            if result == ['']:
                return None

            result = getHTMLSerializer(result, pretty_print=False)
        except (TypeError):
            return None

        site = api.portal.get()
        site_path = '/'.join(site.getPhysicalPath())
        root = result.tree.getroot()
        rendered = {}

        registry = getUtility(IRegistry)

        evaluator = ExpressionEvaluator()
        expression = Expression(registry.get('uwosh.snippets.render_expression',
                                             'context/text/output|context/getText|nothing'))

        for el in root.cssselect('[data-type="snippet_tag"]'):
            snippet_name = el.attrib.get('data-snippet-id')
            header = el.attrib.get('data-header')
            if snippet_name not in rendered:
                ob = uuidToObject(snippet_name)
                if ob is None:
                    ob = site.restrictedTraverse('.snippets/' + snippet_name, None)
                if ob is not None:
                    rendered[snippet_name] = {
                        'html': evaluator.evaluate(expression, ob),
                        'ob': ob
                    }

            if snippet_name in rendered:
                data = rendered[snippet_name]
                ob = data['ob']
                val = data['html']
                if header:
                    val = get_header_from_text(val, header)

                snippet_container = etree.Element('div')

                className = 'snippet-container snippet-container-{}'.format(
                    ob.portal_type.lower().replace(' ', '-')
                )

                if not val:
                    val = '<p>Snippet could not be found</p>'
                    className += ' snippet-container-missing'

                snippet_container.attrib.update({
                    'class': className,
                    'data-source-uid': IUUID(ob),
                    'data-source-id': ob.getId(),
                    'data-source-title': ob.Title(),
                    'data-source-path': '/'.join(ob.getPhysicalPath())[len(site_path):],
                    'data-source-header': header or ''
                })

                content_el = fromstring(val)
                if content_el.tag == 'div':
                    # unwrap: fromstring auto adds div around content so we'll just take the
                    # inside of it instead
                    for inside_el in content_el:
                        snippet_container.append(inside_el)
                else:
                    snippet_container.append(content_el)

                if val:
                    parent = el.getparent()
                    idx = parent.index(el)
                    parent[idx] = snippet_container

        return result
