/* globals Chart:false, feather:false */

function hideallcharts(){
  document.getElementById('myChart').style.display= 'none';
  document.getElementById('pieChart').style.display= 'none';
  document.getElementById('doughnutChart').style.display= 'none';
  document.getElementById('scatterChart').style.display= 'none';
  document.getElementById('lineChart').style.display= 'none';
  document.getElementById('radarChart').style.display= 'none';
  document.getElementById('barChart').style.display= 'none';
  document.getElementById('polarChart').style.display= 'none';
  document.getElementById('bubbleChart').style.display= 'none';
}

function gettabledata(){
  //data
  var x_axis = [];
  var y_axis = [];
  var table = document.getElementById('testtable');
  for (var r = 0, n = table.rows.length; r < n; r++) {
      for (var c = 0, m = table.rows[r].cells.length; c < m; c++) {
          //console.log('r=',r,' c=',c, ' value=',table.rows[r].cells[c].innerHTML);
          if(r>0 && c==0){
            x_axis.push(table.rows[r].cells[c].innerHTML);
          }
          if(r>0 && c==1){
            y_axis.push(parseInt(table.rows[r].cells[c].innerHTML));
          }
      }
  }
  return { x: x_axis , y: y_axis}
}

function gettabledata2(){
  //data
  var xy_pair = [];
  var table = document.getElementById('testtable');
  for (var r = 0, n = table.rows.length; r < n; r++) {
    if(r>0){
      tmp = new Object();
      tmp = { x: parseInt(table.rows[r].cells[1].innerHTML), y: parseInt(table.rows[r].cells[3].innerHTML), };
      xy_pair.push(tmp);
    }
  }
  return xy_pair
}



(function () {
  'use strict'
  showchart1();
}())


function showchart2(){
  hideallcharts();
  document.getElementById('pieChart').style.display= 'block';
  var data=gettabledata();

  //var ctxP = document.getElementById("pieChart").getContext('2d');
  var ctxP = document.getElementById("pieChart").getContext('2d');
  var myPieChart = new Chart(ctxP, {
  type: 'pie',
  data: {
  labels: data['x'],
  datasets: [{
  data: data['y'],
  backgroundColor: ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
  hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
  }]
  },
  options: {
  responsive: true
  }
  });
}

function showchart3(){
  hideallcharts();
  document.getElementById('doughnutChart').style.display= 'block';
  var data=gettabledata();

  var ctxD = document.getElementById("doughnutChart").getContext('2d');
  var myLineChart = new Chart(ctxD, {
  type: 'doughnut',
  data: {
  labels: data['x'],
  datasets: [{
  data: data['y'],
  backgroundColor: ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
  hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
  }]
  },
  options: {
  responsive: true
  }
  });
}

function showchart4(){
  hideallcharts();
  document.getElementById('scatterChart').style.display= 'block';
  var datapair=gettabledata2();

  var ctxSc = document.getElementById('scatterChart').getContext('2d');
  var scatterData = {
  datasets: [{
    borderColor: 'rgba(99,0,125, .2)',
    backgroundColor: 'rgba(99,0,125, .5)',
    label: 'V(node2)',
    data: datapair
  }]
  }

  var config1 = new Chart.Scatter(ctxSc, {
    data: scatterData,
    options: {
    title: {
      display: true,
      text: 'Scatter Chart - Logarithmic X-Axis'
      },
    scales: {
      xAxes: [{
        type: 'logarithmic',
        position: 'bottom',
        ticks: {
          userCallback: function (tick) {
          var remain = tick / (Math.pow(10, Math.floor(Chart.helpers.log10(tick))));
            if (remain === 1 || remain === 2 || remain === 5) {
            return tick.toString() + 'Hz';
            }
          return '';
          },
        },
        scaleLabel: {
        labelString: 'Frequency',
        display: true,
        }
        }],
      yAxes: [{
        type: 'linear',
        ticks: {
        userCallback: function (tick) {
          return tick.toString() + 'dB';
          }
        },
        scaleLabel: {
        labelString: 'Voltage',
        display: true
        }
        }]
      }
    } 
  });
}

function showchart5(){
  hideallcharts();
  document.getElementById('lineChart').style.display= 'block';
  var datapair=gettabledata();

  //line
  var ctxL = document.getElementById("lineChart").getContext('2d');
  var myLineChart = new Chart(ctxL, {
  type: 'line',
  data: {
  labels: datapair['x'],
  datasets: [{
  label: "My First dataset",
  data: datapair['y'],
  backgroundColor: [
  'rgba(105, 0, 132, .2)',
  ],
  borderColor: [
  'rgba(200, 99, 132, .7)',
  ],
  borderWidth: 2
  },
  {
  label: "My Second dataset",
  data: [28, 48, 40, 19, 86, 27, 90],
  backgroundColor: [
  'rgba(0, 137, 132, .2)',
  ],
  borderColor: [
  'rgba(0, 10, 130, .7)',
  ],
  borderWidth: 2
  }
  ]
  },
  options: {
  responsive: true
  }
  });
}

