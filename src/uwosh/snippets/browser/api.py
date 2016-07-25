from plone.app.uuid.utils import uuidToObject
from plone.registry.interfaces import IRegistry
from Products.CMFCore.Expression import Expression
from Products.Five import BrowserView
from uwosh.snippets.utils import ExpressionEvaluator
from uwosh.snippets.utils import render_snippet
from zope.component import getUtility

import json


class SnippetsAPI(BrowserView):
    """
    Web API
    """

    def __call__(self):
        self.request.response.setHeader('Content-type', 'application/json')

        action = self.request.form.get('action')
        if action == 'code':
            data = self.get_code()
        elif action == 'render':
            data = self.get_rendered()
        elif action == 'configuration':
            data = self.get_configuration()

        return json.dumps(data)

    def get_configuration(self):
        registry = getUtility(IRegistry)

        return {
            'relatedItemsOptions': registry.get('uwosh.snippets.related_items_options')
        }

    def get_rendered(self):
        uid = self.request.form.get('uid')
        ob = uuidToObject(uid)
        return {
            'success': True,
            'result': render_snippet(ob, header=self.request.form.get('header'))
        }

    def get_code(self):
        uid = self.request.form.get('uid')

        registry = getUtility(IRegistry)
        ob = uuidToObject(uid)
        evaluator = ExpressionEvaluator()
        expression = Expression(registry.get('uwosh.snippets.code_display_expression',
                                             'string:Snippet:[ID=${context/@@uuid}]'))

        header = self.request.form.get('header') or ''

        return {
            'success': True,
            'result': evaluator.evaluate(expression, ob, uid=uid, header=header)
        }
