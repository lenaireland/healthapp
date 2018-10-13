
'use strict';


function getValueParams(valueId) {
  const params = valueId.split(" ");

  let dbInputs = {
    value_id: parseInt(params[1], 10),
    date: params[2]
  };
  return dbInputs;
}

function updateValueForms() {
  const valueForms = $("form[name='valueform']").get();

  for (let valueItem of valueForms) {
    let valueId = valueItem.id;
    let dbInputs = getValueParams(valueId);

    $.get('/get-user-value-item', dbInputs, function (results) {
      if (results !== "False") {
        valueItem[0].value = parseInt(results, 10);
        valueItem[1].value = "Update Value";
      }
    });
  }
}

// TO DO: GET THIS WORKING!!!!!!!!!!
function updateValue(evt) {
  evt.preventDefault();
  const valueId = evt.currentTarget.id;
  console.log(valueId);

  const dbInputs = getButtonParams(valueId);

  console.log(dbInputs);

  $.post('/update-user-value-item', dbInputs, function (results) {
    console.log(results);
  });




  //   evt.currentTarget.innerText = "False";
  // } else {
  //   dbInputs.TF = true;
  //   $.post('/update-user-symptom', dbInputs, function (results) {
  //     console.log(results);
  //   });
  //   evt.currentTarget.innerText = "True";
  // }
}

// event listener called when the DOM is ready
$(document).ready(updateValueForms);

// event listener on click for any value form
$("form[name='valueform']").on("submit", updateValue);
