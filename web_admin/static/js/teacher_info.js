/**
/**
 * 点击右侧的商务和时间那一行，在左边将信息展示出来
 */
$(".display").on("click",(e)=>{
    //通过e来获取点击的那一行，e代表那个tr
    let $target = $(e.target);
    e = $target.parent();
    let tbody = $(".displaying");
    thd = tbody.children().children();
    let teacher_id = e.attr('data-teacher_id');
    let object_id = e.attr('data-_id');
    //将左侧表格中字体颜色设置为黑色，否则在一次改变为红色后，这个td将变为红色
    for (var i=1; i<=37; i += 3)
        {
            $(thd[i]).css("color","black");
            $(thd[i+1]).css("color","black");

        }
    if(teacher_id !== "None") {
        let type = $(".type");
        type.text("具体信息（修改信息）");
        //从数据库中将这个老师的数据取出来
        let data = {"teacher_id": teacher_id,"_id":object_id};
        console.log(data);
        $.ajax({
            type: "post",
            url: "/get_info_by_tid",
            data: data,
            dataType: "json",
            success: function (response) {

                console.log("succeed");
                console.log(response);
                let from_basic = response["teacher_info_from_basic"];
                let from_feedback = response["teacher_info_from_feedback"];
                //将一些要提交到数据库但不提交的数据写道tbody的属性中
                tbody.attr("data-teacher_id",teacher_id);
                tbody.attr("data-object_id",object_id);
                tbody.attr("data-school",from_feedback["school"]);
                tbody.attr("data-institution",from_feedback["institution"]);
                tbody.attr("department",from_feedback["department"]);
                 //填充到左边table的第二栏
                thd[1].textContent = from_basic["name"];
                thd[4].textContent = from_basic["gender"];
                thd[7].textContent = from_basic["birth_year"];
                thd[10].textContent = from_basic["school"] + from_basic["institution"]
                    +from_basic["department"];
                thd[13].textContent = from_basic["title"];
                thd[16].textContent = from_basic["position"];
                thd[19].textContent = from_basic["honor_title"];
                thd[22].textContent = from_basic["domain"];
                thd[25].textContent = from_basic["email"];
                thd[28].textContent = from_basic["office_number"];
                thd[31].textContent = from_basic["phone_number"];
                thd[34].textContent = from_basic["edu_exp"];
                thd[37].textContent = from_basic["work_exp"];
                //填充到左边第三栏
                thd[2].textContent = from_feedback["name"];
                thd[5].textContent = from_feedback["gender"];
                thd[8].textContent = from_feedback["birth_year"];
                thd[11].textContent = from_feedback["school"] + from_feedback["institution"]
                    +from_feedback["department"];
                thd[14].textContent = from_feedback["title"];
                thd[17].textContent = from_feedback["position"];
                thd[20].textContent = from_feedback["honor_title"];
                thd[23].textContent = from_feedback["domain"];
                thd[26].textContent = from_feedback["email"];
                thd[29].textContent = from_feedback["office_number"];
                thd[32].textContent = from_feedback["phone_number"];
                thd[35].innerHTML = from_feedback["edu_exp"];
                thd[38].innerHTML = from_feedback["work_exp"];
                for (var i=1; i<=37; i += 3)
                {
                    if(thd[i].textContent !== thd[i+1].textContent){
                        $(thd[i+1]).css("color","red");
                    }
                }
            },
            error: function (error) {
            console.log("失败");
            console.log(error);
        }
        });

    }
    //新增记录的处理
    else{
                 //将选中的这一行的数据，即商务提交的教师信息取出来
    let name = e.attr('data-name');
    let gender = e.attr('data-gender');
    let school = e.attr('data-school');
    let institution = e.attr('data-institution');
    let title = e.attr('data-title');
    let position = e.attr('data-position');
    let honor_str = e.attr('data-honor_title');
    let email = e.attr('data-email');
    let phone_number = e.attr('data-phone_number');
    let office_number = e.attr('data-office_number');
    let edu_exp = e.attr('data-edu_exp');
    let teacher_id = e.attr('data-teacher_id');
    let birth_year = e.attr('data-birth_year');
    let object_id = e.attr('data-_id');
    let domain = e.attr("data-domain");
    let department = e.attr("data-department");
    let work_exp = e.attr("data-work_exp");

    //现在决定第二第三列的数据都从数据库中取出，因为feedback中的数据字段不同，而决定将两列数据格式固定，所以需要将feedbakc中缺省的字段从
    //数据库中取出，以分辨是它它发来的是没有这个字段，还是发来的内容中这个字段内容为空
    //将取出的信息填充到左边table的第三列，所以从thd[2]开始,逐个加3，就都是修改第三列

    thd[2].textContent = name;
    thd[5].textContent = gender;
    if(birth_year==="None") {
        thd[8].textContent = "";
    }
    else thd[8].textContent = birth_year;
    thd[11].textContent = school+institution+department;
    thd[14].textContent = title;
    thd[17].textContent = position;
    thd[20].textContent = honor_str;
    thd[23].textContent = domain;
    thd[26].textContent = email;
    thd[29].textContent = office_number;
    thd[32].textContent = phone_number;
    if(edu_exp==="None") {
        thd[35].textContent = "";
    }
    else thd[35].innerHTML = edu_exp;
    thd[38].innerHTML = work_exp;
    //隐藏数据，用于点击保存时提交给后台
    tbody.attr("data-school",school);
    tbody.attr("data-institution",institution);
    // 原本title和honor在一起显示，所以数据放在了这里
    tbody.attr("data-title",title);
    tbody.attr("data-teacher_id",teacher_id);
    tbody.attr("data-object_id",object_id);
    tbody.attr("data-department",department);

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
                thd[28].textContent="";
                thd[31].textContent ="";
                thd[34].textContent = ""
    }

});

$(".preservation").on("click",(e)=>{
    //将商务提交的数据取出来
    console.log("preservation");
    let tbody = $(".displaying");
    thd = tbody.children().children();
    let name= thd[2].textContent;
    let gender = thd[5].textContent;
    let birth_year = thd[8].textContent;
    let school = tbody.attr("data-school");
    let institution = tbody.attr("data-institution");
    let department = tbody.attr("data-apartment");
    let title = thd[14].textContent;
    let position = thd[17].textContent;
    let honor_str = thd[20].textContent;
    let domain = thd[23].textContent;
    let email = thd[26].textContent;
    let office_number = thd[29].textContent;
    let phone_number = thd[32].textContent;
    let edu_exp = thd[35].innerHTML;
    let work_exp = thd[38].innerHTML;
    let teacher_id = tbody.attr("data-teacher_id");
    let object_id = tbody.attr("data-object_id");


    let data = {
        "name": name,
        "gender":gender,
        "birth_year":birth_year,
        "honor_str":honor_str,
        "domain":domain,
        "email": email,
        "office_number": office_number,
        "phone_number": phone_number,
        "edu_exp": edu_exp,
        "work_exp":work_exp,
        "school": school,
        "institution": institution,
        'department':department,
        "title": title,
        "position":position,
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
    let object_id = tbody.attr('data-object_id');
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

