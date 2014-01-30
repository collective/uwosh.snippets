$(document).ready(function() {

	var t = tinyMCEPopup.getWindowArg('t');
	var selectedSnippet = $(t).find('#snippet-selection');

	if( selectedSnippet.val() != "" )
	{
		var selected = $(':radio[value="' + selectedSnippet.val() + '"]');
		$(selected).attr('checked', true);
		$(selected).addClass('highlight');
	}

	var even = 1;
	$('.snippet-box').each(function(even) {
		if(even % 2 == 0)
		{
			$(this).addClass('even');
		}
		even += 1;
	});
	
	$('#snippet-browser-cancel').click(function() {
		tinyMCEPopup.close();
	});

	$('#snippet-browser-select').click(function() {

		var selected = $('input[name="snippet"]:checked').val();

		if( selected == undefined )
		{
			tinyMCEPopup.editor.windowManager.alert('You much choose a snippet to select.');
		}
		else
		{
			selectedSnippet.val(selected);

			var id = '#snippet-' + selected;
			var snippet = $(t).find(id);
			setPreviewWindow(snippet);
			tinyMCEPopup.close();
		}
	});

	$('.snippet-box').click(function() {

		$('.snippet-box').removeClass('highlight');
		$(this).find('input').attr('checked', true);
		$(this).addClass('highlight');
	});

	$('.snippet-box').mouseenter(function() {
		$(this).addClass('highlight');
	}).mouseleave(function() {
		if( $(this).find('input').attr('checked') )
		{
			return 0;
		}
		$(this).removeClass('highlight');
	});

	function setPreviewWindow(snippet) {


		if( $(t).find('#snippet-normal-buttons').css('display') != "none" )
		{
			//We want to preserve all the formatting, so we use .html(), not .text()
			$(t).find('#snippet-preview').html(snippet.find('.snippet-text').html());
		}

		$(t).find('#snippet-info-title').text(snippet.find('.snippet-title').text());
		
		var snippetDesc = snippet.find('.snippet-desc').text();
		var descText = "None";

		if( snippetDesc != "" )
		{
			descText = snippetDesc;
		}

		$(t).find('#snippet-info-desc').text(descText);
		
		$(t).find('#snippet-info').show();

	}
})
