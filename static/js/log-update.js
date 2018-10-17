
'use strict';

function getLogParams(id) {
  const params = id.split(" ");

  let dbInputs = {
    date: params[1]
  };
  return dbInputs;
}

function updateLogText() {
  const logForm = $("form[name='dailylog']").get();

  const id = logForm[0].id;
  let dbInputs = getLogParams(id);

  $.get('/get-user-log', dbInputs, function (results) {
    if (results !== "False") {
      if (results !== "None") {
        logForm[0][0].value = results;
        logForm[0][1].value = "Update";
      }
    }
  });
}

function saveLogText(evt) {
  evt.preventDefault();
  const id = evt.currentTarget.id;
  const text = evt.currentTarget.dailylogtext.value;

  const dbInputs = getLogParams(id);
  dbInputs.text = text;

  $.post('/update-user-log', dbInputs, function (results) {
    console.log(results);
    evt.currentTarget.submit.value = "Update";
  });
}

// event listener called when the DOM is ready
$(document).ready(updateLogText);

// event listener on click for any value form
$("form[name='dailylog']").on("submit", saveLogText);
