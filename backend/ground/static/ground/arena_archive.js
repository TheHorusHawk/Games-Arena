//old js file for button_clicking

document.addEventListener('DOMContentLoaded', function () {

    //use edit buttons to activate edit mode 
    let in_out_button = document.getElementById("in_out_button");
    /*in_out_button.forEach((currentValue, currentIndex, listObj) => {
        currentValue.addEventListener('click', (value) => get_in(value))
    })*/
    in_out_button.addEventListener('click',(x) => get_in(x))
});

function get_in(event) {
    let button = event.target;
    button.innerText = 'Get out!';
    console.log(button.innerHTML)
    console.log("Clicked3")
    fetch('/ground/toggle_in', {
        method: 'POST',
        body: JSON.stringify({
        })
    })