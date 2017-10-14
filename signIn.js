$(function() {
    $('#btnSignIn').click(function() {
 	console.log("This is working so far");
        $.ajax({
            url: '/signIn',
            data: $('form').serialize(),
            type: 'GET',
            success: function(response) {
                console.log(response);
                alert("user created successfully!");
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
