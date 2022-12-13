function print() {
    let printContents  = document.querySelector('.list_print').innerHTML
    document.body.innerHTML = printContents
    window.print()
}