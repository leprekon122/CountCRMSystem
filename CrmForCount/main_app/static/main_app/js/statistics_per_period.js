function mavic_autel_per_month() {

    var ctx = document.getElementById('myChart');

    var months = [document.getElementById('period').innerHTML]

    var mavic_per_month = document.getElementById('quant_of_mavic').innerHTML;
    var autel_per_month = document.getElementById('quant_of_autel').innerHTML

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: months,
            datasets: [
                {
                    label: 'Mavic',
                    data: mavic_per_month,
                    borderWidth: 3
                },
                {
                    label: 'Autel',
                    data: autel_per_month,
                    borderWidth: 3
                }
            ]
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

mavic_autel_per_month();