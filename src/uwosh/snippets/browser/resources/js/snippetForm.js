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

			var title = $($form).find('#form-widgets-title');
			title = encodeURI($(title).val());
			close(title);
		}
	});

	function close(title) {
		//window.location.href = document.referrer;
		var form = $('#snippetTitleForm');
		form.attr('action', document.referrer);
		$(form).find('input').val(title);
		form.submit();

	}

});