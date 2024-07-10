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
  if ( value == undefined ){
    return true;
  }
  value=value.trim();
  if (value == "" || value == null) {
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
function yyyy_mm_dd(dateString) {
  var parts = dateString.split("-");
  return parts[2] + "-" + parts[1] + "-" + parts[0];
}
function yyyy_mm_dd_to_dd_mm_yyyy(dateString) {
  var parts = dateString.split("-");
  return parts[2] + "-" + parts[1] + "-" + parts[0];
}
flatpickr(".date_picker", {
  dateFormat: "d-m-Y", // Customize date format if needed
  // You can add more configuration options here

});

flatpickr(".date_picker_upto_today", {
  dateFormat: "d-m-Y", // Customize date format if needed
  // You can add more configuration options here
  maxDate: "today" // Disable future dates

});
$('.select2').select2()
// In this function every menu which has an active link opens if a link is active. Its ul parent opens itself and adds the class 'open' to its parent (the arrow) so it turns 90 degrees
$('.pagenav li').each(function(i, el) {

  if ($(el).hasClass('selected')) {
    $(el).parent().show().parent().addClass('open');
  };
});

// This function ensures that a menu pops open when you click on it. All other menu's automatically close if the user clicks on a ul header. All the opened ul's close except the one clicked on
$('.accordion h4').click(function(event) {
  $('.accordion > ul > li > ul:visible').not($(this).nextAll('ul')).stop().hide(200).parent().removeClass('open'); //
  $(this).nextAll('ul').slideToggle(200, function() {
    $(this).parent('.pagenav').toggleClass('open');
  });
});

function check_new_notification_count(){
        

  $.ajax({
    type: "POST",
    url: frontend_url + "notifications/check_new_notification_count",
    data: {},
    success: function (response) {  
    console.log("notification",response)  
            
    if(response.response.n ==1){
      $('#notification_count').removeClass('d-none');
      $('#notification_count').html(response.data)  ;
    }else{
      $('#notification_count').html('')  ;
      $('#notification_count').addClass('d-none');
    }

        
    }
  });

}
function check_new_notification(){
        

  $.ajax({
    type: "POST",
    url: frontend_url + "notifications/check_new_notification",
    data: {},
    success: function (response) {  
    console.log("check_new_notification",response)  
    var lihtml='';  
    lihtml+=`
    <li>
        <a class="dropdown-item notification-header" href="#">Notifications</a>
    </li>
    ` 
    if(response.response.n ==1){
      $.each(response.data,function(i,o){
        var message_logo
        var message_class
        if(o.notification_type =='Message'){
          message_logo=frontend_url+'static/assets/images/backgrounds/message.png';
        }else{
          message_logo=frontend_url+'static/assets/images/backgrounds/speaker.jpg'
        }
        if(o.notification_read == false){
          message_class='unread_notification'
        }else{
          message_class='read_notification'
        }

        lihtml+=`
                <li>
                  <a class="dropdown-item p-2 `+message_class+`" href="#">
                    <div class="row m-0 p-0">
                      <div class="col-lg-2 p-0">
                        <div class="imgdiv">
                          <img class="w-100 imgclass" src="`+message_logo+`" alt="" />
                        </div>
                      </div>
                      <div class="col-lg-10 p-0">
                        <div class="notice-div p-0">
                          <div class="notice-title">`+o.from_user_name+` : `+o.notification_title+`</div>
                          <div class="notice-message">`+o.notification_message+`</div>
                          <div class="notification-notice-by pt-2">`+o.createdAt+`
                          </div>
                        </div>
                      </div>
                    </div>
                  </a>
                </li>
                `
      });

    }else{
          message_logo=frontend_url+'static/assets/images/backgrounds/blocked.jpg';

          lihtml=`
                  <li>
                    <a class="dropdown-item p-2" href="#">
                      <div class="row m-0 p-0">
                        <div class="col-lg-2 p-0">
                          <div class="imgdiv">
                            <img class="w-100 imgclass" src="`+message_logo+`" alt="" />
                          </div>
                        </div>
                        <div class="col-lg-10 p-0">
                          <div class="notice-div p-0">
                            <div class="notice-type">No Notification</div>
                            <div class="notice-message">No notification received yet</div>
                            <div class="notification-notice-by pt-2">
                            </div>
                          </div>
                        </div>
                      </div>
                    </a>
                  </li>
          `
    }
    lihtml+=`
    <li>
              <a class="dropdown-item notification-footer" href="/notifications/all_notifications">View All</a>
    </li>
    `
    $('#notification_popup').html(lihtml)

        
    }
  });

}