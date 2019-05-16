let table = '#table_my_friend';
table_init();
function table_init(){
    window.operateEvents = {
        'click #btn_send_msg': function (e, value, row, index) {
            $('#modal_send_message').modal('show');
            $('#btn_send_message').unbind().click(function () {
                let params = {
                    'user_id': row.user_id,
                    'message': $('#text_message').val()
                };
                $.ajax({
                    type: "post",
                    data: params,
                    dataType:'json',
                    url: PUB_URL.dataSendMessage,
                    success: function (data) {
                        if (data.ret){
                            swal(data.msg, {
                                icon: "success",
                            });
                            $('#modal_send_message').modal('hide');
                        }else{
                            alert_msg(data.msg)
                        }
                    }
                });
            });
        }
    };
    $(table).bootstrapTable({
        url: PUB_URL.dataMyFriendTableInit,
        method: 'post',
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        queryParams: function (params) {
            return {
                limit: params.limit, // 每页要显示的数据条数
                offset: params.offset, // 每页显示数据的开始行号
                search_word : $('#input_search_friend').val(),
            }
        },
        toolbar: "#toolbar",
        striped: true, // 是否显示行间隔色
        uniqueId: "title",
        contentType: "application/x-www-form-urlencoded",
        sidePagination: "server",
        pageSize: 5,
        pageList: [10, 15, 20, 30],        //可供选择的每页的行数（*）
        height:500,
        pagination: true, // 是否分页
        sortable: true, // 是否启用排序
        columns: [
            {
                checkbox: true,
            },
            {
                field: 'nickname',
                title: '昵称',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'username',
                title: '账号',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'operate',
                title: '',
                align: 'center',
                width: 100,
                valign: 'middle',
                formatter:operateFormatter,
                events:operateEvents,
            },
        ],
    });
}
function operateFormatter(value, row, index) {
    return [
        '<div class="btn-group">',
        '<button id="btn_send_msg" type="button" class="btn btn-dark">留 言</button>',
        '</div>'
    ].join('');
}
$('#btn_search_friend').click(function () {
    $(table).bootstrapTable('refresh');
});
 $('#modal_send_message').on('hide.bs.modal', function () {
     $('#text_message').val('')
 });
$('#btn_delete_friend').click(function () {
    let user_id_lst = getSelection();
    console.log(user_id_lst)
    if (user_id_lst.length===0){
        alert_msg('您没有选择要删除的好友！')
    }else{
        swal({
            text: "确认删除吗！",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
            .then((willDelete) => {
                if (willDelete) {
                    $.ajax({
                        type: "post",
                        data: {'user_id_lst': JSON.stringify(user_id_lst) },
                        dataType:'json',
                        url: PUB_URL.dataDeleteFriend,
                        success: function (data) {
                            if (data.ret){
                                swal(data.msg, {
                                    icon: "success",
                                });
                                $(table).bootstrapTable('refresh');
                            }else{
                                alert_msg(data.msg)
                            }
                        }
                    });
                } else {
                }
            });
    }
});
function getSelection() {
    return $.map($(table).bootstrapTable('getSelections'), function(row) {
        return row.user_id
    });
}

$('#modal_send_message').on('hide.bs.modal', function () {
    $('#text_message').val('')
});