
'use strict';

function updateNewCondDesc() {
  const condition_form = $("#new_condition_form").get();
  const condition = {
    cond_id: condition_form[0][0].value
  };

  $.get('get-condition-desc', condition, function (results) {
    $("#new_condition_desc").html(results);
  });
}

function addCondition(evt) {
  evt.preventDefault();
  const condition = {
    cond_id: evt.currentTarget.new_conditions.value
  };
  console.log(condition);

  $.post('/add-user-condition', condition, function (results) {
    console.log(results);
  });
  location.reload(true);
}

// event listener called when the DOM is ready
$(document).ready(updateNewCondDesc);

// event listener on change for dropdowns
$("#new_condition_form").on("change", updateNewCondDesc);

// event listener on submit for add new condition button
$("#new_condition_form").on("submit", addCondition);