function showchart6(){
  hideallcharts();
  document.getElementById('radarChart').style.display= 'block';
  var datapair=gettabledata();

  //radar
  var ctxR = document.getElementById("radarChart").getContext('2d');
  var myRadarChart = new Chart(ctxR, {
  type: 'radar',
  data: {
  labels: datapair['x'],
  datasets: [{
    label: "My First dataset",
    data: datapair['y'],
    backgroundColor: ['rgba(105, 0, 132, .2)', ],
    borderColor: ['rgba(200, 99, 132, .7)',],
    borderWidth: 2
    },
    {
    label: "My Second dataset",
    data: [28, 48, 40, 19, 96, 27, 100],
    backgroundColor: [
    'rgba(0, 250, 220, .2)',
    ],
    borderColor: [
    'rgba(0, 213, 132, .7)',
    ],
    borderWidth: 2
    }
  ]
  },
  options: {
  responsive: true
  }
  });
}

function showchart7(){
  hideallcharts();
  document.getElementById('barChart').style.display= 'block';
  var datapair=gettabledata();

  //bar
  var ctxB = document.getElementById("barChart").getContext('2d');
  var myBarChart = new Chart(ctxB, {
  type: 'bar',
  data: {
  labels: datapair['x'],
  datasets: [{
    label: '# of Votes',
    data: datapair['y'],
    backgroundColor: ['rgba(255, 99, 132, 0.2)','rgba(54, 162, 235, 0.2)','rgba(255, 206, 86, 0.2)','rgba(75, 192, 192, 0.2)','rgba(153, 102, 255, 0.2)','rgba(255, 159, 64, 0.2)'],
    borderColor: ['rgba(255,99,132,1)','rgba(54, 162, 235, 1)','rgba(255, 206, 86, 1)','rgba(75, 192, 192, 1)','rgba(153, 102, 255, 1)','rgba(255, 159, 64, 1)'],
    borderWidth: 1
    }]
  },
  options: {
    scales: {
    yAxes: [{
    ticks: {
    beginAtZero: true
    }
    }]
    }
  }
  });
}

function showchart8(){
  hideallcharts();
  document.getElementById('polarChart').style.display= 'block';
  var datapair=gettabledata();

  //polar
  var ctxPA = document.getElementById("polarChart").getContext('2d');
  var myPolarChart = new Chart(ctxPA, {
  type: 'polarArea',
  data: {
  labels: datapair['x'],
  datasets: [{
  data: datapair['y'],
  backgroundColor: ["rgba(219, 0, 0, 0.1)", "rgba(0, 165, 2, 0.1)", "rgba(255, 195, 15, 0.2)",
  "rgba(55, 59, 66, 0.1)", "rgba(0, 0, 0, 0.3)"
  ],
  hoverBackgroundColor: ["rgba(219, 0, 0, 0.2)", "rgba(0, 165, 2, 0.2)",
  "rgba(255, 195, 15, 0.3)", "rgba(55, 59, 66, 0.1)", "rgba(0, 0, 0, 0.4)"
  ]
  }]
  },
  options: {
  responsive: true
  }
  });
}

function showchart1(){
  hideallcharts();
  document.getElementById('myChart').style.display= 'block';

  feather.replace()

  //data
  var data=gettabledata();

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data['x'],
      datasets: [{
        data: data['y'],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
}

function showchart9(){
  hideallcharts();
  document.getElementById('bubbleChart').style.display= 'block';
  //var datapair=gettabledata();

  var ctxBc = document.getElementById('bubbleChart').getContext('2d');
  var bubbleChart = new Chart(ctxBc, {
  type: 'bubble',
  data: {
  datasets: [{
  label: 'John',
  data: [{
  x: 3,
  y: 7,
  r: 10
  }],
  backgroundColor: "#ff6384",
  hoverBackgroundColor: "#ff6384"
  }, {
  label: 'Peter',
  data: [{
  x: 5,
  y: 7,
  r: 10
  }],
  backgroundColor: "#44e4ee",
  hoverBackgroundColor: "#44e4ee"
  }, {
  label: 'Donald',
  data: [{
  x: 7,
  y: 7,
  r: 10
  }],
  backgroundColor: "#62088A",
  hoverBackgroundColor: "#62088A"
  }]
  }
  })
}