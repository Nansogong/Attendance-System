/**
 * Created by jaeseung on 2017. 6. 6..
 */
// var radio_lecture_amout = document.getElementsByName("radio_lecture_amount").value;
//
// if (radio_lecture_amout == "1"){
//     // 1번 시행
// }
// else if (radio_lecture_amout == "2"){
//     // 2번 시행
// }
// else {
//     // 3번 시행
// }



$(document).ready(function() {

    // DOM 생성 완료 시 화면 숨김
    // $("#changeM").hide();
    $("#changeI").hide();
    $("#changeH").hide();

    // radio change 이벤트
    $("input[name=radioName]").change(function() {
        var radioValue = $(this).val();
        if (radioValue == "M") {
            $("#changeM").show();
            $("#changeI").hide();
            $("#changeH").hide();
        } else if (radioValue == "I") {
            $("#changeI").show();
            $("#changeM").hide();
            $("#changeH").hide();
        } else if (radioValue == "H") {
            $("#changeH").show();
            $("#changeI").hide();
            $("#changeM").hide();
        }
    });

    // 서버에서 전달 받은 값으로 radio 버튼 변경
    // $("#changeUpdateRadio").click(function() {
    //     var resultValue = $("#radioId").val();
    //     $("input[name=radioName][value=" + resultValue + "]").attr("checked", true);
    // });

    // 체크 되어 있는지 확인
    var checkCnt = $("input[name=radioName]:checked").size();
    if (checkCnt == 0) {
        // default radio 체크 (첫 번째)
        $("input[name=radioName]").eq(0).attr("checked", true);
    }

});
