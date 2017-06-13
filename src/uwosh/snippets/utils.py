from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from lxml.html import fromstring
from lxml.html import tostring
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFCore.Expression import createExprContext
from Products.CMFCore.Expression import Expression
from zope.component import getUtility


class ExpressionEvaluator(object):

    def __init__(self):
        self.site = api.portal.get()

    def evaluate(self, expression, context, **kwargs):
        try:
            # Find folder (code courtesy of CMFCore.ActionsTool)
            if context is None or not hasattr(context, 'aq_base'):
                folder = self.site
            else:
                folder = context
                # Search up the containment hierarchy until we find an
                # object that claims it's PrincipiaFolderish.
                while folder is not None:
                    if getattr(aq_base(folder), 'isPrincipiaFolderish', 0):
                        # found it.
                        break
                    else:
                        folder = aq_parent(aq_inner(folder))

            __traceback_info__ = (folder, self.site, context, expression)
            ec = createExprContext(folder, self.site, context)
            # add 'context' as an alias for 'object'
            ec.setGlobal('context', context)
            ec.contexts.update({
                'context': context,
            })
            ec.contexts.update(kwargs)
            for name, val in kwargs.items():
                ec.setGlobal(name, val)
            return expression(ec)
        except AttributeError:
            pass


def render_snippet(ob, header=None):
    registry = getUtility(IRegistry)
    evaluator = ExpressionEvaluator()
    expression = Expression(registry.get('uwosh.snippets.render_expression',
                                         'context/text/output|context/getText|nothing'))
    result = evaluator.evaluate(expression, ob)
    if result and header:
        # need to find header in result
        result = get_header_from_text(result, header)
    return result


def get_header_from_text(text, header):
    dom = fromstring(text)
    result = []
    found = False
    for el in dom:
        tag = el.tag.lower()
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            if found == tag or found > tag:
                # found tag that is of equal or higher order than current tag
                # in python, comparing string h2 < h3 == true
                break
            if header.strip() == el.text_content().strip():
                found = tag
        if found:
            result.append(tostring(el))
    return '\n'.join(result)
