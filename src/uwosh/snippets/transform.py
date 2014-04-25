from zope.interface import implements, Interface
from zope.component import adapts

from plone.transformchain.interfaces import ITransform
from repoze.xmliter.utils import getHTMLSerializer

from uwosh.snippets.parser import SnippetParser
from Products.CMFCore.utils import getToolByName

from zope.component.hooks import getSite

class SnippetTransform(object):
    implements(ITransform)
    adapts(Interface, Interface) # any context, any request

    order = 9000

    def __init__(self, published, request):

        self.published = published
        self.request = request

    def transformBytes(self, result, encoding):
        return result

    def transformUnicode(self, result, encoding):
        return result

    def transformIterable(self, result, encoding):

        site = getSite()

        #This prevents the transform from running even when
        #The add-on isn't installed =\ 
        #
        #There must be a better way....
        qi = getToolByName(site, 'portal_quickinstaller')
        if not qi.isProductInstalled('uwosh.snippets'):
            return result

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
