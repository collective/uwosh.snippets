from lxml.html import fromstring
from plone import api
from plone.app.linkintegrity.handlers import check_linkintegrity_dependencies
from plone.app.linkintegrity.handlers import getObjectsFromLinks
from plone.app.linkintegrity.handlers import updateReferences
from plone.app.linkintegrity.interfaces import IRetriever
from plone.app.linkintegrity.utils import getIncomingLinks
from plone.app.textfield import RichText
from plone.app.uuid.utils import uuidToObject
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import getAdditionalSchemata
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from Products.CMFCore.Expression import Expression
from uwosh.snippets.utils import ExpressionEvaluator
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.intid.interfaces import IIntIds
from zope.keyreference.interfaces import NotYet
from zope.schema import getFieldsInOrder


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


def findTextAreas(obj):
    fti = getUtility(IDexterityFTI, name=obj.portal_type)
    schema = fti.lookupSchema()
    additional_schema = getAdditionalSchemata(
        context=obj, portal_type=obj.portal_type)
    schemas = [i for i in additional_schema] + [schema]
    for schema in schemas:
        for name, field in getFieldsInOrder(schema):
            if isinstance(field, RichText):
                value = getattr(schema(obj), name)
                if not value or not getattr(value, 'raw', None):
                    continue
                yield value.raw


def getSnippetRefs(obj):
    refs = set()
    for text in findTextAreas(obj):
        refs |= set(getSnippetRefsFromHtml(text))
    return refs


def checkSnippetReferences(obj):
    """
    Checks if this content is a snippet on any other content.
    If it is, make sure the header setting is not ruined
    """
    registry = getUtility(IRegistry)
    evaluator = ExpressionEvaluator()
    expression = Expression(registry.get('uwosh.snippets.render_expression',
                                         'context/text/output|context/getText|nothing'))
    obj_headers = []
    html = evaluator.evaluate(expression, obj)
    if not html:
        return

    dom = fromstring(html)
    for el in dom.cssselect('h1,h2,h3,h4,h5,h6'):
        if el.text_content():
            obj_headers.append(el.text_content().strip())

    broken = []
    for link in getIncomingLinks(obj):
        for text in findTextAreas(link.from_object):
            if not text:
                continue

            dom = fromstring(text)
            for el in dom.cssselect('[data-snippet-id="{}"]'.format(IUUID(obj))):
                header = el.attrib.get('data-header')
                if not header:
                    continue
                if header not in obj_headers:
                    # broken reference
                    broken.append({
                        'header': header,
                        'link': link.from_object
                    })

    if len(broken) > 0:
        # show status message warning
        names = set()
        for b in broken:
            names.add('{}:{}'.format(b['link'].absolute_url(), b['header']))
        message = 'Broken snippet references: {}'.format(
            ', '.join(names)
        )
        api.portal.show_message(message=message, request=getRequest(), type='error')


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

    # now, check if THIS object is referenced by others and give user warning if there
    # are now missing headers that are referenced
    checkSnippetReferences(obj)
