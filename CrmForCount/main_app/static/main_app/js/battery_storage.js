
function calculator_minus(elemMinus){
    let el = Number(document.getElementById('calc_value' + '_' + elemMinus).value) - 1
    if (el >= 0){
          let new_data = document.getElementById('calc_value' + '_' + elemMinus).value = el
    }
}
function calculator_plus(elemPlus){

    let max_position = document.getElementById('quantities' + elemPlus).innerHTML

    let el = Number(document.getElementById('calc_value' + '_' + elemPlus).value) + 1
    if (el <= max_position){
          let new_data = document.getElementById('calc_value' + '_' + elemPlus).value = el
    }

}