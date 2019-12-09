$(document).ready(function() {
	$('#inputForm').on('submit', function(event) {
	    var input = $('#input').val().trim();
	    $("#input").css( "border", "2px solid gray" );
	    $("#output").css( "border", "2px solid gray" );
	    if (input.length > 0){
            $.ajax({
                data : {
                    input : $('#input').val()
                },
                type : 'POST',
                url : '/process'
            }).done(function(data) {
                $("#output").attr("readonly", false);
                $("#output").val(data.output);
                if (data.success == "True"){
                    $("#output").css( "border", "3px solid green" );
                }
                else{
                    $("#output").css( "border", "3px solid red" );
                }
                $("#output").attr("readonly", true);
            });
         }
         else{
            alert("வெண்பா உள்ளிடுக")
            $("#input").css( "border", "3px solid red" );
         }
		event.preventDefault();
	});
});