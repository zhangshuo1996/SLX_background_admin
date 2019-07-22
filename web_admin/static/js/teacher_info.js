/**
 * 点击右侧的商务和时间那一行，在左边将信息展示出来
 */
$(".display").on("click",(e)=>{
    //通过e来获取点击的那一行，e代表那个tr
    let $target = $(e.target);
    e = $target.parent();
    let tbody = $(".displaying");
    thd = tbody.children().children();
    //将左侧表格中字体颜色设置为黑色，否则在一次改变为红色后，这个td将变为红色
    for (var i=1; i<=22; i += 3)
        {
            $(thd[i]).css("color","black");
            $(thd[i+1]).css("color","black");

        }
    // $(thd[i+1]).css("color","red");
    //将选中的这一行的数据，即商务提交的教师信息取出来
    let id = e.children()[2].textContent;
    let name = e.children()[3].textContent;
    let school = e.children()[4].textContent;
    let institution = e.children()[5].textContent;
    let title = e.children()[6].textContent;
    let honor = e.children()[7].textContent;
    let email = e.children()[8].textContent;
    let phone_number = e.children()[9].textContent;
    let office_number = e.children()[10].textContent;
    let edu_exp = e.children()[11].textContent;
    let teacher_id = e.children()[12].textContent;
    let birth_year = e.children()[13].textContent;
    let object_id = e.children()[14].textContent;
    let domain = e.children()[15].textContent;
    let department = e.children()[16].textContent;
    //将取出的信息填充到左边table的第三列，所以从thd[2]开始,逐个加3，就都是修改第三列


    thd[2].textContent = name;
    if(birth_year=="None") {
        thd[5].textContent = "";
    }
    else thd[5].textContent = birth_year;
    thd[8].textContent = school+institution+department;
    thd[11].textContent = title+"\t"+honor;
    thd[14].textContent = domain;
    thd[17].textContent = email;
    thd[20].textContent = office_number;
    thd[23].textContent = phone_number;
    thd[26].textContent = edu_exp;
    //隐藏数据，用于提交给数据库
    thd[27].textContent = school;
    thd[28].textContent= institution;
    thd[29].textContent= title;
    thd[30].textContent = honor;
    thd[31].textContent = teacher_id;
    thd[32].textContent = object_id;
    thd[33].textContent  = department;
    if(teacher_id != "None") {
        let type = $(".type");
        type.text("具体信息（修改信息）");
        //从数据库中将这个老师的数据取出来
        let data = {"teacher_id": teacher_id};
        $.ajax({
            type: "post",
            url: "/get_info_by_tid",
            data: data,
            dataType: "json",
            success: function (response) {
                //填充到左边table的第二栏
                thd[1].textContent = response["name"];
                thd[4].textContent = response["birth_year"];
                thd[7].textContent = response["school"] + response["institution"]+response["department"];
                thd[10].textContent = response["title"]+"\t"+response["honor"];
                thd[13].textContent = response["domain"];
                thd[16].textContent = response["email"];
                thd[19].textContent = response["office_number"];
                thd[22].textContent = response["phone_number"];
                thd[25].textContent = response["edu_exp"];
                for (var i=1; i<=25; i += 3)
                {
                    if(thd[i].textContent != thd[i+1].textContent){
                        $(thd[i+1]).css("color","red");
                    }
                }
            }
        });

    }
    //新增记录的处理
    else{

                let type = $(".type");
                type.text("具体信息（新增信息）");
                thd[1].textContent = "";
                thd[4].textContent = "";
                thd[7].textContent = "";
                thd[10].textContent = "";
                thd[13].textContent = "";
                thd[16].textContent = "";
                thd[19].textContent = "";
                thd[22].textContent = "";
                thd[25].textContent = "";

    }

});

$(".preservation").on("click",(e)=>{
    //将商务提交的数据取出来
    console.log("preservation");
    let $target = $(e.target);
    let tbody = $(".displaying");
    let name= thd[2].textContent;
    let birth_year = thd[5].textContent;
    let school = thd[27].textContent;
    let institution=  thd[28].textContent;
    let title = thd[29].textContent;
    let honor = thd[30].textContent;
    let domain = thd[14].textContent;
    let email  = thd[17].textContent;
    let office_number = thd[20].textContent;
    let phone_number = thd[23].textContent;
    let edu_exp = thd[26].textContent;
    let teacher_id = thd[31].textContent;
    let object_id = thd[32].textContent;
    let department = thd[33].textContent;
    let data = {
        "name": name,
        "birth_year":birth_year,
        "domain":domain,
        "email": email,
        "office_number": office_number,
        "phone_number": phone_number,
        "edu_exp": edu_exp,
        "school": school,
        "institution": institution,
        'department':department,
        "title": title,
        "honor": honor,
        "teacher_id": teacher_id,
        "object_id":object_id
    };
    $.ajax({
        type: "post",
        url: "/data_preservation",
        data: data,
        dataType: "json",
        success: function (response) {
            console.log(response);
            toggle_alert(true, response.message);

        },
        error: function (error) {
            console.log(error);
            toggle_alert(false, "操作失败，请稍后再试");
        }
    })

});

$(".ignore").on("click",(e)=>{
    console.log("ignore");
    let tbody = $(".displaying");
    thd = tbody.children().children();
    let object_id = thd[32].textContent;
    data = {"object_id":object_id};
    $.ajax({
        type: "post",
        url: "/data_ignore",
        data: data,
        dataType: "json",
            success: function (response) {
            console.log(response);

        },
        error: function (error) {
            console.log(error);
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

