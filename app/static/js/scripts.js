function print_list_patient() {
    let printContents  = document.querySelector('.list_print').innerHTML
    document.body.innerHTML = printContents
    window.print()
}