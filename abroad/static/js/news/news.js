let table = '#table_news'
table_init();
function table_init(){
    $(table).bootstrapTable({
        url: PUB_URL.dataNewsTable,
        method: 'post',
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        queryParams: function (params) {
            return {
                limit: params.limit, // 每页要显示的数据条数
                offset: params.offset, // 每页显示数据的开始行号
                title_search: $('#title_search').val(),
                nickname_search : $('#nickname_search').val(),
                keyword_search : $('#keyword_search').val(),
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
                field: 'title',
                title: '文章标题',
                align: 'center',
                valign: 'middle',
                formatter:href_formatter
            },
            {
                field: 'keyword',
                title: '关键词',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'article',
                title: '文章内容',
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
                field: 'nickname',
                title: '发布人',
                align: 'center',
                valign: 'middle',
            },
            {
                field: 'push_time',
                title: '推送时间',
                align: 'center',
                valign: 'middle',
            },
        ],
    });
}
function href_formatter(value,row,index) {
    let title = value;
    let nickname = row.nickname;
    let href = '../browsing?title='+title+'&nickname='+nickname
    console.log(href)
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
$('#btn_clear').click(function () {
    $('#title_search').val('');
    $('#nickname_search').val('');
    $('#keyword_search').val('');
});