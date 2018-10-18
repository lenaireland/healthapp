
'use strict';

function queryValue(evt) {
  evt.preventDefault();

  const value = {
    value_id: evt.currentTarget.values.value
  };
  console.log(value);

  $.get('/query-user-value', value, function (results) {
    console.log(results);
  });
  // location.reload(true);
}

// event listener on submit for add new condition button
$("#user_value_query_form").on("submit", queryValue);
