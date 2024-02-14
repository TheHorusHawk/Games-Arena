//sets socket up for reloading when there's a move
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const gameSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/tictactoe/'
    + roomName
    + '/'
);
gameSocket.onmessage = () => location.reload();
gameSocket.onclose = () => console.error('Socket closed unexpectedly');

document.addEventListener("DOMContentLoaded", () => {
    //Checks if it's the current player to play
    visibility = document.getElementById('turn').style.display;
    toPlay = visibility === 'block'

    //fetches all the squares to be transformed
    squares = document.querySelectorAll(".square")

    if (!toPlay) {
        squares.forEach(
            (square) => {
                if (square.innerHTML == "0") {
                    square.innerHTML = " "
                }
                else {
                    square.innerHTML == "1" ? square.innerHTML = "X" : square.innerHTML = "O";
                }
            }
        )
    }
    else {
        squares.forEach(
            (square) => {
                if (square.innerHTML == "0") {
                    const button = document.createElement("button")
                    button.id = square.id;
                    square.replaceWith(button)
                    button.addEventListener('click', (value) => play(value))
                }
                else {
                    square.innerHTML == "1" ? square.innerHTML = "X" : square.innerHTML = "O";
                }
            }
        )
    }

})


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
    }).then(() => {
        gameSocket.send(JSON.stringify({
            'message': "Sup"
        }))
        console.log("sent?")
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
