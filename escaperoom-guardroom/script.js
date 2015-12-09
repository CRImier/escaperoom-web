function resetLogin() {
    "use strict";
    document.getElementById('access').style.display = 'none';
    document.getElementById('info_block').style.outline = '3px solid #0F0';
    document.getElementById('password_block').style.display = 'block';
}

function checkPassword() {
    "use strict";
    var msgTimer;
    var password = document.getElementById('password_field').value;

    if (password === "a") {
        document.getElementById('password_block').style.display = 'none';
        document.getElementById('info_block').style.left = "25%";
        document.getElementById('info_block').style.top = "5%";
        document.getElementById('info_block').style.width = "50%";
        document.getElementById('info_block').style.height = "70%";
        document.getElementById('security_console').style.display = 'block';
    } else {
        document.getElementById('access').style.display = 'block';
        document.getElementById('info_block').style.outline = '3px solid #F00';
        document.getElementById('password_block').style.display = 'none';
        msgTimer = setTimeout(resetLogin, 2500);
    }
}

function checkSubmit(e) {
    "use strict";
    if (e && e.keyCode === 13) {
        checkPassword();
    }
}