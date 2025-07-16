function show_filter_panel_btn(){
    let get_obj = document.getElementById('filter_panel_btn')

    if (window.screen.width < 500) {
        get_obj.style.display = 'block';
    }
}
show_filter_panel_btn()

let count_click = 0
function move_filter_block(){
    count_click += 1
    let = take_panel = document.getElementById('side_panel')
    if (count_click % 2 == 0){
        take_panel.style.display = 'none';

        console.log(count_click)
    } else if (count_click % 2 == 1){
        take_panel.style.display = 'block';
        take_panel.style.width = '97%';
        console.log(count_click)
    }
}