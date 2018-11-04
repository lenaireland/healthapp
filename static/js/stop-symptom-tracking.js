
'use strict';

function removeSymptom(evt) {
  evt.preventDefault();

  const symptom = {
    symptom_id: evt.currentTarget.symptoms.value
  };
  // console.log(symptom);

  $.post('/stop-user-symptom', symptom, function (results) {
    alert(results);
  });
  location.reload(true);
}

// event listener on submit for add new condition button
$("#user_symptom_stop_form").on("submit", removeSymptom);
