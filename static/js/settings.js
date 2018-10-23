
'use strict';

function updatePassword(evt) {
  evt.preventDefault();

  const dbInputs = {
    currentPassword: $("#currentpassword")[0].value,
    newPassword: $("#newpassword")[0].value,
    newPassword2: $("#newpassword2")[0].value
  };

  $.post('/update-password', dbInputs, function (results) {
    console.log(results);
  });

  $("#PasswordModal").modal('toggle');
}

// event listener on submit for update password form
$("form[name='password-form']").on("submit", updatePassword);
