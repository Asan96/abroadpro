let cancel_num = 1;
let do_num = 0;
function cancel_like(answer_id) {
    let cancel_like_id = "#cancel_like"+answer_id
    cancel_num += 1;
    let is_like = cancel_num % 2;
    if ( is_like=== 0){
        $(cancel_like_id).attr("class", "glyphicon glyphicon-heart-empty");
    }else{
        $(cancel_like_id).attr("class", "glyphicon glyphicon-heart");
    }
    save_isLIke(answer_id,is_like)
}
function do_like(answer_id) {
    let do_like_id = "#do_like"+answer_id;
    do_num += 1;
    let is_like = do_num % 2;
    if ( is_like=== 0){
        $(do_like_id).attr("class", "glyphicon glyphicon-heart-empty");
    }else{
        $(do_like_id).attr("class", "glyphicon glyphicon-heart");
    }
    save_isLIke(answer_id, is_like)
}
function save_isLIke(answer_id,is_like) {
    let like_num_id = "#like_num"+answer_id;
    let like_num = parseInt($(like_num_id).text());
    $.ajax({
        type: "post",
        data: {
            'answer_id':answer_id,
            'is_like':is_like
            },
        dataType:'json',
        url: PUB_URL.dataBrowsingQuestionAnswerLike,
        success: function (data) {
            if (data.ret){
                if (is_like === 1){
                    $(like_num_id).html(like_num+1)
                } else if (is_like === 0){
                    $(like_num_id).html(like_num-1)
                }
            }else{
                alert_msg(data.msg)
            }
        }
    });
}