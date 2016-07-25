from zope.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue
from zope.keyreference.interfaces import NotYet
from zope.component import getUtility
from lxml.html import fromstring
from plone.dexterity.interfaces import IDexterityFTI
from plone.app.textfield import RichText
from plone.app.uuid.utils import uuidToObject
from plone.dexterity.utils import getAdditionalSchemata
from zope.schema import getFieldsInOrder
from plone.app.linkintegrity.interfaces import IRetriever
from plone.app.linkintegrity.handlers import check_linkintegrity_dependencies
from plone.app.linkintegrity.handlers import updateReferences
from plone.app.linkintegrity.handlers import getObjectsFromLinks


def getSnippetRefsFromHtml(html):
    intids = getUtility(IIntIds)
    dom = fromstring(html)
    refs = set()
    for el in dom.cssselect('[data-type="snippet_tag"]'):
        snippet_name = el.attrib.get('data-snippet-id')
        ob = uuidToObject(snippet_name)
        if ob:
            objid = None
            try:
                objid = intids.getId(ob)
            except KeyError:
                try:
                    intids.register(ob)
                    objid = intids.getId(ob)
                except NotYet:
                    # if we get a NotYet error, the object is not
                    # attached yet and we will need to get links
                    # at a later time when the object has an intid
                    pass
            if objid:
                refs.add(RelationValue(objid))
    return refs


def getSnippetRefs(obj):
    fti = getUtility(IDexterityFTI, name=obj.portal_type)
    schema = fti.lookupSchema()
    additional_schema = getAdditionalSchemata(
        context=obj, portal_type=obj.portal_type)
    schemas = [i for i in additional_schema] + [schema]
    refs = set()
    for schema in schemas:
        for name, field in getFieldsInOrder(schema):
            if isinstance(field, RichText):
                value = getattr(schema(obj), name)
                if not value or not getattr(value, 'raw', None):
                    continue
                refs |= set(getSnippetRefsFromHtml(value.raw))
    return refs


def modifiedDexterity(obj, event):
    """ a dexterity based object was modified """
    if not check_linkintegrity_dependencies(obj):
        return
    retriever = IRetriever(obj, None)
    if retriever is not None:
        links = retriever.retrieveLinks()
        refs = getObjectsFromLinks(obj, links)
        refs |= getSnippetRefs(obj)
        updateReferences(obj, refs)
