
'use strict';

// adapted example D3 code from
// https://bl.ocks.org/d3noob/402dd382a51a4f6eea487f9a35566de0
// and http://bl.ocks.org/d3noob/d8be922a10cb0b148cd5
// and http://www.d3noob.org/2014/07/d3js-multi-line-graph-with-automatic.html

// set the dimensions and margins of the graph
const margin = {top: 20, right: 20, bottom: 70, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// Get today's date
const now = new Date();

// parse the date / time
const parseTime = d3.timeParse("%Y-%m-%d");

// set the ranges
const x = d3.scaleTime().range([0, width]);
const y = d3.scaleLinear().range([height, 0]);

const color = d3.scaleOrdinal(d3.schemeCategory10);

// define the line
let valueline = d3.line()
  .x(function(d) { return x(d.date); })
  .y(function(d) { return y(d.value); });

// append the svg object to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin
let svg_value = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

let svg_count = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Get the value data
$.get('get-value-timeseries.json', function (results) {

  // for list input
  results.forEach(function(d) {
    d.date = parseTime(d.date);
  });

  // Scale the range of the data
  x.domain([d3.min(results, function(d) { return d.date; }), d3.timeDay(now)]);
  y.domain([0, d3.max(results, function(d) { return d.value; })]);

  // let xMin = results[0].date;
  // let xMax = results[0].date;
  // let yMax = results[0].value;

  // results.forEach(function(d) {
  //   if (yMax < d.value) {
  //     yMax = d.value;
  //   }
  //   if (xMax < d.date) {
  //     xMax = d.date;
  //   }
  //   if (xMin > d.date) {
  //     xMin = d.date;
  //   }
  // });

  // // Scale the range of the data
  // x.domain([xMin, xMax]);
  // y.domain([0, yMax]);

  // create data nest
  let valueDataNest = d3.nest()
    .key(function(d) {return d.name; })
    .entries(results);

  const legendSpace = width/valueDataNest.length;

  // Loop through each symbol/key
  valueDataNest.forEach(function(d,i) {

    // Add the valueline path.
    svg_value.append("path")
      .attr("class", "line")
      .style("stroke", function() {
        return d.color = color(d.key); })
      .attr("id", 'tag'+d.key.replace(/\s+/g, '')) // assign ID
      .attr("d", valueline(d.values))
      // .attr("fill", "none")
      // .attr("stroke", "steelblue")
      // .attr("stroke-width", 1.5);

    // Add the legend
    svg_value.append("text")            
      .attr("x", (legendSpace/2)+i*legendSpace)
      .attr("y", height + (margin.bottom/2)+ 5)
      .attr("class", "legend")
      .style("fill", function() {
        return d.color = color(d.key); })
      .on("click", function() {
        // Determine if current line is visibile
        let active = d.active ? false : true;
        let newOpacity = active ? 0 : 1;
        // Hide or show elements based on ID
        d3.select("#tag"+d.key.replace(/\s+/g, ''))
          .transition().duration(100)
          .style("opacity", newOpacity);
        // Update whether or not the elements are active
        d.active = active;
      })
      .text(d.key);
  });

  // Add the X Axis
  svg_value.append("g")
     .attr("class", "x axis")
     .attr("transform", "translate(0," + height + ")")
     .call(d3.axisBottom(x));

  // Add the Y Axis
  svg_value.append("g")
     .attr("class", "y axis")
     .call(d3.axisLeft(y));

});


// Get the count data
$.get('get-count-timeseries.json', function (results) {

  // for list input
  results.forEach(function(d) {
    d.date = parseTime(d.date);
  });

  const colorDomain = d3.extent(results, function(d) { return d.date; });

  const colorScale = d3.scaleLinear()
    .domain(colorDomain)
    .range(["lightblue", "blue"]);

  // create data nest
  let countDataNest = d3.nest()
    .key(function(d) {return d.name; })
    .entries(results);

  let xMin = d3.min(results, function(d) {return d.date});

  let rectangles = svg_count.selectAll("rect")
      .data(results)
      .enter()
      .append("rect")
    //       .attr("x", function(d){ return ((d.date - xMin) * 50); })
    // .attr("y", 50)
    // .attr("width", 50)
    // .attr("height", 50)
    // .style("fill", function(d){
    //   return colorScale(d.count);
    // }); 

  countDataNest.forEach(function(data, index) {
    console.log(data);
    console.log(index);

    rectangles
    .attr("x", function(d){ return ((d.date - xMin) * 50); })
    .attr("y", function(d){ return index * 50; })
    .attr("width", 50)
    .attr("height", 50)
    .style("fill", function(d){
      return colorScale(d.count);
    });  
  })

  // Scale the range of the data
  x.domain([d3.min(results, function(d) { return d.date; }), d3.timeDay(now)]);
  // y.domain([0, d3.max(results, function(d) { return d.value; })]);

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
