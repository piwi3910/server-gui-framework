$(document).ready(function() {

        $("#fire_script").on('click', function (e) {
            $('#output').html("<code>Running</code>");
            console.log( $('#hash').val() );
            $.ajax( {
                url:'/results/',
                type: 'POST',
                data: {
                    "django_text": $('#hash').val(),
                    'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function(data) {
                    $('#newoutput').html(data.Value);
                    console.log(data.Value);
                    $('#output').html("<p>Not running</p>");
                },
                error: function(xhr,errmsg,err,data) {
                    $('#newoutput').html(data.Value);
                    console.log(data.Value);
                    $('#output').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console

                },
                traditional: true
            });
        e.preventDefault();
        });
});

