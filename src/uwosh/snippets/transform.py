from zope.interface import implements, Interface
from zope.component import adapts

from plone.transformchain.interfaces import ITransform
from repoze.xmliter.utils import getHTMLSerializer

from uwosh.snippets.parser import SnippetParser
from Products.CMFCore.utils import getToolByName
from uwosh.snippets.browser.interfaces import SnippetsLayer
from zope.component.hooks import getSite

class SnippetTransform(object):
    implements(ITransform)
    adapts(Interface, SnippetsLayer)

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
            result = getHTMLSerializer(result, pretty_print=False)
        except (TypeError, etree.ParseError):
            return None

        return [ parser.parsePage(r) for r in result ]
