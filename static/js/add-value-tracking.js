
'use strict';

function updateValueDesc() {
  const value_form = $("#user_value_form").get();
  const value = {
    value_id: value_form[0][0].value
  };

  $.get('get-value-desc', value, function (results) {
    $("#value_desc").html(results);
  });
}

function addValue(evt) {
  evt.preventDefault();
  const condition_form = $("#user_condition_form").get();
  const value = {
    value_id: evt.currentTarget.values.value,
    usercond_id: condition_form[0][0].value
  };
  console.log(value);

  $.post('/add-user-value', value, function (results) {
    console.log(results);
  });
  // location.reload(true);
}

// event listener called when the DOM is ready
$(document).ready(updateValueDesc);

// event listener on change for dropdowns
$("#user_value_form").on("change", updateValueDesc);

// event listener on submit for add new condition button
$("#user_value_form").on("submit", addValue);
