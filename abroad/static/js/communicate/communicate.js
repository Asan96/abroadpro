let table = '#table_communicate';
table_init();
function table_init(){
    window.operateEvents = {
        'click #btn_delete_msg': function (e, value, row, index) {
            let msg_id = row.msg_id;
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
                            data: {'msg_id':msg_id},
                            dataType:'json',
                            url: PUB_URL.dataDeleteMessage,
                            success: function (data) {
                                if (data.ret){
                                    swal(data.msg, {
                                        icon: "success",
                                    });
                                    $(table).bootstrapTable('refresh', {
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
        url: PUB_URL.dataCommunicateTable,
        method: 'post',
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        queryParams: function (params) {
            return {
                limit: params.limit, // 每页要显示的数据条数
                offset: params.offset, // 每页显示数据的开始行号
                select_type: $('#select_type').val(),
                select_state: $('#select_state').val(),
                search_word: $('#input_search_word').val(),
                sort: params.sort,      //排序列名
                sortOrder: params.order, //排位命令（desc，asc）
                daterange:$('#id-daterange').val()
            }
        },
        toolbar: "#toolbar",
        striped: true, // 是否显示行间隔色
        uniqueId: "title",
        contentType: "application/x-www-form-urlencoded",
        sidePagination: "server",
        pageSize: 10,
        pageList: [10, 15, 20, 30],        //可供选择的每页的行数（*）
        height:450,
        pagination: true, // 是否分页
        sortable: true, // 是否启用排序
        columns: [
            {
                field: 'from_nickname',
                title: '发信人昵称',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'from_username',
                title: '发信人账号',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'message',
                title: '留言内容',
                align: 'center',
                valign: 'middle',
                formatter:show_formatter,
                cellStyle:{
                    css:{
                        "overflow": "hidden",
                        "text-overflow": "ellipsis",
                        "white-space": "nowrap"
                    }
                },
            },
            {
                field: 'type',
                title: '类型',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'create_time',
                title: '发送时间',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },
            {
                field: 'read_time',
                title: '已读时间',
                align: 'center',
                valign: 'middle',
                sortable: true
            },
            {
                field: 'state',
                title: '状态',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'operate',
                title: '查看',
                align: 'center',
                width: 100,
                valign: 'middle',
                formatter:href_formatter
            },
            {
                field: 'delete',
                title: '删除',
                align: 'center',
                width: 100,
                valign: 'middle',
                formatter:operateFormatter,
                events:operateEvents
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
function href_formatter(value,row,index) {
    let msg_id = row.msg_id;
    let href = '../browsing_message?msg_id='+msg_id;
    return '<a href='+href+'>查看</a>'
};
function operateFormatter(value, row, index) {
    return [
        '<div class="btn-group">',
        '<button id="btn_delete_msg" type="button" class="btn btn-danger">删 除</button>',
        '</div>'
    ].join('');
}
$('#btn_search').click(function () {
    $(table).bootstrapTable('refresh');
});
$('#btn_clear').click(function () {
    $('#input_search_word').val('');
    $('#select_state').selectpicker('val','');
    $('#select_type').selectpicker('val','');
    $('#id-daterange').val('');
    $('#daterange-btn span').html('发送时间');
});


$('#daterange-btn').daterangepicker(
    {
        ranges: {
            '今天': [moment(), moment().subtract(-1, 'days')],
            '昨天': [moment().subtract(1, 'days'), moment()],
            '近一周': [moment().subtract(6, 'days'), moment().subtract(-1, 'days')],
            '近30天': [moment().subtract(29, 'days'), moment().subtract(-1, 'days')],
            '本月': [moment().startOf('month'), moment().endOf('month')]
        },
        startDate: moment().subtract(30, 'days'),
        opens: 'right', //日期选择框的弹出位置
        buttonClasses: ['btn btn-default'],
        applyClass: 'btn-small btn-primary blue',
        cancelClass: 'btn-small',
        endDate: moment(),
        format: 'YYYY-MM-DD', //控件中from和to 显示的日期格式
        separator: 'to',
        autoUpdateInput: false,
        locale: {
            applyLabel: '确定',
            cancelLabel: '取消',
            fromLabel: '起始时间',
            toLabel: '结束时间',
            customRangeLabel: '自定义',
            daysOfWeek: ['日', '一', '二', '三', '四', '五', '六'],
            monthNames: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
            firstDay: 1
        }
    },
    function (start, end) {
        $('#daterange-btn span').html(start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
        $('#id-daterange').val(start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
    }
);
