.. raw::html

==============
uwosh.snippets
==============

Plone Version Compatibility
---------------------------

Version 2.x is compatible with Plone 5.0+

Earlier versions are compatible with Plone 4

Introduction
------------

The uwosh.snippets package allows you to include dynamically updated
rich text snippets (chunks of rich text) anywhere in your site that
uses the TinyMCE editor (i.e., any rich text field), including
Documents (Pages), News Items, and Events.

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
- go to Site Setup -> Add-ons
- Install uwosh.snippets

A new folder called "Snippets" (with ID ".snippets") will be created
at the root of your site; that is the default location where the
add-on will look for snippets.

Navigate to the Snippets folder. Add a Document (Page); give it a
meaningful title and summary to help you and other content editors
locate the snippet most easily; in the body of the Document, enter any
rich text. You can use any TinyMCE formatting tools you wish, and you
can even use the HTML view to add and modify arbitrarily complex
HTML. Save the Document. You have created your first snippet! You can
use this snippet in one or more places on your site.

When you create or edit a Document ("Page"), TinyMCE will have a new
"{{}}" toolbar icon. When you click it, you will see a list of all
snippets found in the Snippets folder. When you click on a snippet, a
reference to it (a "plug") will be inserted into the rich text at the
cursor location. When you press Save, instead of seeing the snippet
plug you will see the rich text contents of the snippet.

Requirements
----------

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
