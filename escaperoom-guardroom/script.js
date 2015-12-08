function checkPassword() {
    "use strict";
    var msgTimer;
    var password = document.getElementById('password_field').value;

    if (password === "correcthorse") {
        window.alert('omelette du fromage');
    } else {
        document.getElementById('access').style.display = 'block';
        document.getElementById('info_block').style.outline = '3px solid #F00'
        document.getElementById('password_block').style.display = 'none';
        msgTimer = setTimeout(resetLogin, 3000);
    }
}

function checkSubmit(e) {
    "use strict";
    if (e && e.keyCode === 13) {
        checkPassword();
    }
}

function resetLogin() {
    document.getElementById('access').style.display = 'none';
    document.getElementById('info_block').style.outline = '3px solid #0F0';
    document.getElementById('password_block').style.display = 'block';
}