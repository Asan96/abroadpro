let table = '#search_user';
$('#btn_search_user').click(function () {
    table_init();
});
function table_init(){
    window.operateEvents = {
        'click #btn_add':function (e, value, row, index) {
            let operate = row.operate;
            if (operate === '关注'){
                let user_id = row.user_id;
                let nickname = row.nickname;
                $.ajax({
                    type : "POST",
                    url : PUB_URL.dataAddFriendMsg,
                    dataType : "json",
                    data : {'user_id': user_id},
                    success : function(data) {
                        if (data.ret){
                            alert_msg(data.msg);
                        } else{
                            alert_msg(data.msg)
                        }
                    },
                    error : function (XMLHttpRequest, textStatus, errorThrown) {
                        alert_msg(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
                    }
                });
            } else{
                alert_msg('您已关注！')
            }
        }
    };
    $(table).bootstrapTable({
        url: PUB_URL.dataSearchUser,
        method: 'post',
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        queryParams: function (params) {
            return {
                limit: params.limit, // 每页要显示的数据条数
                offset: params.offset, // 每页显示数据的开始行号
                search_word : $('#input_search_user').val(),
            }
        },
        toolbar: "#toolbar",
        striped: true, // 是否显示行间隔色
        uniqueId: "title",
        contentType: "application/x-www-form-urlencoded",
        sidePagination: "server",
        pageSize: 5,
        height:500,
        pagination: true, // 是否分页
        sortable: false, // 是否启用排序
        columns: [
            {
                field: 'username',
                title: '用户账号',
                align: 'center',
                valign: 'middle',
            },{
                field: 'nickname',
                title: '昵称',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'sex',
                title: '性别',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'birthday',
                title: '生日',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'operate',
                title: '',
                width: 110,
                align: 'center',
                valign: 'middle',
                formatter:operateFormatter,
                events: operateEvents
            }
        ],
    });
}
function operateFormatter(value, row, index) {
    return [
        '<div class="btn-group">',
        '<button id="btn_add" type="button" class="btn btn-warning" style="width: 80px">'+value+'</button>',
        '</div>'
    ].join('');
}