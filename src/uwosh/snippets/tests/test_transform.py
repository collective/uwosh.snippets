# -*- coding: utf-8 -*-
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from uwosh.snippets.testing import BaseTest
from uwosh.snippets.testing import UWOSH_SNIPPETS_INTEGRATION_TESTING
from uwosh.snippets.transform import SnippetTransform
from zope.component import queryUtility


class TestTransform(BaseTest):

    layer = UWOSH_SNIPPETS_INTEGRATION_TESTING

    def _render_transform(self, page, header=''):
        self.request.response.setHeader('Content-Type', 'text/html')
        transform = SnippetTransform(self.portal, self.request)
        html = '''<html>
<body>
<div data-type="snippet_tag" data-snippet-id="{}" data-header="{}"></div>
</body>
</html>'''.format(IUUID(page), header)

        return ''.join(transform.transformIterable(html, None))

    def test_replace_tag(self):
        page = self._create_page()
        self.assertTrue('<p>foobar</p>' in self._render_transform(page))

    def test_should_include_container(self):
        page = self._create_page()
        self.assertTrue('snippet-container-document' in self._render_transform(page))

    def test_should_include_data_attributes_on_source(self):
        page = self._create_page()
        result = self._render_transform(page)
        self.assertTrue('data-source-uid="' + IUUID(page) in result)

    def test_customize_render_expression(self):
        registry = queryUtility(IRegistry)
        registry['uwosh.snippets.render_expression'] = u'context/Title'
        page = self._create_page()

        self.assertTrue('Test Snippet' in self._render_transform(page))

    def test_render_header(self):
        page = self._create_page(text='''
<h1>Foobar 1</h1>
<p>foobar 1</p>
<h1>Foobar 2</h1>
<p>foobar 2</p>
<h2>Foobar 3</h2>
<p>foobar 3</p>
<h1>Foobar 4</h1>
<p>foobar 4</p>
''')

        result = self._render_transform(page, 'Foobar 3')
        self.assertTrue('Foobar 1' not in result)
        self.assertTrue('Foobar 2' not in result)
        self.assertTrue('<h2>Foobar 3</h2>' in result)
        self.assertTrue('<p>foobar 3</p>' in result)
        self.assertTrue('Foobar 4' not in result)

    def test_render_header_nested(self):
        page = self._create_page(text='''
<h1>Foobar 1</h1>
<p>foobar 1</p>
<h1>Foobar 2</h1>
<p>foobar 2</p>
<h2>Foobar 3</h2>
<p>foobar 3</p>
<h3>Foobar 4</h3>
<p>foobar 4</p>
<h4>Foobar 5</h4>
<p>foobar 5</p>
<h3>Foobar 6</h3>
<p>foobar 6</p>
<h2>Foobar 7</h2>
<p>foobar 7</p>
''')

        result = self._render_transform(page, 'Foobar 3')
        self.assertTrue('Foobar 1' not in result)
        self.assertTrue('Foobar 2' not in result)
        self.assertTrue('<h2>Foobar 3</h2>' in result)
        self.assertTrue('<p>foobar 3</p>' in result)
        self.assertTrue('Foobar 4' in result)
        self.assertTrue('Foobar 5' in result)
        self.assertTrue('Foobar 6' in result)
        self.assertTrue('Foobar 7' not in result)
