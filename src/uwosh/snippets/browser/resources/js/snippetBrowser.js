$(document).ready(function() {

	var t = tinyMCEPopup.getWindowArg('t');
	var setSelected = tinyMCEPopup.getWindowArg('setSelected');
	var selectedSnippet = $(t).find('#snippet-selection');
	var lastURL;

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
			selected = sanitize(selected);
			selectedSnippet.val(selected);

			var id = "#snippet-" + selected;
			setPreviewWindow(selected);
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

	$('.snippet-delete').click(function() {
		event.preventDefault();
		var url = $(this);
		tinyMCEPopup.editor.windowManager.confirm("Are you sure you want to delete this snippet?", function (s) {
			if(s)
			{
				$.ajax({
		            url: $(url).attr('href'),
		            success: function(data) {
		            	if( data == 'True' )
		            	{
		            		tinyMCEPopup.editor.windowManager.alert("The snippet was deleted successfully.");	
		            		$(url).parent().remove();
		            	}
		            	else
		            	{
		            		tinyMCEPopup.editor.windowManager.alert("Something when wrong. The snippet wasn't deleted: " + data);
		            	}
		            }
		        });
			}	
			else
			{
				return false;
			}
		});
	});

	function sanitize(snippetId) {
		snippet = snippetId.replace(/\./g, '\\.');
		snippet = snippet.replace(/\:/g, '\\:');

		return snippet;
	}

	function setPreviewWindow(snippet) {

		$(t).find('#snippet-selection').val($(snippet).find('.snippet-id').text());
		selectedSnippet.val(snippet);
		var selected = $(t).find('#snippet-' + snippet);
		setSelected(selected);
	}
})
