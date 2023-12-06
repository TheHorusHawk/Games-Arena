document.addEventListener('DOMContentLoaded', function () {
    squares = document.querySelectorAll(".square")
    squares.forEach(
        (square) => {
            if (square.innerHTML == "0") {
                const button = document.createElement("button")
                button.id = square.id;
                square.replaceWith(button)
                button.addEventListener('click', (value) => play(value))
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

function play(event) {
    const button = event.target;
    const csrftoken = getCookie('csrftoken')
    console.log(button.id)
    fetch('', {
        method: 'POST',
        body: JSON.stringify({
            id: button.id
        }),
        credentials: 'same-origin',
        headers: { "X-CSRFToken": csrftoken }
    })
}

//added to add csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}