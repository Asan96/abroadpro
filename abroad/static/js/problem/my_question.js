let table = '#table_my_question';
let table_child = [];
table_init();
function table_init(){
    window.operateEvents = {
        'click #btn_delete_question': function (e, value, row, index) {
            let question_id = row.question_id;
            swal({
                title: "操作确认",
                text: "删除后，您将无法恢复！",
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
                .then((willDelete) => {
                    if (willDelete) {
                        $.ajax({
                            type: "post",
                            data: {'question_id':question_id},
                            dataType:'json',
                            url: PUB_URL.dataDeleteQuestion,
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
    };
    window.operateEventsChild = {
        'click #btn_like': function (e, value, row, index) {
            let answer_id = row.answer_id;
            $.ajax({
                type: "post",
                data: {'answer_id':answer_id},
                dataType:'json',
                url: PUB_URL.dataAnswerLike,
                success: function (data) {
                    if (data.ret){
                        $(table_child).bootstrapTable('refresh')
                    }else{
                        alert_msg(data.msg)
                    }
                }
            });
        }
    };
    $(table).bootstrapTable({
        url: PUB_URL.dataMyQuestionTableInit,
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
        detailView: true,//父子表
        uniqueId: "question_id",
        contentType: "application/x-www-form-urlencoded",
        sidePagination: "server",
        pageSize: 5,
        pageList: [10, 15, 20, 30],        //可供选择的每页的行数（*）
        height: 600,
        pagination: true, // 是否分页
        sortable: true, // 是否启用排序
        columns: [
            {
                field: 'title',
                title: '问题描述',
                width: '60%',
                align: 'center',
                valign: 'middle',
                formatter:show_formatter_title
            },
            // {
            //     field: 'question',
            //     title: '问题内容',
            //     align: 'center',
            //     valign: 'middle',
            //     formatter:show_formatter_question,
            //     cellStyle:{
            //         css:{
            //             "overflow": "hidden",
            //             "text-overflow": "ellipsis",
            //             "white-space": "nowrap"
            //         }
            //     },
            // },
            // {
            //     field: 'state',
            //     title: '当前状态',
            //     align: 'center',
            //     valign: 'middle',
            //     formatter:function (value, row, index) {
            //         if (value ==='0')
            //         {
            //             return '未回答'
            //         }else if(value === '1'){
            //             return '已回答'
            //         }
            //     }
            // },
            {
                field: 'answer_num',
                title: '回答数',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'category',
                title: '分类',
                align: 'center',
                valign: 'middle',
            },{
                field: 'create_time',
                title: '提问时间',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'operate',
                title: '',
                width:100,
                align: 'center',
                valign: 'middle',
                formatter:operateFormatter,
                events:operateEvents
            },
        ],
        //注册加载子表的事件。注意下这里的三个参数！
        onExpandRow: function (index, row, $detail) {
            InitSubTable(index, row, $detail);
        }
    });
}
//初始化子表格(无线循环)
    InitSubTable = function (index, row, $detail) {
        var questionId = row.question_id;
        var cur_table = $detail.html('<table class="table table-striped article_table table_col_line"></table>').find('table');
        table_child.push(cur_table);
        $(cur_table).bootstrapTable({
            url: PUB_URL.dataMyQuestionChildTableInit,
            method: 'POST',
            queryParams : function(){
                return { 'question_id': questionId }
            },
            // clickToSelect: true,
            detailView: false,//父子表
            striped: true, // 是否显示行间隔色
            uniqueId: "answer_id",
            contentType: "application/x-www-form-urlencoded",
            pageSize: 5,
            pageList: [10, 15],
            pagination: true, // 是否分页
            columns: [{
                field: 'answer',
                title: '回答内容',
                align: 'center',
                width: '60%',
                valign: 'middle',
                formatter:show_formatter,
                cellStyle:{
                    css:{
                        "overflow": "hidden",
                        "text-overflow": "ellipsis",
                        "white-space": "nowrap"
                    }
                },
            }, {
                field: 'nickname',
                title: '回答人',
                align: 'center',
                valign: 'middle',
            }, {
                field: 'like_num',
                title: '点赞数',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'create_time',
                title: '回答时间',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'like',
                title: '',
                align: 'center',
                width: 60,
                valign: 'middle',
                formatter:formatterLike,
                events: operateEventsChild
            },
            ],
        });
    };
function show_formatter(value,row,index) {
    let span=document.createElement('span');
    span.setAttribute('title',value);
    span.innerHTML = value;
    return span.outerHTML;
}

function show_formatter_title(value,row,index) {
    let span=document.createElement('span');
    span.setAttribute('title',value);
    span.innerHTML = value;
    let href = "../browsing_question?question_id="+row.question_id;
    return  '<a href='+href+'>'+row.title+'</a>';
}

function operateFormatter(value, row, index) {
    return [
        '<div class="btn-group">',
        '<button id="btn_delete_question" type="button" class="btn btn-danger">删除</button>',
        '</div>'
    ].join('');
}
function formatterLike(value, row, index) {
    let user_is_like = row.user_is_like;
    if (user_is_like === '0'){
        return [
            '<div class="btn-group">',
            '<button id="btn_like" type="button" class="btn btn-dark glyphicon glyphicon-heart-empty"></button>',
            '</div>'
        ].join('');
    }else if(user_is_like === '1'){
        return [
            '<div class="btn-group">',
            '<button id="btn_like" type="button" class="btn btn-danger glyphicon glyphicon-heart"></button>',
            '</div>'
        ].join('');
    }
}