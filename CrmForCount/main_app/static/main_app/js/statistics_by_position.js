function mavic_autel_by_position() {


    var mav_on_position_Bangkok = document.getElementById('mavic_on_pos_Bangkok').innerHTML;
    var mav_aut_for_all_period_Bangkok = document.getElementById('autel_on_pos_Bangkok').innerHTML;

    var mav_on_position_Shushanik = document.getElementById('mavic_on_pos_Shushanik').innerHTML;
    var mav_aut_for_all_period_Shushanik = document.getElementById('autel_on_pos_Shushanik').innerHTML;

    var mav_on_position_Fog = document.getElementById('mavic_on_pos_Bangkok').innerHTML;
    var mav_aut_for_all_period_Fog = document.getElementById('autel_on_pos_Bangkok').innerHTML;



    const ctx = document.getElementById('myChartMavicPosition');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Bangkok', 'Shushanik', 'Fog'],
            datasets: [
                {
                    label: 'Mavic',
                    data: [Number(mav_on_position_Bangkok), Number(mav_on_position_Shushanik), Number(mav_on_position_Fog)],
                    borderWidth: 3
                },
                {
                    label: 'Autel',
                    data: [Number(mav_aut_for_all_period_Bangkok), Number(mav_aut_for_all_period_Shushanik), Number(mav_aut_for_all_period_Fog)],
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
mavic_autel_by_position()
