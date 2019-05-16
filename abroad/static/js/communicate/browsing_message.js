$(function () {
    let msg_type = $('#input_msg_type').val();
    let msg_state = $('#input_msg_state').val();
    if (msg_type === '1' &&msg_state === '0'){
        $('#btn_div').show()
    }
    else if(msg_type === '0' &&msg_state === '0'){
        read_message();
    }
});
let check_num = '';
$('#btn_agree').click(function () {
   check_num = 1;
   checkFriend(check_num);
});
$('#btn_disagree').click(function () {
   check_num = 0;
    checkFriend(check_num);
});
function checkFriend(check_num) {
    let params = {
        'check_num':check_num,
        'msg_id': $('#input_msg_id').val(),
        'from_user_id': $('#input_from_user_id').val(),
    };
    $.ajax({
        type: "post",
        data: params,
        dataType:'json',
        url: PUB_URL.dataCheckFriend,
        success: function (data) {
            if (data.ret){
                alert_msg(data.msg);
                $('#btn_div').hide()
            }else{
                alert_msg(data.msg);
                $('#btn_div').hide()
            }
        }
    });
}
function read_message() {
    $('#btn_div').hide();
    let params = {
        'msg_id': $('#input_msg_id').val(),
    };
    $.ajax({
        type: "post",
        data: params,
        dataType:'json',
        url: PUB_URL.dataReadMessage,
        success: function (data) {
            if (data.ret){
            }else{
                alert_msg(data.msg);
            }
        }
    });
}