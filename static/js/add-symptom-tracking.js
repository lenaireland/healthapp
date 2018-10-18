
'use strict';

function updateSymptomDesc() {
  const symptom_form = $("#user_symptom_form").get();
  const symptom = {
    symptom_id: symptom_form[0][0].value
  };

  $.get('get-symptom-desc', symptom, function (results) {
    $("#symptom_desc").html(results);
  });
}

function addSymptom(evt) {
  evt.preventDefault();
  const condition_form = $("#user_condition_form").get();
  const symptom = {
    symptom_id: evt.currentTarget.symptoms.value,
    usercond_id: condition_form[0][0].value
  };
  console.log(symptom);

  $.post('/add-user-symptom', symptom, function (results) {
    console.log(results);
  });
  location.reload(true);
}

// event listener called when the DOM is ready
$(document).ready(updateSymptomDesc);

// event listener on change for dropdowns
$("#user_symptom_form").on("change", updateSymptomDesc);

// event listener on submit for add new condition button
$("#user_symptom_form").on("submit", addSymptom);
