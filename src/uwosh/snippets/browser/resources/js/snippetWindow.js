$(document).ready(function() {

	document.title = 'Add a snippet';
	var t = $(this);

	var editor_snippet = tinyMCEPopup.getWindowArg('editor_snippet');

	if( editor_snippet != false )
	{
		$('#snippet-selection').val($(editor_snippet).attr('data-snippet-id'));
		setSelectedSnippet();
	}

	$('#snippet-insert').click(function() {
		var snippet = $('#snippet-selection').val();

		var text = getSelectedSnippet().find('.snippet-text').html();

		if( snippet != "None" )
		{
			output = createSpanTag(snippet, text);

			var editor_snippet = tinyMCEPopup.getWindowArg('editor_snippet');

			if( editor_snippet != false )
			{
				editor_snippet = catchNestedSpans(editor_snippet);
				$(editor_snippet).replaceWith(output);
				editor_snippet = false;
				tinyMCEPopup.close();
			}
			tinyMCEPopup.editor.selection.setContent(output, {format: 'raw'});
			tinyMCEPopup.close();
		}
		else if( snippet == undefined )
		{
			tinyMCEPopup.editor.windowManager.alert('You must select a snippet before saving.');
			$('#snippet-select').focus();
		}
	});

	$('#snippet-cancel').click(function() {

		tinyMCEPopup.close();
	});

	$('#snippet-view').click(function() {
		var body = tinyMCEPopup.editor.getDoc().body;
		$('#snippet-preview').html($(body).clone());
		$('#snippet-normal-buttons').hide();
		$('#snippet-preview-buttons').show();
	});

	$('#snippet-preview-cancel').click(function() {
		$('#snippet-normal-buttons').show();
		$('#snippet-preview-buttons').hide();
		$('#snippet-preview').html(getSelectedSnippet().find('.snippet-text').html());
	});

	$('#snippet-select').click(function() {
		var url = tinyMCEPopup.getWindowArg('current_url');
		var ed = tinyMCE.activeEditor;
		ed.windowManager.open({
			file: url + '/@@get-snippet-list?list-view=true',
			width : 800,
          	height : 600,
          	inline : 1

		}, {
			t: t,
			setSelected: setSelectedSnippet,
		});
	});

	$('#snippet-preview-insert').click(function() {
		if( $('#snippet-select').val() != "None" )
		{
			var text = getSelectedSnippet();
			var id = $(text).parent().find('.snippet-id').text();
			text = $(text).find('.snippet-text').text();

			var snippet = document.createElement('span');
			$(snippet).css('outline', "black dotted thin");
			$(snippet).css('display', 'inline-block');

			$(snippet).attr('data-type', 'snippet_tag');
			$(snippet).attr('data-snippet-id', id);

			$(snippet).text(text);

			var preview = $('#snippet-preview').get(0);

			var sel = window.getSelection();
			range = sel.getRangeAt(0);

			//makes sure the user selection is inside the 
			//preview window. Otherwise, the user could replace
			//text anywhere on the window. Chaos ensues.
			if( range.intersectsNode(preview) )
			{
				sel.deleteFromDocument();
				range.insertNode($(snippet).get(0));
			}
			else
			{
				tinyMCEPopup.editor.windowManager.alert('You must select select a location to insert the snippet.');
			}
		}
		else
		{
			tinyMCEPopup.editor.windowManager.alert("You must select a snippet to insert.");
			$('#snippet-select').focus();
		}
	});

	$('#snippet-preview-save').click(function() {

		var snippets = $('.snippet-wrapper');
		$(snippets).each(function() {
			var name = $(this).attr('snippet-id');

			var tag = createSpanTag(name);

			$(this).replaceWith(tag);
		});

		var body = $('#snippet-preview').html();
		tinyMCEPopup.editor.setContent(body);

		tinyMCEPopup.close();
	});

	function catchNestedSpans(plug) {

		//once in a while, the snippet-tag spans will
		//not get properly removed, so you'll have several nested 
		//inside one another. This function gets the
		//upper-most of the 'snippet-plug' spans and returns it.

		if( $(plug).parent().attr('data-type') == 'snippet_tag' )
		{
			plug = catchNestedSpans($(plug).parent());
		}

		return plug;
	}

	function createSpanTag(snippetId, snippetText)
	{
		if( snippetId != "" )
		{
			var style = "outline-style: dotted; outline-width: thin; outline-color: black; display: inline-block;";
			return '<span style="'+ style +'" data-type="snippet_tag" data-snippet-id="' + snippetId + '">' + snippetText + '</span>';
		}
	}

	function getSelectedSnippet() {
		var selected = $('#snippet-selection').val();
		var id = '#snippet-' + selected;

		return $(id);
	}

	function setSelectedSnippet(selected) {
		snippet = typeof(selected) != 'undefined' ? selected : getSelectedSnippet();

		if( $('#snippet-normal-buttons').css('display') != "none" )
		{
			//We want to preserve all the formatting, so we use .html(), not .text()
			$('#snippet-preview').html(snippet.find('.snippet-text').html());
		}

		$('#snippet-info-title').text(snippet.find('.snippet-title').text());
		
		var snippetDesc = snippet.find('.snippet-desc').text();
		var descText = "None";

		if( snippetDesc != "" )
		{
			descText = snippetDesc;
		}

		$('#snippet-info-desc').text(descText);
		
		$('#snippet-info').show();
	}
});