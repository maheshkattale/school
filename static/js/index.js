$(".toggle-password").click(function () {

  $(this).toggleClass("fa-eye fa-eye-slash");
  var input = $($(this).attr("toggle"));
  if (input.attr("type") == "password") {
    input.attr("type", "text");
  } else {
    input.attr("type", "password");
  }
});

function IsValid(value) {
  value=value.trim();
  if (value == "" || value == null || value == undefined ) {
    return true;
  } else {
    return false;
  }
}

function password_validate(id) {
  var password = $('#' + id).val();
  var password_message = $('#' + id + '_error');
  var uppercaseRegex = /[A-Z]/;
  var specialCharRegex = /[!@#$%^&*()-_+=]/;
  var numberRegex = /[0-9]/;

  var valid = true;

  // Check if password has at least one uppercase letter
  if (!password.match(uppercaseRegex)) {
      valid = false;
      password_message.text('Password must contain at least one uppercase letter').show().delay(3000).slideUp();
      password_message.css('color', 'red');
  }

  // Check if password has at least one special character
  if (!password.match(specialCharRegex)) {
      valid = false;
      password_message.text('Password must contain at least one special character').show().delay(3000).slideUp();
      password_message.css('color', 'red');
  }

  // Check if password has at least one digit
  if (!password.match(numberRegex)) {
      valid = false;
      password_message.text('Password must contain at least one digit').show().delay(3000).slideUp();
      password_message.css('color', 'red');
  }

  // Check if password has minimum length of 8 characters
  if (password.length < 8) {
      valid = false;
      password_message.text('Password must have a minimum length of 8 characters').show().delay(3000).slideUp();
      password_message.css('color', 'red');
  }

  if (valid) {
      valid = true;

      // password_message.text('Password is strong and meets all requirements!').show().delay(3000).slideUp();
      // password_message.css('color', 'green');
  }
  return valid
}
function email_validate(id) {
  var email = $('#'+id).val();
  var email_message = $('#'+id+'_error');
  var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!emailRegex.test(email)) {
      email_message.html('Invalid email format. Please enter a valid email address.').show().delay(3000).slideUp();
      return false;
  }

  return true;
}
function mobile_validate(id) {
  var mobile = $('#'+id).val();
  var mobile_message = $('#'+id+'_error');
  var mobileRegex =/^[0-9]{10}$/;

  if (!mobileRegex.test(mobile)) {
      mobile_message.html(' Please enter a valid mobile number.').show().delay(3000).slideUp();
      return false;
  }

  return true;
}
