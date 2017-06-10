/**
 * Created by seominkyu on 2017. 6. 5..
 */

var professor_email;
var professor_name;


function accept(originalRequest)
{
    // 변수 선언 후 테이블 ID 명
    var tableSearch = $('wait_accept');

    // rows, cells ( TR / TD ) 를 length를 돌려
    // 테이블의 tr, td 갯수를 가져온다.
    var rowLen = tableSearch.rows.length;
    var celLen = tableSearch.cells.length;

    professor_email = tableSearch.rows[1].cells[2];
    professor_name = tableSearch.rows[1].cells[3];
}

// function accept(){



    // var form = document.createElement("form");
    // form.setAttribute("charset", "UTF-8");
    // form.setAttribute("method", "Post"); // Get 또는 Post 입력
    // form.setAttribute("action", "../views/website.py");
    //
    // var hiddenField = document.createElement("input");
    // hiddenField.setAttribute("type", "hidden");
    // hiddenField.setAttribute("name", "professor_email");
    // hiddenField.setAttribute("value", profeesor_email);
    // form.appendChild(hiddenField);
    //
    // hiddenField = document.createElement("input");
    // hiddenField.setAttribute("type", "hidden");
    // hiddenField.setAttribute("name", "professor_name");
    // hiddenField.setAttribute("value", professor_name);
    // form.appendChild(hiddenField);
    //
    // form.submit();
// }

function reject(){
    alert("email : "+ professor_email +" 입니다");
}
function gotoPage(){
    location.href="../templates/view_lecture.html";
}