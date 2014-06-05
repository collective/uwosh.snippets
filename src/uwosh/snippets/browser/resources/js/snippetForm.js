$(document).ready(function() {

	$('#form-buttons-cancel').click(function(e) {
		e.preventDefault();
		close();
	});

	$('#form-buttons-save').click(function() {

		var options = {
			success:   successHandler, 
		};

		$('#form').ajaxForm(options);


		function successHandler(responseText, statusText, xhr, $form)
		{
			alert('The snippet was saved successfully!');
			close();
		}
	});

	function close() {

		//This means we're editing a snippet.
		//We only want to pass the title back if it's a new snippet
		if( $('#form-widgets-id').val().length > 0 )
		{
			window.location.href = document.referrer;
			return;
		}

		var id = $('#form-widgets-title').val();
		//Sanitize the id. It will be done again once it reaches the 
		//form class, in case this fails (or the JS is subverted).
		id = id.replace(/\W/g, '');

		var form = $('#snippetIdForm');
		form.attr('action', document.referrer);
		$(form).find('input').val(id);
		form.submit();
	}
});