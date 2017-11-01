$(function() {
    $('#btnSignUp').click(function() {
 	console.log("This is working so far");
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                if(typeof response =='object'){
                    alert('User created successfully!')
                    window.location.href = '/';
                else
                    alert(response);
                
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
