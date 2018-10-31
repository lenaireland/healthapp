
'use strict';

// adapted example D3 code from
// https://bl.ocks.org/d3noob/402dd382a51a4f6eea487f9a35566de0
// and http://bl.ocks.org/d3noob/d8be922a10cb0b148cd5

// set the dimensions and margins of the graph
const margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// parse the date / time
const parseTime = d3.timeParse("%Y-%m-%d");

// set the ranges
const x = d3.scaleTime().range([0, width]);
const y = d3.scaleLinear().range([height, 0]);

// // Define the axes
// const xAxis = d3.svg.axis().scale(x)
//     .orient("bottom").ticks(5);

// const yAxis = d3.svg.axis().scale(y)
//     .orient("left").ticks(5);

// define the line
let valueline = d3.line()
  .x(function(d) { return x(d.date); })
  .y(function(d) { return y(d.value); });

// append the svg object to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin
let svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Get the data

$.get('get-value-timeseries.json', function (results) {

  // console.log(results);

// for list input
  results.forEach(function(d) {
    d.date = parseTime(d.date);
  });


  let nests = d3.nest()
    .key(function(d) {return d.name; })
    .entries(results);

// figure out how to do this in with .forEach instead

  let xMin=results[0].date;
  let xMax=results[0].date;
  let yMax=results[0].value;

  for (let result in results) {

    let data = results[result];

    if (yMax < data.value) {
      yMax = data.value;
    }

    if (xMax < data.date) {
      xMax= data.date;
    }

    if (xMin > data.date) {
      xMin= data.date;
    }
  }

  // Scale the range of the data   
  x.domain([xMin, xMax]);
  y.domain([0, yMax]);

  // Add the valueline path.
  nests.forEach(function(d) {
    svg.append("path")
       .attr("class", "line")
       .attr("d", valueline(d.values))
       .attr("fill", "none")
       .attr("stroke", "steelblue")
       .attr("stroke-width", 1.5);
  });

    // debugger;




  // // Scale the range of the data
  // let extents = ["date", "value"].map(function(name) {
  //   return d3.extent(results, function(d) {return d[name] });
  // });

  // // Scale the range of the data
  // x.domain(d3.extent(data, function(d) { return d.date; }));
  // y.domain([0, d3.max(data, function(d) { return d.value; })]);

  // Add the X Axis
  svg.append("g")
     .attr("class", "x axis")
     .attr("transform", "translate(0," + height + ")")
     .call(d3.axisBottom(x));

  // Add the Y Axis
  svg.append("g")
     .attr("class", "y axis")
     .call(d3.axisLeft(y));

});


// event listener called when the DOM is ready
$(document).ready($.get('get-symptom-timeseries.json', function (results) {
  console.log(results);
}));

// event listener called when the DOM is ready
$(document).ready($.get('get-value-timeseries.json', function (results) {
  console.log(results);
}));

// event listener called when the DOM is ready
$(document).ready($.get('get-count-timeseries.json', function (results) {
  console.log(results);
}));
