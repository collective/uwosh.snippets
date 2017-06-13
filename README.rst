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
The uwosh.snippets package allows the user to include dynamically updated rich-text snippets
into a Plone page. The snippets can be used anywhere that rich-text can be used. They can be
inserted into a page much like a picture or hyperlink.

What is a snippet?
------------------
Technically speaking, a snippet is just an ordinary chunk of rich-text that can be repeatedly
inserted into a Plone page wherever you like. However, unlike templates, copy/paste, or other
similar methods, snippets are dynamic. Instead of a bunch of text that is dumped onto a page at
edit time, a snippet is simply a pointer to a single instance of text that is stored elsewhere.
Since the placeholders (referred to as "plugs") are being stored on the page, instead of the
text they represent, they never need to be updated. You simply just edit the snippet "definition"
and immediately the changes will be propagated everywhere that you have a plug in your website.

How to use
----------
In order to use the uwosh.snippets add-on, the TinyMCE WYSIWYG editor needs to be installed
and enabled. A basic understanding of its use is also highly recommended. For more information
about TinyMCE, visit their `website <http://www.tinymce.com>`_.


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

This add-on is maintained by Wildcard Corp., https://wildcardcorp.com, developers of the Castle CMS enhanced distribution of Plone, https://castlecms.io 
