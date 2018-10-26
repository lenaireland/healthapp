
'use strict';


// GET THIS FUNCTION TO SHOW FORMATTED RESULTS!!!
function displayResults(results, name) {
  console.log(name);

  let final_results = {};
  let nameResult;
  let out = '<ul>';

  for (let [queryItem, queryResult] of results) {
    if (queryItem === name) {
      console.log(queryResult);
      nameResult = queryResult;
      // console.log(nameValue);
    } else if (queryResult > 0) {
      out += '<li>' + queryItem + ' occurred ' + queryResult + ' times.</li>';
    }
  }

  out += '</ul>';

  console.log(final_results);
  $("#name").html(name);
  $("#nameResult").html("Occurred "+nameResult+" time(s)");
  $("#otherItems").html("Other tracked items that occurred on the same day"
                        + " (and how many times they occurred):");
  $("#listOutput").html(out);

  // let html = '<h3>{nameValue}</h3><p>Occurred {queryValue} times</p>';

  // $("#query_results").html(html);

  // $("#query_results").html(JSON.stringify(results));
}

function querySymptom(evt) {
  evt.preventDefault();

  const params = evt.currentTarget.symptoms.value.split(";");
  const name = params[0];
  console.log(name);

  const symptom = {
    symptom_id: params[1]
  };
  console.log(symptom);

  $.get('/query-user-symptom.json', symptom, function (results) {
    console.log(results);
    displayResults(results, name);
  });
}

// event listener on submit for symptom query
$("#user_symptom_query_form").on("submit", querySymptom);

function queryValue(evt) {
  evt.preventDefault();

  const params = evt.currentTarget.values.value.split(";");
  const name = params[0];
  console.log(name);

  const value = {
    value_id: params[1]
  };
  console.log(value);

  $.get('/query-user-value.json', value, function (results) {
    console.log(results);
    displayResults(results, name);
  });
}

// event listener on submit for value query
$("#user_value_query_form").on("submit", queryValue);

function queryCount(evt) {
  evt.preventDefault();

  const params = evt.currentTarget.counts.value.split(";");
  const name = params[0];
  console.log(name);

  const count = {
    count_id: params[1]
  };
  console.log(count);

  $.get('/query-user-count.json', count, function (results) {
    console.log(results);
    displayResults(results, name);
  });
}

// event listener on submit for count query
$("#user_count_query_form").on("submit", queryCount);
