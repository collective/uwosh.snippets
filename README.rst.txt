.. raw::html

Introduction
============
The uwosh.snippets package allows the user to include dynamically updated rich-text snippets into a Plone page.
The snippets can be used anywhere that rich-text can be used. They can be inserted into a page much like 
a picture or hyperlink.

What is a snippet?
=================
Technically speaking, a snippet is just an ordinary bit of rich-text that can be shoe-horned into a Plone 
page wherever you like. However, unlike templates, copy/paste, or other similar methods, snippets are 
tied to an independent file, and then rendered when the page is rendered. This means that you can edit the snippet once, 
and the changes are reflected instantly on any page that it is "inserted" into. 

How to use
==========
Navigate to a pages edit view. Click somewhere inside the TinyMCE content window. The snippet
will be placed wherever the cursor is. If you highlight a block of text instead, the snippet
will replace whatever was highlighted.

In the TinyMCE toolbar, there should be a new button (looks like {{}} ). 
Click it, it will bring up a dialog box with options to create/browse/insert a snippet. Create 
a new snippet, and then click the Browse button to select it for insertion.

The Preview button will bring up an editable version of the page you're editing. 
In the preview window, you can insert several snippets at once, and see what it will
look like before saving it. 

Once you've inserted a snippet, you will see it in the TinyMCE edit window.
When you're editing a page, the snippets are denoted with a thin dotted border.
However, when the page is rendered normally, the border won't be there. 
While editing a page, if there is a snippet already embedded in the page 
(denoted with the dotted outline), you can click it to quickly bring up the snippet editor.
