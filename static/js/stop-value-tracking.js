
'use strict';

function removeValue(evt) {
  evt.preventDefault();

  const value = {
    value_id: evt.currentTarget.values.value
  };
  console.log(value);

  $.post('/stop-user-value', value, function (results) {
    console.log(results);
  });
  location.reload(true);
}

// event listener on submit for add new condition button
$("#user_value_stop_form").on("submit", removeValue);
