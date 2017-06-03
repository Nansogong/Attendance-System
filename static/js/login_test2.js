/**
* Created by seominkyu on 2017. 6. 2..
*/

function submit_login() {

    var email_data = document.getElementById("input_email").value;
    var password_data = document.getElementById("input_password").value;

    var form = document.createElement("form");
    form.setAttribute("charset", "UTF-8");
    form.setAttribute("method", "Post"); // Get 또는 Post 입력
    form.setAttribute("action", "../views/website.py");

    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "email");
    hiddenField.setAttribute("value", email_data);
    form.appendChild(hiddenField);

    hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "pw");
    hiddenField.setAttribute("value", password_data);
    form.appendChild(hiddenField);

    form.submit();
}

function submit_signup(){
    location.href="../templates/signup.html";
}