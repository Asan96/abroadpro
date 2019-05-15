let table = '#table_communicate';
table_init();
function table_init(){
    $(table).bootstrapTable({
        url: PUB_URL.dataCommunicateTable,
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
        pageSize: 10,
        pageList: [10, 15, 20, 30],        //可供选择的每页的行数（*）
        height:500,
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
            },
            {
                field: 'state',
                title: '状态',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'operate',
                title: '',
                align: 'center',
                width: 100,
                valign: 'middle',
                formatter:href_formatter
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