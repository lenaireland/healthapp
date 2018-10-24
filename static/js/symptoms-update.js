
'use strict';


function getButtonParams(buttonId) {
  const params = buttonId.split(" ");

  let dbInputs = {
    user_symptom_id: parseInt(params[1], 10),
    date: params[2]
  };
  return dbInputs;
}

function updateSymptomButtons() {
  const symptomButtons = $("button[name='symptombutton']").get();

  for (let button of symptomButtons) {
    let buttonId = button.id;
    let dbInputs = getButtonParams(buttonId);

    $.get('/get-user-symptom', dbInputs, function (results) {
      if (results === "True") {
        button.innerText = "True";
      } else {
        button.innerText = "False";
      }
    });
  }
}

function updateSymptom(evt) {
  evt.preventDefault();
  const buttonId = evt.currentTarget.id;

  const dbInputs = getButtonParams(buttonId);

  if (evt.currentTarget.innerText === "True") {
    dbInputs.TF = false;
    $.post('/update-user-symptom', dbInputs, function (results) {
      console.log(results);
    });
    evt.currentTarget.innerText = "False";
  } else {
    dbInputs.TF = true;
    $.post('/update-user-symptom', dbInputs, function (results) {
      console.log(results);
    });
    evt.currentTarget.innerText = "True";
  }
}

// event listener called when the DOM is ready
$(document).ready(updateSymptomButtons);

// event listener on click for any symptom button
$("button[name='symptombutton']").on("click", updateSymptom);
