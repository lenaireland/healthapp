
'use strict';

function removeCondition(evt) {
  evt.preventDefault();

  const condition = {
    cond_id: evt.currentTarget.conditions.value
  };
  console.log(condition);

  $.post('/stop-user-condition', condition, function (results) {
    console.log(results);
  });
  location.reload(true);
}

// event listener on submit for add new condition button
$("#user_condition_stop_form").on("submit", removeCondition);
