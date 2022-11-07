let yourself_form = document.querySelector('.yourself-form');
let other_form = document.querySelector('.other-form');
let radio_check_patient = document.getElementsByName('patient')
yourself_form.style.display = 'block'
other_form.style.display = 'none'
let radio_length = radio_check_patient.length
for(let i = 0; i < radio_length; i++) {
    radio_check_patient[i].onclick = function (){
        let val = this.value;
        if(val == 'yourself') {
            yourself_form.style.display = 'block'
            other_form.style.display = 'none'
        }
        else if (val=='other') {
            other_form.style.display = 'block'
            yourself_form.style.display = 'none'
        }
    }
}