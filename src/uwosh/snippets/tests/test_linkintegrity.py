# -*- coding: utf-8 -*-
from zope.annotation.interfaces import IAnnotations
from Products.statusmessages import STATUSMESSAGEKEY
from plone.app.textfield.value import RichTextValue
from plone.app.linkintegrity.utils import getIncomingLinks, getOutgoingLinks
from plone.uuid.interfaces import IUUID
from uwosh.snippets.linkintegrity import checkSnippetReferences
from uwosh.snippets.linkintegrity import getSnippetRefs
from uwosh.snippets.testing import BaseTest
from uwosh.snippets.testing import UWOSH_SNIPPETS_INTEGRATION_TESTING


class TestTransform(BaseTest):

    layer = UWOSH_SNIPPETS_INTEGRATION_TESTING

    def test_get_ref_form_snippet(self):
        page1 = self._create_page(_id='test1')
        page2 = self._create_page(
            text='<div data-type="snippet_tag" data-snippet-id="{}"</div>'.format(
                IUUID(page1)
            ))
        refs = getSnippetRefs(page2)
        self.assertEqual([i for i in refs][0].to_object.getId(), 'test1')
        # should also have stored these refs for object
        links = getOutgoingLinks(page2)
        self.assertEqual([l for l in links][0].to_object.getId(), 'test1')

    def test_breaking_header_links(self):
        page = self._create_page(_id='test1', text='''
<h1>Foobar 1</h1>
<p>foobar 1</p>
<h1>Foobar 2</h1>
<p>foobar 2</p>
<h2>Foobar 3</h2>
<p>foobar 3</p>
<h1>Foobar 4</h1>
<p>foobar 4</p>
''')
        page2 = self._create_page(_id='test2', text='''
<div data-type="snippet_tag"
     data-snippet-id="{}"
     data-header="Foobar 2"></div>'''.format(IUUID(page)))

        links = getOutgoingLinks(page2)  # should add link
        self.assertEqual([l for l in links][0].to_object.getId(), 'test1')
        links = getIncomingLinks(page)  # should add link
        self.assertEqual([l for l in links][0].from_object.getId(), 'test2')

        # now, remove the header...
        page.text = RichTextValue('''
<h1>Foobar 1</h1>
<p>foobar 1</p>
<h2>Foobar 3</h2>
<p>foobar 3</p>
<h1>Foobar 4</h1>
<p>foobar 4</p>
''', 'text/html', 'text/html')

        status_annotations = IAnnotations(self.request)
        self.assertFalse(bool(status_annotations.get(STATUSMESSAGEKEY)))

        checkSnippetReferences(page)

        self.assertTrue(bool(status_annotations.get(STATUSMESSAGEKEY)))
