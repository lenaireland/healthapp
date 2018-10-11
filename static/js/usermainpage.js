
'use strict';

function successFunction(results) {
  console.log(results);
}

function updateSymptom(evt) {
  evt.preventDefault();
  const buttonId = evt.currentTarget.id;
  console.log(buttonId);
  const params = buttonId.split(" ");

  let dbInputs = {
    symptom_id: parseInt(params[1]),
    date: params[2],
    TF: false
  };

  if (evt.currentTarget.innerText === "True") {
    dbInputs.TF = false;
    $.post('/update-user-symptom', dbInputs, successFunction);
    evt.currentTarget.innerText = "False";
  } else {
    dbInputs.TF = true;
    $.post('/update-user-symptom', dbInputs, successFunction);    
    evt.currentTarget.innerText = "True";
  }
}

$("button[name='symptombutton']").on("click", updateSymptom);
