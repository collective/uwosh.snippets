# -*- coding: utf-8 -*-
import re
from string import replace
from uwosh.snippets.snippetmanager import SnippetManager


class SnippetParser():
    # The SnippetParser class handles the finding/replacing of snippets within a pages content.
    # The page content is passed to a Parser object, and it then tries to pattern match
    # the <span> tags used to represent snippets. If it finds a valid snippet tag,
    # it replaces it with the appropriate snippet text.

    def __init__(self):
        self.sm = SnippetManager()

    snippetRegex = '<span(?=[^>]*?data-type="snippet_tag"\s*)(?=[^>]*?data-snippet-id="([a-zA-Z0-9\s_-]+?)"\s*)[^>]+?>[^<>]*?<\/span>'  # noqa

    def parsePage(self, pageText):
        result = self.parseSnippets(pageText)

        return result

    def parseSnippets(self, pageText):
        pattern = re.compile(self.snippetRegex)
        matches = pattern.finditer(pageText)

        snippets = self.sm.getSnippets(True)
        rendered = {}
        matches = []
        for match in matches:
            replace_text = match.group(0)
            snippet_name = match.group(1)
            if replace_text in matches:
                continue
            try:
                if snippet_name not in rendered:
                    rendered[snippet_name] = snippets[snippet_name].getText()
                pageText = replace(pageText, replace_text, rendered[snippet_name])
                matches.append(replace_text)
            except KeyError:
                # The snippetID was invalid
                pageText = replace(pageText, match.group(0), '')

        return pageText
