var mav_on_storage = document.getElementById('mav_on_storage').innerHTML
var mav_on_position = document.getElementById('mav_on_position').innerHTML
var mav_for_all_period  = document.getElementById('mav_for_all_period').innerHTML
var all_destroy = document.getElementById('all_destroy').innerHTML
var data_set = [mav_on_storage, mav_on_position, mav_for_all_period, all_destroy]

console.log(mav_on_storage)

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