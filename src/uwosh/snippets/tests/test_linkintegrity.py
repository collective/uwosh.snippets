# -*- coding: utf-8 -*-
from plone.app.linkintegrity.utils import getOutgoingLinks
from plone.uuid.interfaces import IUUID
from uwosh.snippets.testing import BaseTest
from uwosh.snippets.testing import UWOSH_SNIPPETS_INTEGRATION_TESTING
from uwosh.snippets.linkintegrity import getSnippetRefs


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
