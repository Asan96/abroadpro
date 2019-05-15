table_init('#table_my_draft');
function table_init(table){
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
        },
        'click #btn_modify':function (e, value, row, index) {
            let news_id = row.id;
            $.ajax({
                type : "POST",
                url : PUB_URL.dataLoadDraft,
                dataType : "json",
                data : {'news_id':news_id},
                success : function(data) {
                    if (data.id){
                      $('#draft_title').val(data.title);
                      $('#draft_keyword').val(data.keyword);
                      $('#draft_article').val(data.article);
                    }
                },
                error : function (XMLHttpRequest, textStatus, errorThrown) {
                    alert_msg(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
                }
            });
            $('#modal_draft').modal('show');
            $('#btn_modify_save').unbind().click(function () {
                let params = {
                    'news_id':news_id,
                    'title': $('#draft_title').val(),
                    'keyword': $('#draft_keyword').val(),
                    'article': $('#draft_article').val(),
                };
                $.ajax({
                    type : "POST",
                    url : PUB_URL.dataModifySave,
                    dataType : "json",
                    data : params,
                    success : function(data) {
                        if (data.ret){
                            alert_msg(data.msg);
                            $('#modal_draft').modal('hide');
                        }else{
                            alert_msg(data.msg)
                        }
                    },
                    error : function (XMLHttpRequest, textStatus, errorThrown) {
                        alert_msg(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
                    }
                });
            })
        },
        'click #btn_submit':function (e, value, row, index) {
            let news_id = row.id;
            $.ajax({
                type : "POST",
                url : PUB_URL.dataDraftSubmit,
                dataType : "json",
                data : {'news_id':news_id},
                success : function(data) {
                    if (data.ret){
                        alert_msg(data.msg);
                        $(table).bootstrapTable('remove', {
                            field: 'title',
                            values: [row.title]
                        });
                    } else{
                        alert_msg(data.msg)
                    }
                },
                error : function (XMLHttpRequest, textStatus, errorThrown) {
                    alert_msg(XMLHttpRequest.status+" "+textStatus+" "+errorThrown)
                }
            });
        }
    };
    $(table).bootstrapTable({
        url: PUB_URL.dataDraftTable,
        method: 'post',
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        queryParams: function (params) {
            return {
                limit: params.limit, // 每页要显示的数据条数
                offset: params.offset, // 每页显示数据的开始行号
            }
        },
        toolbar: "#toolbar",
        striped: true, // 是否显示行间隔色
        uniqueId: "title",
        contentType: "application/x-www-form-urlencoded",
        sidePagination: "server",
        pageSize: 6,
        pageList: [10, 15, 20, 30],        //可供选择的每页的行数（*）
        height:480,
        pagination: true, // 是否分页
        sortable: true, // 是否启用排序
        columns: [
            {
                field: 'title',
                title: '文章标题',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'keyword',
                title: '关键词',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'create_time',
                title: '推送时间',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'update_time',
                title: '更新时间',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'article',
                title: '文章内容',
                align: 'center',
                valign: 'middle',
                cellStyle:{
                    css:{
                        "overflow": "hidden",
                        "text-overflow": "ellipsis",
                        "white-space": "nowrap"
                    }
                },
                formatter:show_formatter
            },
            {
                field: 'price',
                title: '操作',
                width: 200,
                align: 'center',
                valign: 'middle',
                formatter:operateFormatter,
                events: operateEvents
            },

        ],
    });
}
function show_formatter(value,row,index) {
    let span=document.createElement('span');
    span.setAttribute('title',value);
    span.innerHTML = value;
    return span.outerHTML;
}

function operateFormatter(value, row, index) {
    return [
        '<div class="btn-group">',
        '<button id="btn_delete" type="button" class="btn btn-warning">删除</button>',
        '<button id="btn_modify" type="button" class="btn btn-default" style="">修改</button>',
        '<button id="btn_submit" type="button" class="btn btn-dark" style="">发布</button>',
        '</div>'
    ].join('');
}