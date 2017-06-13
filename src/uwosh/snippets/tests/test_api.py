# -*- coding: utf-8 -*-
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from uwosh.snippets.browser.api import SnippetsAPI
from uwosh.snippets.testing import BaseTest
from uwosh.snippets.testing import UWOSH_SNIPPETS_INTEGRATION_TESTING
from zope.component import queryUtility

import json


class TestAPI(BaseTest):

    layer = UWOSH_SNIPPETS_INTEGRATION_TESTING

    def test_get_code(self):
        page = self._create_page()
        self.request.form.update({
            'action': 'code',
            'uid': IUUID(page)
        })

        api_view = SnippetsAPI(page, self.request)

        self.assertEqual('Snippet:[ID={}]'.format(IUUID(page)),
                         json.loads(api_view())['result'])

    def test_get_code_custom_expression(self):
        registry = queryUtility(IRegistry)
        registry['uwosh.snippets.code_display_expression'] = u'string:foobar:[ID=${context/@@uuid}]'

        page = self._create_page()
        self.request.form.update({
            'action': 'code',
            'uid': IUUID(page)
        })

        api_view = SnippetsAPI(page, self.request)

        self.assertEqual('foobar:[ID={}]'.format(IUUID(page)),
                         json.loads(api_view())['result'])
