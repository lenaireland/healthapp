
'use strict';


function getCountParams(countId) {
  const params = countId.split(" ");

  let dbInputs = {
    count_id: parseInt(params[1], 10),
    date: params[2]
  };
  return dbInputs;
}

function updateCountForms() {
  const countForms = $("form[name='countform']").get();

  for (let countItem of countForms) {
    let countId = countItem.id;
    let dbInputs = getCountParams(countId);

    $.get('/get-user-count-item', dbInputs, function (results) {
      if (results !== "False") {
        countItem[0].value = parseInt(results, 10);
        countItem[1].value = "Update";
      }
    });
  }
}

function updateCount(evt) {
  evt.preventDefault();
  const countId = evt.currentTarget.id;
  console.log(countId)
  const count = evt.currentTarget.count.value;

  console.log(count);
  console.log(countId);

  const dbInputs = getCountParams(countId);
  dbInputs.count = count;

  console.log(dbInputs);

  $.post('/update-user-count-item', dbInputs, function (results) {
    console.log(results);
  });
}

// event listener called when the DOM is ready
$(document).ready(updateCountForms);

// event listener on click for any count form
$("form[name='countform']").on("submit", updateCount);
