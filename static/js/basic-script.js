document.getElementById("form").addEventListener("submit", function (e) {
    e.preventDefault();
});

// Don't submit form on enter
document.getElementById("form").onkeypress = (e) => {
    if (e.key == "Enter")
        e.preventDefault();
};

function asyncCheckLogin(login) {
    return new Promise((resolve, reject) => {
        const url = `/user/${login}`;
        var request = new XMLHttpRequest();
        request.open('GET', url);

        request.onload = function () {
            if (request.status === 404) {
                resolve(false);
            }
            else if (request.status === 200) {
                resolve(true);
            } else {
                reject(Error(`Unable to verify user; error code:${request.statusText}`));
            }
        };

        request.onerror = function () {
            reject(Error('There was a network error.'));
        };

        request.send();
    });
}

document.getElementById("username").addEventListener("change", function (e) {
    const input = e.target;
    var usernameInput = document.getElementById("username");
    
    asyncCheckLogin(input.value).then((isAvailable) => {
        if (isAvailable) {
            usernameInput.classList.remove("invalid");
            usernameInput.classList.add("valid");
            var message = "This username is available. Enjoy!"
        } else {
            usernameInput.classList.remove("valid");
            usernameInput.classList.add("invalid");
            var message = "This username is taken. Try another one."
        }
    
    var feedback = document.getElementById("feedback");    
    if (feedback != null) {
        feedback.parentNode.removeChild(feedback);
    }
    feedback = document.createElement("p");
    feedback.setAttribute("id", "feedback")
    usernameInput.insertAdjacentElement('afterend', feedback)
    var text = document.createTextNode(message);
    feedback.appendChild(text)
    }).catch((error) => console.log(error));
});