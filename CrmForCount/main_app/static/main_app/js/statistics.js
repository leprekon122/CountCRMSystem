var mav_on_storage = document.getElementById('mav_on_storage').innerHTML
var mav_on_position = document.getElementById('mav_on_position').innerHTML
var data_set = [mav_on_storage, mav_on_position]

console.log(mav_on_storage)

const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Blue', 'Red'],
      datasets: [{
        label: '# of Votes',
        data: data_set,
        borderWidth: 1
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