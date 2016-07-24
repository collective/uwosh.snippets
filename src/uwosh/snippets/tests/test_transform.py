# -*- coding: utf-8 -*-
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from uwosh.snippets.testing import BaseTest
from uwosh.snippets.testing import UWOSH_SNIPPETS_INTEGRATION_TESTING
from uwosh.snippets.transform import SnippetTransform
from zope.component import queryUtility


class TestTransform(BaseTest):

    layer = UWOSH_SNIPPETS_INTEGRATION_TESTING

    def _render_transform(self, page):
        self.request.response.setHeader('Content-Type', 'text/html')
        transform = SnippetTransform(self.portal, self.request)
        html = '''<html>
<body>
<div data-type="snippet_tag" data-snippet-id="{}"></div>
</body>
</html>'''.format(IUUID(page))

        return ''.join(transform.transformIterable(html, None))

    def test_replace_tag(self):
        page = self._create_page()
        self.assertTrue('<p>foobar</p>' in self._render_transform(page))

    def test_customize_render_expression(self):
        registry = queryUtility(IRegistry)
        registry['uwosh.snippets.render_expression'] = u'context/Title'
        page = self._create_page()

        self.assertTrue('Test Snippet' in self._render_transform(page))
