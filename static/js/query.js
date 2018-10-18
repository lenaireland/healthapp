
'use strict';

// GET THIS FUNCTION TO SHOW FORMATTED RESULTS!!!
function displayResults(results) {
  $("#query_results").html(JSON.stringify(results));  
}

function querySymptom(evt) {
  evt.preventDefault();

  const symptom = {
    symptom_id: evt.currentTarget.symptoms.value
  };
  console.log(symptom);

  $.get('/query-user-symptom', symptom, function (results) {
    console.log(results);
    displayResults(results);
  });
  // location.reload(true);
}

// event listener on submit for add new condition button
$("#user_symptom_query_form").on("submit", querySymptom);

function queryValue(evt) {
  evt.preventDefault();

  const value = {
    value_id: evt.currentTarget.values.value
  };
  console.log(value);

  $.get('/query-user-value', value, function (results) {
    console.log(results);
    displayResults(results);
  });
  // location.reload(true);
}

// event listener on submit for add new condition button
$("#user_value_query_form").on("submit", queryValue);

function queryCount(evt) {
  evt.preventDefault();

  const count = {
    count_id: evt.currentTarget.counts.value
  };
  console.log(count);

  $.get('/query-user-count', count, function (results) {
    console.log(results);
    displayResults(results);
  });
  // location.reload(true);
}

// event listener on submit for add new condition button
$("#user_count_query_form").on("submit", queryCount);
