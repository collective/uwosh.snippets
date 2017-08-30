==============
uwosh.snippets
==============

Adds dynamically-updated rich text snippets to Plone. Update a 
snippet to display the change everywhere the snippet is used 
(pages, news items, events, anywhere rich text and TinyMCE 
appear).

Plone Version Compatibility
---------------------------

Version 2.x is compatible with Plone 5.0+

Earlier versions are compatible with Plone 4

Introduction
------------

The uwosh.snippets package allows you to include dynamically updated
rich text snippets (chunks of rich text) anywhere in your site that
uses the TinyMCE editor (i.e., any rich text field), including
Pages, News Items, and Events.

Snippets can be used anywhere that rich text can be used. They are
inserted into a page much like you would an image or hyperlink.

Because snippets are dynamically rendered, if you edit the snippet,
its updated rich text is shown everywhere you had inserted the
snippet.

This is much more efficient and less error prone than copying and
pasting rich text in multiple places in your site.

Example
-------

A university wants to display its number of enrolled students
consistently across its web site. Instead of manually updating each
page that mentions the number of enrolled students and having to
remember to change each of these pages whenever the enrollment number
changes (e.g. annually), a content editor would create a snippet
called "Enrollment Number" containing the rich text "13,491 students"
and would insert that snippet wherever the enrollment number needed to
be displayed.

Whenever the official enrollment number changes, the content editor
edits the "Enrollment Number" snippet to update the count,
e.g. "14,120 students", and saves the change. All subsequent views of
pages that contained that snippet will display the updated number.

How to use
----------

- Edit your buildout.cfg to add uwosh.snippets to your eggs.
- Run buildout.
- Restart your instance or clients.
- Go to Site Setup -> Add-ons
- Activate uwosh.snippets

A new folder called "Snippets" (with ID ".snippets") will be created
at the root of your site; that is the default location where the
add-on will look for snippets.

To add a snippet:

- Navigate to the Snippets folder.
- Add a Page. Give it a meaningful title and summary to
  help you and other content editors locate the snippet most
  easily. In the body, enter any rich text. You can use TinyMCE's
  Tools -> Source Code (HTML) view to insert arbitrarily complex HTML,
  as long as it satisfies your site's HTML Filtering settings.
- Click the Save button.

You have created your first snippet! You can use this snippet in one
or more places on your site, anywhere TinyMCE is used as the editor.

To insert a snippet:

- Add or edit a Page (or Event or News Item or any other content
  item that has a rich text field that uses the TinyMCE editor).
- In the TinyMCE editor, place your cursor where you will want to have
  the snippet's rich text appear.
- Click on TinyMCE's new "{{}}" toolbar icon to bring up the snippet
  search dialog, which by default looks in your site's Snippets
  folder.
- Use the search dialog to locate the snippet you want to
  insert. Click in the search dialog's text field. You will see a list
  of all snippets in your snippets folder. If you enter text in the
  search field, you will see only the snippets that match the search
  term you entered.
- Click on the snippet you want to insert. The Snippet Preview will
  show you the contents of the snippet you selected. Use the "Select
  section" drop down to choose the portion of the snippet you want to
  preview (this is useful if you have particularly long snippets).
- Click the Insert button. A reference to the snippet (a "plug") will
  be inserted into the rich text at the cursor location. It will look
  something like "Snippet:[ID=82341234bcda]".
- Click the Save button.

Instead of seeing the snippet plug you will now see the rich text
contents of the snippet.

Settings
--------

uwosh.snippets includes a control panel, available at Site Setup ->
Snippets ('@@snippets-controlpanel').

Related items settings:

- Use this to change the directory in which to look for snippets (by
  default, a folder with the ID `.snippets` and title `Snippets`). For
  example, to look for snippets in a folder with the ID `blabla` at
  the root of your site, change the value of `basePath` from `/.snippets` to `/blabla`.
- You can also modify the content type you use as snippets. By
  default, this is Pages (Documents). For example, to use the rich
  text field of a News Item, change the value of `selectableTypes`
  from `[Document]` to `[News Item]`.

Code display expression:

- Use this to modify the way a snippet reference ("plug") is displayed
  inside the TinyMCE editing area. Defaults to
  `string:Snippet:[ID=${context/@@uuid}]`. This is probably not a
  setting you will want to change.

Render expression:

- Use this to specify the TAL expression that renders a
  snippet. Defaults to
  `context/text/output|context/getText|nothing`. This is probably not
  a setting you will want to change. See the `TAL expression
  documentation
  <https://docs.plone.org/develop/plone/functionality/expressions.html>`_.

Notes
-----

If you want a snippet to be rendered without causing a line break
(because of the `p` tag that TinyMCE wraps around the rich text), edit
the snippet and, beneath the TinyMCE rich text editing area, use the
Text drop down and choose `text/x-web-textile`. Then manually remove
the `p` tag around the snippet's rich text and click Save. The rich
text will be saved without TinyMCE re-wrapping it with the `p` tag,
and when you use the snippet elsewhere it will not start a new
paragraph.

Requirements
------------

The TinyMCE WYSIWYG editor needs to be installed and enabled. A basic
understanding of its use is also highly recommended. For more
information about TinyMCE, visit their `website
<http://www.tinymce.com>`_.


TODO
----

- would be nice: re-add support for add/edit/delete snippets in the modal
- doesn't fit as well into how we're allowing snippets from anywhere on the site now
  
Credits
-------

The original concept was developed by Sam Schwartz for the Office of International Education at University of Wisconsin Oshkosh.

Plone 5 compatibility was developed by Nathan Van Gheem / Wildcard Corp. for Philip Bauer / Starzel.de.

Maintainers
-----------

This add-on is maintained by Wildcard Corp., https://wildcardcorp.com,
developers of the Castle CMS enhanced distribution of Plone,
https://castlecms.io
