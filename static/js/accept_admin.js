/**
 * Created by seominkyu on 2017. 6. 7..
 */

var professor_email;
var professor_name;
var real_count=0;


function accept()
{

    professor_name = document.getElementsByTagName('td')[1+real_count].childNodes[0].nodeValue;
    professor_email = document.getElementsByTagName('td')[2+real_count].childNodes[0].nodeValue;
    real_count += 5;

    var form = document.createElement("form");
    form.setAttribute("charset", "UTF-8");
    form.setAttribute("method", "Post"); // Get 또는 Post 입력
    form.setAttribute("action", "../views/website.py");

    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "professor_name");
    hiddenField.setAttribute("value", profeesor_name);
    form.appendChild(hiddenField);

    hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "professor_email");
    hiddenField.setAttribute("value", professor_email);
    form.appendChild(hiddenField);

    form.submit();

}

function reject(){
    // 이부분 다시 작성해야함
    alert("name : "+ professor_name +" 입니다");
    alert("email : "+ professor_email +" 입니다");
}
function gotoPage(){
    location.href="../templates/admin.html";
}