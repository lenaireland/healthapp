
'use strict';

chart = {
  // const svg = d3.select(DOM.svg(width, height));
  const svg = d3.select("svg")
  // const svg = d3.select("body").append("svg")
                .attr("width", width)
                .attr("height", height)

  svg.append("g")
      .call(xAxis);

  svg.append("g")
      .call(yAxis);
  
  svg.append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("d", line);
  
  return svg.node();
}

height = 500
// width = 842

margin = ({top: 20, right: 30, bottom: 30, left: 40})

x = d3.scaleTime()
    .domain(d3.extent(data, d => d.date))
    .range([margin.left, width - margin.right])

y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)]).nice()
    .range([height - margin.bottom, margin.top])

xAxis = g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0))

yAxis = g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y))
    .call(g => g.select(".domain").remove())
    .call(g => g.select(".tick:last-of-type text").clone()
        .attr("x", 3)
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .text(data.y))

line = d3.line()
    .defined(d => !isNaN(d.value))
    .x(d => x(d.date))
    .y(d => y(d.value))

let data;

$.get('get-value-timeseries.json', function (results) {
  console.log(results);
  for (let result in results) {
    // console.log(results[result]);
    if (result === 'AQI') {
      data = results[result];
      console.log(data);
    }
  }
});

d3 = require("d3@5")


// function drawChart(data) {

//   const svgWidth = 960, svgHeight = 500
//   const margin = { top:20, right: 20, bottom: 30, left: 50}
//   const width = svgWidth - margin.left - margin.right;
//   const height = svgHeight - margin.top - margin.bottom;

//   const svg = d3.select('svg')
//     .attr("width", svgWidth)
//     .attr("height", svgHeight)
// }


// // event listener called when the DOM is ready
// $(document).ready($.get('get-value-timeseries.json', function (results) {
//   console.log(results)
//   let data;

//   // parse the date / time
//   const parseTime = d3.timeParse("%Y-%m-%d");

//   for (let result in results) {
//     console.log(results[result]);

//     if (result === 'AQI') {
//       data = results[result];
//       console.log(data); 

//       .then(function (data) {
//         data.forEach(function(d) {
//           d.date = parseTime(d.date)
//         });
//         drawChart(data);
//       });
//     }
//   }
// }));
