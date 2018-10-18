
'use strict';

function querySymptom(evt) {
  evt.preventDefault();

  const symptom = {
    symptom_id: evt.currentTarget.symptoms.value
  };
  console.log(symptom);

  $.get('/query-user-symptom', symptom, function (results) {
    console.log(results);
  });
  // location.reload(true);
}

// event listener on submit for add new condition button
$("#user_symptom_query_form").on("submit", querySymptom);
