$(document).ready(function() {

	var snippets = $('.snippet');
	$(snippets).each(function() {
		var title = $(this).find('.snippet-title').text();
		var id = $(this).find('.snippet-id').text();
		$('#snippet-select').append('<option value="' + id + '">' + title + '</option>');
	});

	$('#snippet-select').change(function() {
		if( $('#snippet-normal-buttons').css('display') != "none" )
		{
			//We want to preserve all the formatting, so we use .html(), not .text()
			$('#snippet-preview').html(getSelectedSnippet().html());
		}
	});

	$('#snippet-insert').click(function() {
		insert();
		tinyMCEPopup.close();
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
		$('#snippet-preview').html(getSelectedSnippet().html());
	});

	$('#snippet-preview-insert').click(function() {
		if( $('#snippet-select').find('option:selected').val() != "None" )
		{
			var text = getSelectedSnippet();
			//grabs the actual DOM element. 
			text = $(text).clone().get(0);

			sel = window.getSelection();
			sel.deleteFromDocument();
			sel = sel.getRangeAt(0);
			sel.insertNode(text);
		}
	});

	function getSelectedSnippet() {
		var selected = $('#snippet-select').find('option:selected').val();
		var id = '#snippet-' + selected;

		return $(id).find('.snippet-text');
	}

	function insert() {
		var snippet = $('#snippet-select').find('option:selected').val();
		if( snippet != "None" )
		{
			tinyMCEPopup.editor.selection.setContent('!{{' + snippet + '}}!', {format: 'raw'});
		}
		else if( snippet == "None" )
		{
			alert('You must select a snippet before saving.');
			$('#snippet-select').focus();
		}
	}
});