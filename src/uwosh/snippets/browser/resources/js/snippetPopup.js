$(document).ready(function() {

	var snippets = $('.snippet');
	$(snippets).each(function() {
		var title = $(this).find('.snippet-title').text();
		var id = $(this).find('.snippet-id').text();
		$('#snippet-select').append('<option value="' + id + '">' + title + '</option>');
	})



	$('#snippet-select').change(function() {
		var selected = $('#snippet-select').find('option:selected').val();
		var id = '#snippet-' + selected;

		//We want to preserve all the formatting, so we use .html(), not .text()
		$('#snippet-preview').html(($(id).find('.snippet-text').html()));
	})

	$('#snippet-save').click(function() {
		var snippet = $('#snippet-select').find('option:selected').val();
		if( snippet != "None" )
		{
			tinyMCEPopup.editor.selection.setContent('!{{' + snippet + '}}!');
			tinyMCEPopup.close();
		}
		else if( snippet == "None" )
		{
			alert('You must select a snippet before saving.');
			$('#snippet-select').focus();
		}
	});

	$('#snippet-cancel').click(function() {
		tinyMCEPopup.close();
	})
});