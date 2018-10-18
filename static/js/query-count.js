
'use strict';

function queryCount(evt) {
  evt.preventDefault();

  const count = {
    count_id: evt.currentTarget.counts.value
  };
  console.log(count);

  $.get('/query-user-count', count, function (results) {
    console.log(results);
  });
  // location.reload(true);
}

// event listener on submit for add new condition button
$("#user_count_query_form").on("submit", queryCount);
