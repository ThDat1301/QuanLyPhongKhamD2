function print_list_patient() {
    let printContents  = document.querySelector('.list_patient_by_day').innerHTML
    document.body.innerHTML = printContents
    window.print()
}