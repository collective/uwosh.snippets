from zope.interface import implements, Interface
from zope.component import adapts

from plone.transformchain.interfaces import ITransform

class SnippetTransform(object):
    implements(ITransform)
    adapts(Interface, Interface) # any context, any request

    order = 1000

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def transformBytes(self, result, encoding):
        return result

    def transformUnicode(self, result, encoding):
        return result

    def transformIterable(self, result, encoding):
        return [s.upper() for s in result]
