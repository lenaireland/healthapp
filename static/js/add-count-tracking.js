
'use strict';

function updateCountDesc() {
  const count_form = $("#user_count_form").get();
  const count = {
    count_id: count_form[0][0].value
  };

  $.get('get-count-desc', count, function (results) {
    $("#count_desc").html(results);
  });
}

function addCount(evt) {
  evt.preventDefault();
  const condition_form = $("#user_condition_form").get();
  const count = {
    count_id: evt.currentTarget.counts.value,
    usercond_id: condition_form[0][0].value
  };
  // console.log(count);

  $.post('/add-user-count', count, function (results) {
    alert(results);
  });
  location.reload(true);
}

// event listener called when the DOM is ready
$(document).ready(updateCountDesc);

// event listener on change for dropdowns
$("#user_count_form").on("change", updateCountDesc);

// event listener on submit for add new condition button
$("#user_count_form").on("submit", addCount);
