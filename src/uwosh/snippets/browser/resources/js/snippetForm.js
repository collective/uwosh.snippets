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
		window.location.href = document.referrer;
	}

});