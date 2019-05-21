$('#btn_question_submit').click(function () {
    let question = $('#input_raise_question').val();
    let params = {
        'title': $('#input_title').val(),
        'category_id': $('#select_category').val(),
        'question': $('#textarea_question').val(),
    };
    if (params['question'].length> 300)
    {
        alert_msg('问题内容过长，请在三百字以内！')
    }else if (params['title'].length>=50)
    {
        alert_msg('问题描述过长，请在五十字以内！')
    }else{
        $.ajax({
            type: "post",
            data: params,
            dataType:'json',
            url: PUB_URL.dataRaiseQuestion,
            success: function (data) {
                if (data.ret){
                    alert_msg(data.msg)
                    clear_input()
                }else{
                    alert_msg(data.msg)
                }
            }
        });
    }
});
function clear_input() {
   $('#input_title').val('');
   $('#select_category').selectpicker('val','');
   $('#textarea_question').val('')
}