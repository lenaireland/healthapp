3.
'use strict';

// adapted example D3 code from
// https://bl.ocks.org/d3noob/402dd382a51a4f6eea487f9a35566de0
// and http://bl.ocks.org/d3noob/d8be922a10cb0b148cd5
// and http://www.d3noob.org/2014/07/d3js-multi-line-graph-with-automatic.html

// set the dimensions and margins of the graph
const margin = {top: 20, right: 20, bottom: 70, left: 100},
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

let svg_symp = d3.select("body").append("svg")
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

let valueResults;
let countResults;

let dateMax;
let dateMin;


// Get the value data
$.get('get-value-timeseries.json', function (results) {

  // for list input
  results.forEach(function(d) {
    d.date = parseTime(d.date);
  });

  // Scale the range of the data
  x.domain([d3.min(results, function(d) { return d.date; }), d3.timeDay(now)]);
  y.domain([0, d3.max(results, function(d) { return d.value; })]);

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

// Get the symptom data
$.get('get-symptom-timeseries.json', function (results) {

  // for list input
  results.forEach(function(d) {
    d.date = parseTime(d.date);
  });

  // Scale the range of the data
  x.domain([d3.min(results, function(d) { return d.date; }), d3.timeDay(now)]);
  // y.domain([0, d3.max(results, function(d) { return d.count; })]);


  const colorDomain = d3.extent(results, function(d) { return d.date; });

  let colorScale = d3.scaleOrdinal(['pink', 'blue', 'orange', 'green']);

  // const colorScale = d3.scaleLinear()
  //   .domain(colorDomain)
  //   .range(["lightblue", "blue"]);

  // create data nest
  let countDataNest = d3.nest()
    .key(function(d) {return d.name; })
    .entries(results);

  let xMin = d3.min(results, function(d) {return d.date});
  let xMax = d3.max(results, function(d) {return d.date});
  let yNum = countDataNest.length;

  let numDays = (xMax - xMin)/1000/3600/24;

  let xScale = d3.scaleLinear()
                 .domain([xMin, xMax])
                 .range([0, 800]);

  let yScale = d3.scaleLinear()
                 .domain([0, yNum])
                 .range([0, 400]);

  allDays = Array.from(Array(numDays + 1).keys());


  countDataNest.forEach(function(data, index) {
    console.log(data);
    console.log(index);
    console.log(data.key);

    // let label = svg_count.selectAll("labels")
    //   .data(data)
    //   .enter()
    //   .append('g')
    //   .attr("class", "name");

    // label.append('name')
    //   .attr('x', -150)
    //   .attr('y', (d) => (100 * index+25))
    //   .text((d) => d.key);

    let boxes = svg_symp.selectAll("eachCount")
      .data(data.values)
      .enter()
      .append('g')
      .attr("class", "rect");

    boxes.append('rect')
      .attr('x', (d) => xScale(d.date))
      .attr('y', () => yScale(index))
      .attr("width", () => (xScale(xMax)/numDays))
      .attr("height", () => (xScale(xMax)/numDays))
      .style('fill', (d) => colorScale(d.name));

    boxes.append('text')
      .attr('x', (d) => (xScale(d.date) + (xScale(xMax)/numDays/2) ))
      .attr('y', () => (yScale(index) + (xScale(xMax)/numDays/2) ))
      .text((d) => d.count);

    allDays.forEach(function(num) {

      let empty_boxes = svg_symp.selectAll("eachCount")
        .data(data.values)
        .enter()
        .append('g')
        .attr("class", "rect");

      empty_boxes.append('rect')
        .attr('x', () => xScale(xMax)/numDays*num )
        .attr('y', () => yScale(index))
        .attr("width", () => (xScale(xMax)/numDays))
        .attr("height", () => (xScale(xMax)/numDays))
        .style('fill', 'transparent')
        .style("stroke", 'black')
        .style("stroke-width", 0.5);

      empty_boxes.append('text')
        .attr('x', -100)
        .attr('y', (yScale(index) + (xScale(xMax)/numDays/2)))
        .text((d) => d.name);
    })

  });


  // Add the X Axis
  svg_symp.append("g")
     .attr("class", "x axis")
     .attr("transform", "translate(0," + height + ")")
     .call(d3.axisBottom(x));
});


// Get the count data
$.get('get-count-timeseries.json', function (results) {

  // for list input
  results.forEach(function(d) {
    d.date = parseTime(d.date);
  });

  // Scale the range of the data
  x.domain([d3.min(results, function(d) { return d.date; }), d3.timeDay(now)]);
  // y.domain([0, d3.max(results, function(d) { return d.count; })]);


  const colorDomain = d3.extent(results, function(d) { return d.date; });

  let colorScale = d3.scaleOrdinal(['pink', 'blue', 'orange', 'green']);

  // const colorScale = d3.scaleLinear()
  //   .domain(colorDomain)
  //   .range(["lightblue", "blue"]);

  // create data nest
  let countDataNest = d3.nest()
    .key(function(d) {return d.name; })
    .entries(results);

  let xMin = d3.min(results, function(d) {return d.date});
  let xMax = d3.max(results, function(d) {return d.date});
  let yNum = countDataNest.length;

  let numDays = (xMax - xMin)/1000/3600/24;

  let xScale = d3.scaleLinear()
                 .domain([xMin, xMax])
                 .range([0, 800]);

  let yScale = d3.scaleLinear()
                 .domain([0, yNum])
                 .range([0, 400]);

  allDays = Array.from(Array(numDays + 1).keys());


  countDataNest.forEach(function(data, index) {
    console.log(data);
    console.log(index);
    console.log(data.key);

    // let label = svg_count.selectAll("labels")
    //   .data(data)
    //   .enter()
    //   .append('g')
    //   .attr("class", "name");

    // label.append('name')
    //   .attr('x', -150)
    //   .attr('y', (d) => (100 * index+25))
    //   .text((d) => d.key);

    let boxes = svg_count.selectAll("eachCount")
      .data(data.values)
      .enter()
      .append('g')
      .attr("class", "rect");

    boxes.append('rect')
      .attr('x', (d) => xScale(d.date))
      .attr('y', () => yScale(index))
      .attr("width", () => (xScale(xMax)/numDays))
      .attr("height", () => (xScale(xMax)/numDays))
      .style('fill', (d) => colorScale(d.name));

    boxes.append('text')
      .attr('x', (d) => (xScale(d.date) + (xScale(xMax)/numDays/2) ))
      .attr('y', () => (yScale(index) + (xScale(xMax)/numDays/2) ))
      .text((d) => d.count);

    allDays.forEach(function(num) {

      let empty_boxes = svg_count.selectAll("eachCount")
        .data(data.values)
        .enter()
        .append('g')
        .attr("class", "rect");

      empty_boxes.append('rect')
        .attr('x', () => xScale(xMax)/numDays*num )
        .attr('y', () => yScale(index))
        .attr("width", () => (xScale(xMax)/numDays))
        .attr("height", () => (xScale(xMax)/numDays))
        .style('fill', 'transparent')
        .style("stroke", 'black')
        .style("stroke-width", 0.5);

      empty_boxes.append('text')
        .attr('x', -100)
        .attr('y', (yScale(index) + (xScale(xMax)/numDays/2)))
        .text((d) => d.name);
    })

  });


  // Add the X Axis
  svg_count.append("g")
     .attr("class", "x axis")
     .attr("transform", "translate(0," + height + ")")
     .call(d3.axisBottom(x));

  // // Add the Y Axis
  // svg_count.append("g")
  //    .attr("class", "y axis")
  //    .call(d3.axisLeft(y));

});




// // event listener called when the DOM is ready
// $(document).ready($.get('get-symptom-timeseries.json', function (results) {
//   console.log(results);
// }));

// // event listener called when the DOM is ready
// $(document).ready($.get('get-value-timeseries.json', function (results) {
//   console.log(results);
// }));

// // event listener called when the DOM is ready
// $(document).ready($.get('get-count-timeseries.json', function (results) {
//   console.log(results);
// }));
