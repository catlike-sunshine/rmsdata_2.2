function initDataTable(lengthMenuParam,urlParam,columnsParam){
  return{
      "pagingType":"simple_numbers",
      destroy:true,
      serverSide:true,//开启服务器模式
      bProcessing:true,//开启读取服务器数据时显示正在加载中......
      sAjaxSource:urlParam,//ajax向后端请求的网址
      "fnServerData":function(sSource,aoData,fnCallback){
        $.ajax({
            "dataType":'json',
            "type":"post",
            "url":sSource,
            "data":{"aoData":JSON.stringify(aoData)},
            "success":function(resp){
                fnCallback(resp);
            },
        });
      },
      "columns":columnsParam,
      //添加copy、Excel、Print按钮
//      dom:"Bflrtip",
      dom:"flrtip",
      //dom控制控件顺序,l-length changing input control,f-filtering input,t-table,i-table information summary,p-pagination control,r-processing display element,B-buttons,R-ColReorder,S-select,默认lfrtip
//      buttons:[
//        'copy','excel','print'
//      ],
//      buttons:[
//          {
//              'extend':'excelHtml5',
//              'text':'下载Excel',
//              'className':'btn btn-primary',
//              'exportOptions':{
//                  body:function(data,row,column,node){
//                      return data
//                    //设置Excel下载
////                    $('#mydownload').click(function(){
////                        $.ajax({
////                            "type":"post",
////                            "url":"{% url 'data_platform:get_failure_mode_bank_list' 'A320' %}",
////                            "data":{"action":'download'},
////                            "success":function(data){
////                                return data;
////                            },
////                        });
////                    });
//                  },
//              },
//          },
//      ],
      "language": {
        "sProcessing": "处理中...",
        "sLengthMenu": "显示 _MENU_ 项结果",
        "sZeroRecords": "没有匹配结果",
        "sInfo": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
        "sInfoEmpty": "显示第 0 至 0 项结果，共 0 项",
        "sInfoFiltered": "(由 _MAX_ 项结果过滤)",
        "sInfoPostFix": "",
        "sSearch": "搜索:",
        "sUrl": "",
        "sEmptyTable": "表中数据为空",
        "sLoadingRecords": "载入中...",
        "sInfoThousands": ",",
        "oPaginate": {
            "sFirst": "首页",
            "sPrevious": "上页",
            "sNext": "下页",
            "sLast": "末页"
        },
        "oAria": {
            "sSortAscending": ": 以升序排列此列",
            "sSortDescending": ": 以降序排列此列"
        },
      },
  }
};

