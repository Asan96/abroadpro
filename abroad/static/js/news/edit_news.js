$(function () {
    $('#select_country,#select_school').selectpicker({
        size: 5
    });
    $('#select_country').change(function () {
        $('#select_school').empty();
        $('#select_school').append("<option value=''>请选择学校</option>");
        $.ajax({
                type: "post",
                data: {'country':$('#select_country').val()},
                dataType:'json',
                url: PUB_URL.dataSelectSchoolInit,
                success: function (data) {
                    let school_lst = data.msg.split(',');
                    for (let i=0;i<school_lst.length;i++){
                        let school = school_lst[i];
                        if (school!==''){
                            $('#select_school').append("<option value='"+school+"'>"+school+"</option>");
                        }
                    }
                    $('#select_school').selectpicker('refresh');
                }
            });
    })

});
function getParams(){
    let params ={
        'title':$('#edit_title').val(),
        'country':$('#select_country').val(),
        'school':$('#select_school').val(),
        'article': $('#edit_article').val(),
        'clas': $('#select_clas').val(),
    };
    if (params['title'] === ''){
        alert_msg('文章标题不得为空');
        return ''
    }else if (params['title'].length>50){
        alert_msg('标题过长，长度应小于五十字！');
        return ''
    }else if (params['article'].length>50000){
        alert_msg('内容过长，长度应小于五万字！');
        return ''
    }else if (params['country'] === ''){
        alert_msg('请选择留学国家！');
        return ''
    }else if (params['school'] === ''){
        alert_msg('请选择留学学校！');
        return ''
    }else if (params['clas'] === ''){
        alert_msg('请选择文章分类！');
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
    $('#select_country').selectpicker('val','');
    $('#select_school').selectpicker('val','');
    $('#select_clas').selectpicker('val','');
    $('#edit_article').val('');
}