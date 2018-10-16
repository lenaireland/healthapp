
'use strict';

function updateTrackedCondDesc() {
  const condition_form = $("#user_condition_form").get();
  const condition = {
    cond_id: condition_form[0][0].value
  };

  $.get('get-condition-desc', condition, function (results) {
    $("#user_condition_desc").html(results);
  });
}

// event listener called when the DOM is ready
$(document).ready(updateTrackedCondDesc);

// event listener on change for add new condition button
$("#user_condition_form").on("change", updateTrackedCondDesc);
