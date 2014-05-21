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

	$('.snippet-delete').click(function(e) {
		e.preventDefault();
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

		selectedSnippet = getSelectionElement();
		selectedSnippet.val(snippet);
		setSelected();
	}

	function getSelectionElement()
	{
		//We need to do this the "hard" way because, when returning from 
		//the snippet edit window, the t variable is nowhere to be found

		windows = tinyMCEPopup.editor.windowManager.windows

		for( value in windows ) {
			element = windows[value].element.get()
			frame = $(element).find('iframe')
			doc = $(frame).contents()
			if( $(doc).find('#snippet-selection').length >= 1 )
			{
				element = $(doc).find('#snippet-selection');
				return element;
			}
		}
	}
})
