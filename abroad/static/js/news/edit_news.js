function getParams(){
    let params ={
        'title':$('#edit_title').val(),
        'keyword': $('#edit_keyword').val(),
        'article': $('#edit_article').val(),
    };
    if (params['title'] === ''){
        alert_msg('文章标题不得为空');
        return ''
    }else if (params['title'].length>50){
        alert_msg('标题过长，长度应小于五十字！');
        return ''
    }else if (params['keyword'] === ''){
        alert_msg('文章关键词不得为空！');
        return ''
    }else if (params['keyword'].length>50){
        alert_msg('关键词过长，长度应小于五十字！');
        return ''
    }else if (params['article'].length>50000){
        alert_msg('内容过长，长度应小于五万字！');
        return ''
    }else if (params['article']=== ''){
        alert_msg('文章内容不得为空！');
        return ''
    }
    else
    {
        return params
    }
}
$('#save_btn').click(function () {
    let params = getParams();
    if (params){
        $.ajax({
            type : "POST",
            url : PUB_URL.dataEditSave,
            dataType : "json",
            data : params,
            success : function(data) {
                if (data.ret){
                    alert_msg(data.msg)
                    input_clear();
                } else {
                    alert_msg(data.msg)
                }
            },
            error : function (XMLHttpRequest, textStatus, errorThrown) {
                alert_msg(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
            }
        })
    }
})
$('#submit_btn').click(function () {
    let params = getParams()
    if (params){
        $.ajax({
            type : "POST",
            url : PUB_URL.dataEditSubmit,
            dataType : "json",
            data : getParams(),
            success : function(data) {
                if (data.ret){
                    alert_msg(data.msg)
                    input_clear();
                } else {
                    alert_msg(data.msg)
                }
            },
            error : function (XMLHttpRequest, textStatus, errorThrown) {
                alert_msg(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
            }
        })
    }
})
function input_clear() {
    $('#edit_title').val('');
    $('#edit_keyword').val('');
    $('#edit_article').val('');
}