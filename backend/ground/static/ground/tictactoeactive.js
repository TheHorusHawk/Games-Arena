document.addEventListener('DOMContentLoaded', function () {
    squares = document.querySelectorAll(".square")
    squares.forEach(
        (square) => {
            if (square.innerHTML == "0") {
                const button = document.createElement("button")
                button.id = square.id;
                square.replaceWith(button)
            }
        }
    )
//     use edit buttons to activate edit mode 
//     let in_button = document.getElementById("in_button");
//     in_button.innerHTML = "Javascript loaded"
//     /*in_out_button.forEach((currentValue, currentIndex, listObj) => {
//         currentValue.addEventListener('click', (value) => get_in(value))
//     })*/
//     in_button.addEventListener('click', (x) => get_in(x))
});

// function get_in(event) {
//     let button = event.target;
//     button.innerText = 'Get out!';
//     console.log(button.innerHTML)
//     console.log("Clicked3")
//     fetch('toggle_in', {
//         method: 'POST',
//         body: JSON.stringify({
//         })
//     })
// }