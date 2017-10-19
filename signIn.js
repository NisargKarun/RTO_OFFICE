$(function() {
    $('#btnSignIn').click(function() {
 	console.log("This is working so far");
        $.ajax({
            url: '/signIn',
            data: $('form').serialize(),
            type: 'GET',
            success: function(response) {
                console.log(response);
                if(typeof response =='object')
                    window.location.href = '/showMenuPage';
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
