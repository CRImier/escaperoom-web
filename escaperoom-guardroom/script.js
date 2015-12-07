function checkPassword() {
    "use strict";
    var password = document.getElementById('password_field').value;

    if (password === "correcthorse") {
        window.alert('omelette du fromage');
    } else {
        document.getElementById('access').style.display = 'table-cell';
        document.getElementById('password_block').style.display = 'none';
    }
}

function checkSubmit(e) {
    "use strict";
    if (e && e.keyCode === 13) {
        checkPassword();
    }
}