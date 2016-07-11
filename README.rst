.. raw::html

==============
uwosh.snippets
==============

(Plone 4.3+)

Introduction
------------
The uwosh.snippets package allows the user to include dynamically updated rich-text snippets into a Plone page.
The snippets can be used anywhere that rich-text can be used. They can be inserted into a page much like 
a picture or hyperlink.

What is a snippet?
------------------
Technically speaking, a snippet is just an ordinary chunk of rich-text that can be repeatedly inserted into a Plone page wherever you like. However, unlike templates, copy/paste, or other similar methods, snippets are dynamic. Instead of a bunch of text that is dumped onto a page at edit time, a snippet is simply a pointer to a single instance of text that is stored elsewhere. Since the placeholders (referred to as "plugs") are being stored on the page, instead of the text they represent, they never need to be updated. You simply just edit the snippet "definition" and immediately the changes will be propagated everywhere that you have a plug in your website.

Terminology:

Snippet definition
	The actual information that will be rendered onto the page. The snippet plugs are used as placeholders for their definitions during editing. 

Snippet plug
	The placeholder text that is placed into a page to represent its respective definition. Whenever a page containing a plug is rendered, the snippet parser will fetch the definition associated with that particular plug and place it into the page in place of the plug. The definition of a snippet can be edited, and the changes will be immediately reflected everywhere a plug is inserted. 

How to use
----------
In order to use the uwosh.snippets add-on, the TinyMCE WYSIWYG editor needs to be installed and enabled. A basic understanding of its use is also highly recommended. For more information about TinyMCE, visit their `website <http://www.tinymce.com>`_. 

Creating/adding/deleting/updating snippets can all be done through the snippet browser. To open the snippet browser, navigate to the "Edit" tab of any Plone page. In the TinyMCE editor, you should see a new button that looks like **{{}}**. Click it to open the snippet browser. Every one of the following steps will require opening the snippet browser at some point, so it's a good idea to make sure you know how to do this.

**Permission Issues:** In order to create/edit/delete snippet definitions, the current user account must have the proper permissions to do so. These permissions mirror the permissions to modify the .snippets folder (which is created in the site root when the add-on is installed). If the user can create a page (Document) in .snippets, they can create a new snippet definition. The same goes for deleting and editing.

**Usage**

- **Creating:** 
    To create a new snippet definition, open up the snippet browser. At the bottom of the snippet browser window, click on the link  "Create a new snippet.". An editor window will pop up allowing you to create a new snippet. Fill in the fields and click the "Save" button at the bottom. An alert box should appear, confirming that the snippet was created successfully.

- **Insertion:**
    When adding a new snippet to a page, it's first necessary to specify where it should be inserted. This is done by placing the cursor in the desired location in the text. The snippet browser will "paste" the snippet plug in this location.

    Next, open the snippet browser. Towards the top, in the "Selected Snippet" box, click the "Browse" button. A new window should appear containing a list of all existing snippets. Click on the desired snippet, and click the "Select" button towards the bottom left of the window. Now, click the "Insert" button at the bottom left of the snippet browser window.

    At this point, the window will close, and the snippet should be inserted at the cursor location. Snippets are shown with a small dotted border around them to make them more easily identifiable. Clicking inside this border will bring up the snippet browser again, with the clicked snippet already selected.

    **Note:** the page being edited still needs to be saved after inserting a snippet, otherwise no changes will be applied.

- **Editing:**
    To edit a snippet, open the snippet browser. Click the "Browse" button to bring up the snippet list. Locate the snippet in the list and click the "Edit" link directly to the right of the snippet description. An editor window will appear with the snippet's information filled in. Make the desired changes, and click the "Save" button. An alert will appear confirming that the changes have been successfully saved. The changes should now appear immediately everywhere the snippet has been inserted. No other changes are necessary.

- **Deleting:**
    **Beware:** Deleting a snippet will remove the snippet entirely, including any references to it. There is no way to reverse this. If you only want to remove a specific instance of a snippet, refer to the "Removing" section.

    To delete a snippet, open the snippet browser, and click the "Browse" button. Locate the desired snippet and click the "Delete" link directly to the right of the snippet description. Click "OK" to confirm the action.

- **Removing:**
    To remove a specific snippet plug from a page, click on the snippet in the TinyMCE editing window. When the snippet browser appears, click the "Remove" button. Click the "Cancel" button to close out of the snippet browser.

    **Note:** The page needs to be saved after removing a snippet for the changes to occur.

