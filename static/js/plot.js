
'use strict';

function makePlots() {

  // adapted example D3 code from
  // lecture notes
  // and https://bl.ocks.org/d3noob/402dd382a51a4f6eea487f9a35566de0
  // and http://bl.ocks.org/d3noob/d8be922a10cb0b148cd5
  // and http://www.d3noob.org/2014/07/d3js-multi-line-graph-with-automatic.html

  // set the dimensions and margins of the values graph
  let margin = {top: 20, right: 20, bottom: 70, left: 150};
  let width = 960 - margin.left - margin.right;
  let height = 500 - margin.top - margin.bottom;

  // set the dimensions and margins of the boxes graph
  let boxes_margin = {top: 20, right: 20, bottom: 70, left: 150};
  let boxes_width = 960 - boxes_margin.left - boxes_margin.right;
  let boxes_height = 1500 - boxes_margin.top - boxes_margin.bottom;

  // Get today's date
  const now = new Date();

  // parse the date / time
  const parseTime = d3.timeParse("%Y-%m-%d");

  // set the ranges
  const x = d3.scaleTime().range([0, width]);
  const y = d3.scaleLinear().range([height, 0]);

  const color = d3.scaleOrdinal(d3.schemeCategory10);
  // const colorScale = d3.scaleOrdinal(['pink', 'blue', 'orange', 'green']);

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

  let svg_boxes = d3.select("body").append("svg")
      .attr("width", boxes_width + boxes_margin.left + boxes_margin.right)
      .attr("height", boxes_height + boxes_margin.top + boxes_margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + boxes_margin.left + "," + boxes_margin.top + ")");


// to get first date user tracked
  let valueDateMin;
  let countDateMin;
  let sympDateMin;
  let dateMin;

  let sympNum = new Set();

  // Get the value data
  const getValueData = $.get('get-value-timeseries.json', function (results) {
    // for list input
    results.forEach(function(d) {
      d.date = parseTime(d.date);
    });

    valueDateMin = d3.min(results, function(d) { return d.date; });
  });

  // Get the symptom data
  const getSympData = $.get('get-symptom-timeseries.json', function (results) {
    // for list input
    results.forEach(function(d) {
      d.date = parseTime(d.date);
      sympNum.add(d.name);
    });

    sympDateMin = d3.min(results, function(d) { return d.date; });
  });

  // Get the count data
  const getCountData = $.get('get-count-timeseries.json', function (results) {
    // for list input
    results.forEach(function(d) {
      d.date = parseTime(d.date);
    });

    countDateMin = d3.min(results, function(d) { return d.date; });
  });

  // Get the overall min
  const getMin = function() {      
    dateMin = d3.min([valueDateMin, sympDateMin, countDateMin]);
  }

  const useData = function() {

    // for value data

    $.get('get-value-timeseries.json', function (results) {
      // for list input
      results.forEach(function(d) {
        d.date = parseTime(d.date);
      });

      // Scale the range of the data
      x.domain([dateMin, d3.timeDay(now)]);
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
          .attr("class", 'tag'+d.key.replace(/\s+/g, '')) // assign ID
          .attr("d", valueline(d.values))

        // Add the scatterplot
        svg_value.selectAll("dot")
            .data(d.values)
          .enter().append("circle")
            .attr("r", 3.5)
            .attr("class", 'tag'+d.key.replace(/\s+/g, '')) // assign ID      
            .attr("cx", function(d) { return x(d.date); })
            .attr("cy", function(d) { return y(d.value); })
            .style("fill", function() {
              return d.color = color(d.key); });

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
            d3.selectAll(".tag"+d.key.replace(/\s+/g, ''))
              .transition().duration(100)
              .style("opacity", newOpacity);
              // .style("fill", 'transparent');
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

    // // For symptom data

    $.get('get-symptom-timeseries.json', function (results) {
      // for list input
      results.forEach(function(d) {
        d.date = parseTime(d.date);
      });

      // Scale the range of the data
      x.domain([dateMin, d3.timeDay(now)]);

      // create data nest
      let sympDataNest = d3.nest()
        .key(function(d) {return d.name; })
        .entries(results);

      // parameters of data
      let xMax = d3.timeDay(now);
      let yNum = sympDataNest.length;

      let numDays = (xMax - dateMin)/1000/3600/24;

      let xScale = d3.scaleLinear()
                     .domain([dateMin, xMax])
                     .range([0, boxes_width]);

      let allDays = Array.from(Array(numDays + 1).keys());

      // create groups for each tracked item
      for (let y in Array.from(Array(yNum))) {
        svg_boxes.append('g')
          .attr("class", "Symp" + y);      
      }

      // loop through datanest
      sympDataNest.forEach(function(data, index) {

        svg_boxes.select(".Symp" + index)
          .data(data.values)
          .enter()

        // Add item name label
        svg_boxes.select(".Symp" + index).append('text')
          .attr('x', -100)
          .attr('y', (index * 35 + 17.5 ))
          .text((d) => d.name);

        // For each data entry, add a colored box to correct day
        data.values.forEach(function(d) {

          svg_boxes.select(".Symp" + index).append('rect')
            .attr('x', () => xScale(d.date) - (xScale(xMax)/numDays)/2)
            .attr('y', () => (index * 35))
            .attr("width", () => (xScale(xMax)/numDays))
            .attr("height", 25)
            .style('fill', () => color(d.name));
        })

        // For every day in range, add transparent box
        allDays.forEach(function(num) {

          svg_boxes.select(".Symp" + index).append('rect')
            .attr('x', () => xScale(xMax) / numDays * (num - 1/2) )
            .attr('y', () => (index * 35))
            .attr("width", () => (xScale(xMax)/numDays))
            .attr("height", 25)
            .style('fill', 'transparent')
            .style("stroke", 'black')
            .style("stroke-width", 0.5);

        });

      });

    });


    // // For count data

    $.get('get-count-timeseries.json', function (results) {
      // for list input
      results.forEach(function(d) {
        d.date = parseTime(d.date);
      });
      // Scale the range of the data
      x.domain([dateMin, d3.timeDay(now)]);

      // create data nest
      let countDataNest = d3.nest()
        .key(function(d) {return d.name; })
        .entries(results);

      // parameters for data
      let xMax = d3.timeDay(now);
      let yNum = countDataNest.length;

      let numDays = (xMax - dateMin)/1000/3600/24;

      let xScale = d3.scaleLinear()
                     .domain([dateMin, xMax])
                     .range([0, boxes_width]);

      let allDays = Array.from(Array(numDays + 1).keys());

      // create groups for each tracked item
      for (let y in Array.from(Array(yNum))) {
        svg_boxes.append('g')
          .attr("class", "Count" + y);      
      }

      // loop through datanest
      countDataNest.forEach(function(data, index) {

        svg_boxes.select(".Count" + index)
          .data(data.values)
          .enter();

        // Add item name label
        svg_boxes.select(".Count" + index).append('text')
          .attr('x', -100)
          .attr('y', ((sympNum.size + index) * 35 + 17.5))
          .text((d) => d.name);

        // For each data entry, add a colored box to correct day
        data.values.forEach(function(d) {          

          svg_boxes.select(".Count" + index).append('rect')
            .attr('x', () => xScale(d.date) - (xScale(xMax)/numDays)/2)
            .attr('y', () => ((sympNum.size + index) * 35))
            .attr("width", () => (xScale(xMax)/numDays))
            .attr("height", () => 25)
            .style('fill', () => color(d.name));

          svg_boxes.select(".Count" + index).append('text')
            .attr('x', () => (xScale(d.date) -4))
            .attr('y', () => ((sympNum.size + index) * 35 + 17.5))
            .text(() => d.count);
        });

        // For every day in range, add transparent box
        allDays.forEach(function(num) {

          svg_boxes.select(".Count" + index).append('rect')
            .attr('x', () => xScale(xMax) / numDays * (num - 1/2) )
            .attr('y', () => ((sympNum.size + index) * 35))
            .attr("width", () => (xScale(xMax)/numDays))
            .attr("height", 25)
            .style('fill', 'transparent')
            .style("stroke", 'black')
            .style("stroke-width", 0.5);

        });

      });

      // // Add the X Axis
      // svg_boxes.append("g")
      //    .attr("class", "x axis")
      //    .attr("transform", "translate(0," + height + ")")
      //    .call(d3.axisBottom(x));

      // // Add the Y Axis
      // svg_count.append("g")
      //    .attr("class", "y axis")
      //    .call(d3.axisLeft(y));
  });

  }

  // chained calls
  // would be nice to do value, symptom, and count together, then getMin, 
  // but this will do
  getValueData.always(getSympData)
              .always(getCountData)
              .always(getMin)
              .always(useData)

}

makePlots();
