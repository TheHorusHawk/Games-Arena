document.addEventListener('DOMContentLoaded', function () {
    squares = document.querySelectorAll(".square")
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
});