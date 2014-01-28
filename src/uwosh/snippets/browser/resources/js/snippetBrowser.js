$(document).ready(function() {

	if( tinyMCEPopup.editor.selected_snippet != undefined )
	{
		var selected = $(':radio[value="' + tinyMCEPopup.editor.selected_snippet + '"]');
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
			tinyMCEPopup.editor.selected_snippet = selected;
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
})
