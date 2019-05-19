$('#btn_comment').click(function () {
    let params = {
        'news_id': $('#news_id').val(),
        'my_id': $('#my_id').val(),
        'comment': $('#input_comment').val()
    };
    $.ajax({
        type: "post",
        data: params,
        dataType:'json',
        url: PUB_URL.dataComment,
        success: function (data) {
            if (data.ret){
                alert_msg(data.msg);
                $('#input_comment').val('')
                $('#div_all_comment').append("<div class = \"panel-group\" id = \"comment"+data.comment_id+"\" style=\"margin-bottom: 0px\">\n" +
                    "                <div class = \"panel panel-default\" >\n" +
                    "                    <div class = \"panel-heading\" >\n" +
                    "                        <h4 class = \"panel-title\" >\n" +
                    "                            <a data-toggle = \"collapse\"  data-parent = \"#acordord\" href =\"#div_comment"+data.comment_id+"\">\n" +
                    "                                <span style=\"font-size: 16px\">\n" +
                    "                                         <span style=\"color: #0069d9\">"+data.nickname+" </span>\n" +
                    "                            的评论:</span>\n" +
                    "                            </a >\n" +
                    "                            <span style=\"float: right\">"+data.create_time+"</span>\n" +
                    "                            <p style=\"padding-top: 5px;text-align:left;padding-left: 50px\">\n" +
                    "                                <span>"+data.comment+"</span>\n" +
                    "                                    <a style=\"float: right;padding-right: 10px;color: red\" onclick=\"delete_comment("+data.comment_id+")\">删除</a>\n" +
                    "                            </p>\n" +
                    "                        </h4 >\n" +
                    "                    </div >\n" +
                    "                    <div id = \"div_comment"+data.comment_id+"\"  class = \"panel-collapse collapse \" >\n" +
                    "                        <div class = \"panel-body article_table\" style=\"padding-bottom: 0px\">\n" +
                    "                        </div>\n" +
                    "                    </div>\n" +
                    "                </div>\n" +
                    "            </div>")
            } else{
                alert_msg(data.msg)
            }
        }
    });
});
function reply_comment(comment_id) {
    $('#modal_reply').modal('show');
    $('#btn_reply_submit').unbind().click(function () {
        let params = {
          'comment_id': comment_id,
          'reply': $('#text_reply').val(),
        };
        $.ajax({
            type: "post",
            data: params,
            dataType:'json',
            url: PUB_URL.dataReplyComment,
            success: function (data) {
                if (data.ret){
                    $('#modal_reply').modal('hide');
                    let div_comment = '#div_comment'+params['comment_id'];
                    $(div_comment).append(
                        "<div class = 'panel-body article_table' style='padding-bottom: 0px'>"+
                        "<div style='padding-top: 0px' id='reply"+data.reply_id+"'>"+
                        "<div class='alert alert-dark' style='padding-top: 0px;padding-bottom: 0px;border: #f7e1b5 1px solid '>"+
                        "<span style='font-size: 16px'>"+
                        "<span style='color: #ba8b00'>"+data.nickname+"</span> 的回复:</span>"+
                        "<span style='float: right'>"+data.create_time+"</span>"+
                        "<p style='padding-top: 0px;text-align:left;padding-left: 50px'>"+
                        "<span>"+data.reply+"</span>"+
                        "<a style='float: right;color: red' onclick='delete_reply("+data.reply_id+")'>删除</a>\n"+
                        "</p>"+
                        "</div>"+
                        "</div>"+
                        "</div>"
                    )
                    // $(div_comment).refresh()
                } else{
                    alert_msg(data.msg)
                }
            }
        });
    })
}
function delete_comment(comment_id) {
    let params = {
        'comment_id': comment_id,
    };
    let comment_div = '#comment'+comment_id;
    $.ajax({
        type: "post",
        data: params,
        dataType:'json',
        url: PUB_URL.dataDeleteComment,
        success: function (data) {
            if (data.ret){
                alert_msg(data.msg)
                $(comment_div).remove()
            } else{
                alert_msg(data.msg)
            }
        }
    });
}

function delete_reply(reply_id) {
    let params = {
        'reply_id': reply_id,
    };
    let reply_div = '#reply'+reply_id;
    $.ajax({
        type: "post",
        data: params,
        dataType:'json',
        url: PUB_URL.dataDeleteReply,
        success: function (data) {
            if (data.ret){
                alert_msg(data.msg)
                $(reply_div).remove()
            } else{
                alert_msg(data.msg)
            }
        }
    });
}

$('#modal_reply').on('hide.bs.modal', function () {
    $('#text_reply').val('')
});