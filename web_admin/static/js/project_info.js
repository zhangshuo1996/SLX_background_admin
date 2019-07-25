/**
 * by dxy 2019/7/23
 */

$(".display").on("click",(e)=>{
    let $target = $(e.target);
    e = $target.parent();
    //取出要展示的数据
    let _id = e.attr("data-id");
    let name = e.attr("data-name");
    let project_type = e.attr("data-project_type");
    let fund = e.attr("data-fund");
    let start_time = e.attr("data-start_time");
    let end_time = e.attr("data-end_time");
    let mermbers_str = e.attr("data-members");
    let members = eval(mermbers_str);
    let memberstr = '';
    let leader = members[0]['name'];
    for(var i= 1;i<members.length;i++){
        memberstr += (" "+members[i]['name'])
    }
    let company = e.attr("data-company");
    let content = e.attr("data-content");

    //点击时,将这条数据放到左边的表格中
    let tbody = $(".displaying");
    thd = tbody.children().children();
    thd[1].textContent =  name;
    thd[3].innerText = project_type;
    thd[5].textContent = fund+' 万元';
    thd[7].textContent = start_time+'—'+end_time;
    thd[9].textContent = leader;
    thd[11].textContent = memberstr;
    thd[13].textContent = company;
    thd[15].textContent = content;
    //隐藏数据，用于保存时提交的数据库
    tbody.attr("data-members",mermbers_str);
    tbody.attr("data-start_time",start_time);
    tbody.attr("data-end_time",end_time);
    tbody.attr("data-_id",_id)
});

$(".preservation").on("click",(e)=>{
   let tbody = $(".displaying");
   thd = tbody.children().children();
   let name = thd[1].textContent;
   let project_type = thd[3].innerText;
   let funds = thd[5].textContent;
   let company = thd[13].textContent;
   let content = thd[15].textContent;
   let members = tbody.attr("data-members");
   let start_time = tbody.attr("data-start_time");
   let end_time = tbody.attr("data-end_time");
   let _id = tbody.attr("data-_id");
   let data = {
       "_id":_id,
       "name":name,
       "project_type":project_type,
       "fund":funds,
       "company":company,
       "content":content,
       "members":members,
       "start_time":start_time,
       "end_time":end_time,
   };
   $.ajax({
       type:"post",
       url:"/project_data_preservation",
       data:data,
       dataType:"json",
       success:function (response) {
           toggle_alert(true,response.message)
       },
       error:function (error) {
           console.log(error);
           toggle_alert(false,"操作失败，请稍后再试");
       }
   })
});

$(".ignore").on("click",(e)=>{
    console.log("ignore");
    let tbody = $(".displaying");
    thd = tbody.children().children();
    let _id = tbody.attr("data-_id");
    data = {"_id":_id};
    $.ajax({
        type: "post",
        url: "/project_data_ignore",
        data: data,
        dataType: "json",
            success: function (response) {
            toggle_alert(true,response.message)

        },
        error: function (error) {
             toggle_alert(false,"操作失败，请稍后再试");
        }
    })
});



    /**
 * 显示/隐藏提示框
 * @param {boolean} isSuccess
 * @param {string} message 用于显示的消息
 */
function toggle_alert(isSuccess,message = ""){


    let alert_success = $("#alert-box-success");
    let alert_error = $("#alert-box-danger");
    // 显示操作成功的提示框
    if(isSuccess){
        console.log(message);
        alert_error.hide();

        if(message){
            alert_success.find('.alert-message').text(message);
        }

        alert_success.show(200);
        setTimeout(()=>{
            alert_success.hide(200);
        }, 2500)
    }else{
        alert_success.hide();

        if(message){
            alert_error.find('.alert-message').text(message);
        }

        alert_error.show(200);
        setTimeout(()=>{
            alert_error.hide(200);
        },2500);
    }
}