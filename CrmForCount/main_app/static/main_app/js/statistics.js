function main_report(){
var mav_on_storage = document.getElementById('mav_on_storage').innerHTML
var mav_on_position = document.getElementById('mav_on_position').innerHTML
var mav_for_all_period  = document.getElementById('mav_for_all_period').innerHTML
var all_destroy = document.getElementById('all_destroy').innerHTML


var data_set = [mav_on_storage, mav_on_position, mav_for_all_period, all_destroy]

const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['in storage','mav_on_position', 'mav_for_all_period', 'all_destroy'],
      datasets: [{
        label: 'data',
        data: data_set,
        borderWidth: 3
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  }

main_report()


function mavic_autel_report() {

    var mav_on_storage = document.getElementById('mav_aut_on_storage').innerHTML;
    var mav_on_position = document.getElementById('mav_aut_on_position').innerHTML;
    var mav_aut_for_all_period = document.getElementById('mav_aut_for_all_period').innerHTML;

    var all_mav_aut_destroy = document.getElementById('all_mav_aut_destroy').innerHTML;

    console.log(mav_aut_for_all_period)


    const ctx = document.getElementById('myChartMavic');

    new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['mav_in storage','mav_on_position', 'mav_aut_for_all_period', 'all_mav_aut_destroy'],
      datasets: [{
        label: 'data',
        data: [mav_on_storage, mav_on_position, mav_aut_for_all_period, all_mav_aut_destroy],
        borderWidth: 3
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }

      }
    }
  });

  }
mavic_autel_report();
