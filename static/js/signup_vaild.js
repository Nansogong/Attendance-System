/**
 * Created by seominkyu on 2017. 6. 2..
 */

function execute() {
    /// aaa와 bbb의 결과를 합쳐서 result에 보여주기
    var email_value = document.getElementById("input_email");
    var password_value = document.getElementById('input_password');

    var re = /^[0-9]+$/;
    if(!re.test(input_eamil.value)) {
        alert("숫자만 넣으셔야 합니다.");
        input_email.value="";
        input_email.focus();
        return;
    }


    // 문자-> 숫자 : parseInt(), Number() (실수 : parseFloat())
    var result = Number(aaa.value) + parseInt(bbb.value);

    if(isNaN(result)) {
        result = "숫자를 넣어라!"
    }

    document.getElementById("result").innerHTML = result;



}
function validate() {
    var id = document.getElementById('userid');
    var pass = document.getElementById('pass');
    var pass1 = document.getElementById('pass1');
    var name = document.getElementById('name');
    var email = document.getElementById('email');
    var tel1 = document.getElementById('tel1');
    var tel2 = document.getElementById('tel2');
    var tel3 = document.getElementById('tel3');

    // 이메일 검사
    // 4글자 이상(\w = [a-zA-Z0-9_], [\w-\.]) @가 나오고
    // 1글자 이상(주소). 글자 가 1~3번 반복됨
    if(!chk(/^[\w]{4,}@[\w]+(\.[\w-]+){1,3}$/, email, "이메일 형식에 어긋납니다."))
        return false;

    // 아이디 검사
    // 첫 글자는 반드시 영문 소문자, 4~12자로 이루어지고, 숫자가
    // 하나 이상 포함되어야 한다. 영문소문자와 숫자로만 이루어져야한다.
    // \d : [0-9]와 같다.       {n,m} : n에서 m까지 글자수
    if(!chk(/^[a-z][a-z\d]{3,11}$/, id, "첫글자는 영문 소문자, 4~12자 입력할것!"))
        return false;
    if(!chk(/[0-9]/, id, "숫자 하나이상포함!"))
        return false;

    // 비밀번호 확인 검사
    if(pass.value!=pass1.value) {
        alert("비밀번호 확인!");
    }

    // 이름 검사
    // 2글자 이상, 한글만
    // 통과하지 못하면 한글로 2글자 이상을 넣으세요~ alert 출력!
    if(!/^[가-힝]{2,}$/, name, "한글로 2글자 이상을 넣으세요~")
        return false;

    // 전화번호 검사

    // 전화번호 앞자리는 2~3자리 숫자, 두번째 자리는 3~4자리 숫자
    // 세번째 자리는 4자리 숫자

    if (tel1.value != '') {
        if (!chk(/^0(2|1[01679])$/, tel1, "번호 2자리 이상 입력"))
            return false;
        if (!chk(/^[0-9]{3,}$/, tel2, "번호 3자리 이상 입력"))
            return false;
        if (!chk(/^[0-9]{4}$/, tel3, "4자리 번호 입력"))
            return false;
    }

}

function chk(re, e, msg) {
    if (re.test(e.value)) {
        return true;
    }

    alert(msg);
    e.value = "";
    e.focus();
    return false;
}