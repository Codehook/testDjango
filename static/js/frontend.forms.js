/**
 * These will execute on load
 */
$('#login-errors').hide();
$('#signup-errors').hide();

/**
 * Control how log in works
 */
$('#login').submit(function(event) {

    // Avoid a redirect
    event.preventDefault();

    // Ajax submit call
    $.ajax({
        dataType: 'json',             // Expecting JSON response
        data: $(this).serialize(),    // Send the form data
        type: $(this).attr('method'), // Get the form method
        url: $(this).attr('action'),  // Get the form action

        // This will execute if JSON is received
        success: function(form, status, jqxhr) {

            if(form.valid) {

                // Redirect the user on success
                window.location = '/d';

            } else {

                // Reset the signup form
                resetLoginForm();

                // Loop through the form errors
                for(field in form.errors) {

                    // Mark the field if an error exists
                    switch(field) {
                        case 'email':
                            $('#login-email').addClass('error');
                            break;
                        case 'password_two':
                            $('#login-password').addClass('error');
                            break;
                        case '__all__':
                            $('#login-email').addClass('error');
                            $('#login-password').addClass('error');
                            break;
                    }

                    // Add each error to the list
                    for(i = 0; i < form.errors[field].length; i++) {
                        $('#login-errors ul').append('<li>' + form.errors[field][i] + '</li>');
                    }

                    // Show the sign up errors
                    $('#login-errors').show();
                }
            }
        }
    });
});

/**
 * Control how sign up works
 */
$('#signup').submit(function(event) {

    // Avoid a redirect
    event.preventDefault();

    // Ajax submit call
    $.ajax({
        dataType: 'json',             // Expecting JSON response
        data: $(this).serialize(),    // Send the form data
        type: $(this).attr('method'), // Get the form method
        url: $(this).attr('action'),  // Get the form action

        // This will execute if JSON is received
        success: function(form, status, jqxhr) {

            if(form.valid) {

                // Redirect the user on success
                window.location = '/d';

            } else {

                // Reset the signup form
                resetSignupForm();

                // Loop through the form errors
                for(field in form.errors) {

                    // Mark the field if an error exists
                    switch(field) {
                        case 'first_name':
                            $('#signup-first-name').addClass('error');
                            break;
                        case 'last_name':
                            $('#signup-last-name').addClass('error');
                            break;
                        case 'username':
                            $('#signup-username').addClass('error');
                            break;
                        case 'email':
                            $('#signup-email').addClass('error');
                            break;
                        case 'password_two':
                            $('#signup-password-one').addClass('error');
                            $('#signup-password-two').addClass('error');
                            break;
                    }

                    // Add each error to the list
                    for(i = 0; i < form.errors[field].length; i++) {
                        $('#signup-errors ul').append('<li>' + form.errors[field][i] + '</li>');
                    }

                    // Show the sign up errors
                    $('#signup-errors').show();
                }
            }
        }
    });
});

/**
 * Reset the log in form
 */
function resetLoginForm() {
    // Reset all error indicators
    $('#login-email').removeClass('error');
    $('#login-password').removeClass('error');
    // Remove all error messages
    $('#login-errors ul').empty();
    $('#login-errors').hide();
}

/**
 * Reset the sign up form
 */
function resetSignupForm() {
    // Reset all error indicators
    $('#signup-first-name').removeClass('error');
    $('#signup-last-name').removeClass('error');
    $('#signup-username').removeClass('error');
    $('#signup-email').removeClass('error');
    $('#signup-password-one').removeClass('error');
    $('#signup-password-two').removeClass('error');
    // Remove all error messages
    $('#signup-errors ul').empty();
    $('#signup-errors').hide();
}

/**
 * Shows the log in modal
 */
function login() {
    $('#login').modal('show');
}

/**
 * Shows the sign up modal
 */
function signup() {
    $('#signup').modal('show');
}