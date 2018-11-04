
'use strict';

function removeCount(evt) {
  evt.preventDefault();

  const count = {
    count_id: evt.currentTarget.counts.value
  };
  // console.log(count);

  $.post('/stop-user-count', count, function (results) {
    alert(results);
  });
  location.reload(true);
}

// event listener on submit for add new condition button
$("#user_count_stop_form").on("submit", removeCount);
