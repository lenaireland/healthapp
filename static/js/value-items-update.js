
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
    let valueType = valueItem.innerText.split(" ")[0];

    if (valueType === "AQI:") {
      valueItem[1].value = "Get AirNOW AQI data";
    }

    $.get('/get-user-value-item', dbInputs, function (results) {
      if (results !== "False") {
        if (results !== "None") {
          valueItem[0].value = parseFloat(results, 10);
          valueItem[1].value = "Update Value";
        }
      }
    });
  }
}

function updateValue(evt) {
  evt.preventDefault();
  const valueId = evt.currentTarget.id;
  const valueType = evt.currentTarget.innerText.split(" ")[0];
  console.log(valueType);
  const value = evt.currentTarget.value.value;

  const dbInputs = getValueParams(valueId);

  if (valueType === "AQI:") {
    $.get('/airnow-api', dbInputs, function (results) {
      console.log(results);
      dbInputs.value = results;
    });
  } else {
    dbInputs.value = value;
  }
  
  $.post('/update-user-value-item', dbInputs, function (results) {
    console.log(results);
    evt.currentTarget.submit.value = "Update";
  });
}

// event listener called when the DOM is ready
$(document).ready(updateValueForms);

// event listener on click for any value form
$("form[name='valueform']").on("submit", updateValue);
