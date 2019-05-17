let count = parseInt($('#my_answer_count').val());
$(function () {
    if (count===0){
        $('#div_warning').show();
    }
});
function delete_answer(answer_id) {
    let remove_div = '#panel'+answer_id;
    $.ajax({
        type: "post",
        data: {'answer_id':answer_id},
        dataType:'json',
        url: PUB_URL.dataDeleteAnswer,
        success: function (data) {
            if (data.ret){
                $(remove_div).remove();
                count -= 1;
                if (count === 0) {
                    $('#div_warning').show();
                }
            }else{
                alert_msg(data.msg)
            }
        }
    });
}