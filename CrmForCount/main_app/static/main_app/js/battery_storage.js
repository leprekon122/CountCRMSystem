
function calculator_minus(){
    let el = document.getElementById('calc_value').value - 1
    if (el >= 0){
          let new_data = document.getElementById('calc_value').value = el
    }
}
function calculator_plus(){
    let max_position = document.getElementById('quantities').innerHTML
    let el = Number(document.getElementById('calc_value').value) + 1
    console.log(max_position)
    console.log(el)
    if (el <= max_position){
          let new_data = document.getElementById('calc_value').value = el
    }

}