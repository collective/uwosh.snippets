# -*- coding: utf-8 -*-
from lxml.html import fromstring
from plone import api
from plone.app.uuid.utils import uuidToObject
from plone.dexterity.interfaces import IDexterityContent
from plone.transformchain.interfaces import ITransform
from repoze.xmliter.utils import getHTMLSerializer
from uwosh.snippets.browser.interfaces import ISnippetsLayer
from uwosh.snippets.parser import SnippetParser
from zope.component import adapts
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

        try:
            parser = SnippetParser()
        except AttributeError:
            return result

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
        root = result.tree.getroot()
        rendered = {}
        for el in root.cssselect('[data-type="snippet_tag"]'):
            snippet_name = el.attrib.get('data-snippet-id')
            if snippet_name not in rendered:
                ob = uuidToObject(snippet_name)
                if ob is None:
                    ob = site.restrictedTraverse('.snippets/' + snippet_name, None)
                if ob is not None:
                    if IDexterityContent.providedBy(ob):
                        rendered[snippet_name] = ob.text.output
                    else:
                        rendered[snippet_name] = ob.getText()
            if snippet_name in rendered:
                parent = el.getparent()
                idx = parent.index(el)
                parent[idx] = fromstring(rendered[snippet_name])

        return result

        return [parser.parsePage(r) for r in result]
