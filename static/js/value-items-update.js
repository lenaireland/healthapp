
'use strict';


function getValueParams(valueId) {
  const params = valueId.split(" ");

  let dbInputs = {
    user_value_id: parseInt(params[1], 10),
    date: params[2]
  };
  return dbInputs;
}

function updateValueForms() {
  const valueForms = $("form[name='valueform']").get();

  for (let valueItem of valueForms) {
    let valueId = valueItem.id;
    let dbInputs = getValueParams(valueId);
    let valueType = valueItem.innerText.split(" ")[0];

    if (valueType === "AQI") {
      valueItem[1].value = "Get AirNOW AQI data";
    }

    $.get('/get-user-value-item', dbInputs, function (results) {
      if (results !== "False") {
        if (results !== "None") {
          valueItem[0].value = parseFloat(results, 10);
          if (valueType === "AQI") {
            valueItem[1].value = "Get AirNOW AQI Data";
          } else {
            valueItem[1].value = "Update Value";
          }
        }
      }
    });
  }
}

function updateValue(evt) {
  evt.preventDefault();
  const valueId = evt.currentTarget.id;
  const valueType = evt.currentTarget.innerText.split(" ")[0];

  const dbInputs = getValueParams(valueId);
  let value = evt.currentTarget.value.value;
  dbInputs.value = value;
  $.post('/update-user-value-item', dbInputs, function (results) {
    console.log(results);
    evt.currentTarget.submit.value = "Update";
  });
}

function defaultZip(evt) {
  evt.preventDefault();
  const target = evt.currentTarget;
  console.log(target);

  const valueForms = $("form[name='valueform']").get();

  for (let valueItem of valueForms) {
    let valueId = valueItem.id;
    let valueType = valueItem.innerText.split(" ")[0];

    if (valueType === "AQI") {
      const dbInputs = getValueParams(valueId);
      $.post('/update-airnow-item', dbInputs, function (results) {
        console.log(results);
        valueItem.value.value = results[0];
        valueItem.submit.value = "Get AirNOW AQI Data";
      });
    }
  }
  $("#AQIModal").modal('toggle');
}

function newZip(evt) {
  evt.preventDefault();
  const target = evt.currentTarget;
  console.log(target);
  console.log(target.newzip.value);

  const valueForms = $("form[name='valueform']").get();

  for (let valueItem of valueForms) {
    let valueId = valueItem.id;
    let valueType = valueItem.innerText.split(" ")[0];

    if (valueType === "AQI") {
      let dbInputs = getValueParams(valueId);
      dbInputs.zipcode = target.newzip.value;
      $.post('/update-airnow-item', dbInputs, function (results) {
        console.log(results);
        valueItem.value.value = results[0];
        valueItem.submit.value = "Get AirNOW AQI Data";
      });
    }
  }
  $("#AQIModal").modal('toggle');
}


// event listener called when the DOM is ready
$(document).ready(updateValueForms);

// event listener on click for any value form
$("form[name='valueform']").on("submit", updateValue);

$("#default-zip").on("click", defaultZip);

$("form[name='zip-form']").on("submit", newZip);
