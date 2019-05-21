let table = '#table_manage_news';
table_init();
function table_init(){
    window.operateEvents = {
        'click #btn_delete': function (e, value, row, index) {
            let news_id = row.id;
            swal({
                title: "操作确认",
                text: "删除后，您将无法恢复此文章！",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
                .then((willDelete) => {
                    if (willDelete) {
                        $.ajax({
                            type: "post",
                            data: {'news_id':news_id},
                            dataType:'json',
                            url: PUB_URL.dataDeletePush,
                            success: function (data) {
                                if (data.ret){
                                    swal(data.msg, {
                                        icon: "success",
                                    });
                                    $(table).bootstrapTable('remove', {
                                        field: 'title',
                                        values: [row.title]
                                    });
                                }else{
                                    alert_msg(data.msg)
                                }
                            }
                        });
                    } else {
                    }
                });
        }
    };
    $(table).bootstrapTable({
        url: PUB_URL.dataNewsTable,
        method: 'post',
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        queryParams: function (params) {
            return {
                limit: params.limit, // 每页要显示的数据条数
                offset: params.offset, // 每页显示数据的开始行号
                search_word: $('#search_word').val(),
            }
        },
        toolbar: "#toolbar",
        striped: true, // 是否显示行间隔色
        uniqueId: "title",
        contentType: "application/x-www-form-urlencoded",
        sidePagination: "server",
        pageSize: 20,
        pageList: [20, 30, 50, 100],        //可供选择的每页的行数（*）
        height:660,
        pagination: true, // 是否分页
        sortable: true, // 是否启用排序
        columns: [
            {
                field: 'title',
                title: '文章标题',
                align: 'center',
                valign: 'middle',
                width: '50%',
                formatter:href_formatter
            },
            {
                field: 'keyword',
                title: '关键词',
                align: 'center',
                valign: 'middle',
            },
            // {
            //     field: 'article',
            //     title: '文章内容',
            //     align: 'center',
            //     valign: 'middle',
            //     formatter:show_formatter,
            //     cellStyle:{
            //         css:{
            //             "overflow": "hidden",
            //             "text-overflow": "ellipsis",
            //             "white-space": "nowrap"
            //         }
            //     },
            // },
            {
                field: 'nickname',
                title: '发布人',
                width:120,
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'push_time',
                title: '推送时间',
                width:150,
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'operate',
                title: '操作',
                width: 80,
                align: 'center',
                valign: 'middle',
                formatter:operateFormatter,
                events: operateEvents
            },
        ],
    });
}
function href_formatter(value,row,index) {
    let title = value
    let news_id = row.id;
    let nickname = row.nickname;
    let href = '../browsing_news?news_id='+news_id+'&nickname='+nickname
    return '<a href='+href+'>'+title+'</a>'
};
function show_formatter(value,row,index) {
    let span=document.createElement('span');
    span.setAttribute('title',value);
    span.innerHTML = value;
    return span.outerHTML;
}
$('#btn_search').click(function () {
    $(table).bootstrapTable('refresh')
});
function table_refresh() {
    $('#search_word').val('');
    $(table).bootstrapTable('refresh')
}
function operateFormatter(value, row, index) {
    return [
        '<div class="btn-group">',
        '<button id="btn_delete" type="button" class="btn btn-danger">删除</button>',
        '</div>'
    ].join('');
}
