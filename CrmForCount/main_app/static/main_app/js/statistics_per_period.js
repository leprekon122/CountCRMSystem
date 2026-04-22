function mavic_autel_per_month() {

    var ctx = document.getElementById('myChart');

    var months = [document.getElementById('period').innerHTML]

    var mavic_per_month = document.getElementById('quant_of_mavic').innerHTML;
    var autel_per_month = document.getElementById('quant_of_autel').innerHTML;



    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: months,
            datasets: [
                {
                    label: 'Mavic',
                    data: [Number(mavic_per_month)],
                    borderWidth: 3
                },
                {
                    label: 'Autel',
                    data: [Number(autel_per_month)],
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

function avic_autel_by_position() {


    var mav_on_position_Bangkok = document.getElementById('mavic_on_pos_Bangkok').innerHTML;
    var mav_aut_for_all_period_Bangkok = document.getElementById('autel_on_pos_Bangkok').innerHTML;

    var mav_on_position_Shushanik = document.getElementById('mavic_on_pos_Shushanik').innerHTML;
    var mav_aut_for_all_period_Shushanik = document.getElementById('autel_on_pos_Shushanik').innerHTML;

    var mav_on_position_Fog = document.getElementById('mavic_on_pos_Bangkok').innerHTML;
    var mav_aut_for_all_period_Fog = document.getElementById('autel_on_pos_Bangkok').innerHTML;

    var mav_on_position_Fog = document.getElementById('mavic_on_pos_Falcon').innerHTML;
    var mav_aut_for_all_period_Fog = document.getElementById('autel_on_pos_Falcon').innerHTML;


    const ctx = document.getElementById('myChartMavicPosition');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Bangkok', 'Shushanik', 'Fog', 'Falcon'],
            datasets: [
                {
                    label: 'Mavic',
                    data: [Number(mav_on_position_Bangkok), Number(mav_on_position_Shushanik), Number(mav_on_position_Fog), Number(mav_on_position_Falcon)],
                    borderWidth: 4
                },
                {
                    label: 'Autel',
                    data: [Number(mav_aut_for_all_period_Bangkok), Number(mav_aut_for_all_period_Shushanik), Number(mav_aut_for_all_period_Fog), Number(mav_aut_for_all_period_Falcon)],
                    borderWidth: 4
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


function mavic_autel_by_position() {
    const positions = ['Bangkok', 'Shushanik', 'Fog', 'Falcon'];

    const mavicData = positions.map(pos =>
        Number(document.getElementById(`mavic_on_pos_${pos}`).textContent.trim())
    );

    const autelData = positions.map(pos =>
        Number(document.getElementById(`autel_on_pos_${pos}`).textContent.trim())
    );

    const ctx = document.getElementById('myChartMavicPosition');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: positions,
            datasets: [
                {
                    label: 'Mavic',
                    data: mavicData,
                    borderWidth: 4
                },
                {
                    label: 'Autel',
                    data: autelData,
                    borderWidth: 4
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

mavic_autel_by_position();




