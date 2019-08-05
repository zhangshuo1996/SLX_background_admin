function get_institution() {
    //根据学校名获取此学校的所有学院名
    var  myselect=document.getElementById("school");
    var index= myselect.selectedIndex ;
    var school = myselect.options[index].text;
    //发送学校名
    let data = {"school":school}
    $.ajax({
    type: "post",
    url: "/get_institution",
    dataType: "json",
    data: data,
    success: function (response) {
        //将学院下拉列表清空，重新添加新的学院列表
        document.getElementById("institution").length=0;
        $("#institution").append("<option>"+" "+"</option>")
        for(var i=0; i<response.institution.length; i++){
            $("#institution").append("<option>"+response.institution[i]+"</option>")
        }
    },
    error: function(response){
        toggle_alert(response.success, "", response.message);
    }
});

}


function  teacher_search() {
    /**根据学校名、学院名和老师姓名获取教师的信息*/
    //获取当前学校名和学院名
    var school_select = document.getElementById("school");
    var school_index = school_select.selectedIndex ;
    var school = school_select.options[school_index].text;
    var institution_select = document.getElementById("institution");
    var institution_index = institution_select.selectedIndex;
    var institution = institution_select.options[institution_index].text;
    var teacher = $("#teacher").val();
    if(teacher == ""){
        toggle_alert("False", "", "教师名不能为空！");
        return false;
    }
    let data = {"school":school,"institution":institution, "teacher":teacher};
    $.ajax({
        type:"POST",
        url:"/get_teacher_info",
        data: data,
        dataType: "json",
        success: function (response) {
            if(response.success) {
                //将获取到的教师信息在表格中展示
                $("#id").val(response.teacher_info['id'])
                $("#name").val(response.teacher_info['name'])
                $("#university").val(response.teacher_info['university'])
                $("#college").val(response.teacher_info['college'])
                $("#title").val(response.teacher_info['title'])
                $("#email").val(response.teacher_info['email'])
                $("#birth_year").val(response.teacher_info['birth_year'])
                $("#phone_number").val(response.teacher_info['phone_number'])
                $("#office_number").val(response.teacher_info['office_number'])
                $("#edu_exp").val(response.teacher_info['edu_exp'])
            }
            else {
                toggle_alert("False", "", "没有此老师信息！");
            }
        },
        error: function(){
            toggle_alert("False", "", "请求失败！");
    }
    });
}

function update_teacher() {
    //获取列表中教师的信息
    let id = $("#id").val()
    let name = $("#name").val()
    let school = $("#university").val()
    let institution = $("#college").val()
    let title = $("#title").val()
    let email = $("#email").val()
    let birth_year = $("#birth_year").val()
    let phone_number = $("#phone_number").val()
    let office_number = $("#office_number").val()
    let edu_exp = $("#edu_exp").val()
    if(name == ""){
        toggle_alert("False", "", "教师名不能为空！");
        return false;
    }
    if(school==""){
        toggle_alert("False", "", "学校名不能为空！");
        return false;
    }
    if(institution==""){
        toggle_alert("False", "", "学院名不能为空！");
        return false;
    }
    var re =  /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
    if(email!=""&&!re.test(email)){
        toggle_alert("False", "", "请输入正确的邮箱！");
        return false;
    }
    var re = /^1\d{10}$/;
    if(phone_number!=""&&!re.test(phone_number)){
        toggle_alert("False", "", "请输入正确的手机号码！");
        return false;
    }
    let data = {"id":id,"name":name, "school":school, "institution":institution, "title":title, "email":email, "birth_year":birth_year,"office_number":office_number,
    "phone_number":phone_number,"edu_exp":edu_exp}
    $.ajax({
        type:"POST",
        url:"/update_teacher",
        data: data,
        dataType: "json",
        success: function (response) {
            if(response.success) {
                toggle_alert(response.success, "", response.message);
            }
            else {
                toggle_alert(response.success, "", response.message);
            }
        },
        error: function(){
            toggle_alert("False", "", "请求失败!");
    }
    });
}

function delete_teacher() {
   //根据用户id删除某个用户
    if(confirm('确定要删除此教师吗?')) {
        let id = $("#id").val();
        let data = {"id": id};
        $.ajax({
            type: "POST",
            url: "/delete_teacher",
            data: data,
            dataType: "json",
            success: function (response) {
                if (response.success) {
                    toggle_alert(response.success, "", response.message);
                }
                else {
                    toggle_alert(response.success, "", response.message);
                }
            },
            error: function () {
                toggle_alert("False", "", "请求失败!");
            }
        });
    }
}

function add_teacher() {
    let name = $("#name").val()
    let school = $("#university").val()
    let institution = $("#college").val()
    let title = $("#title").val()
    let email = $("#email").val()
    let birth_year = $("#birth_year").val()
    let phone_number = $("#phone_number").val()
    let office_number = $("#office_number").val()
    let edu_exp = $("#edu_exp").val()
    if(name == ""){
        toggle_alert("False", "", "教师名不能为空！");
        return false;
    }
    if(school==""){
        toggle_alert("False", "", "学校名不能为空！");
        return false;
    }
    if(institution==""){
        toggle_alert("False", "", "学院名不能为空！");
        return false;
    }
    var re =  /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
    if(email!=""&&!re.test(email)) {
        toggle_alert("False", "", "请输入正确的邮箱！");
        return false;
    }
    var re = /^1\d{10}$/;
    if(phone_number!=""&&!re.test(phone_number)){
        toggle_alert("False", "", "请输入正确的手机号码！");
        return false;
    }
    let data = {"name":name, "school":school, "institution":institution, "title":title, "email":email, "birth_year":birth_year,"office_number":office_number,
    "phone_number":phone_number,"edu_exp":edu_exp}
    let teacher_data = {"teacher":name, "school":school, "institution":institution}
    console.log(teacher_data)
    console.log(data)
    //判断数据库中是否存在此老师信息
    $.ajax({
        type:"POST",
        url:"/get_teacher_info",
        data: teacher_data,
        dataType: "json",
        success: function (response) {
            console.log(response.success)
            if (response.success) {
                if(confirm('已存在此老师信息，是否继续添加?')) {
                    $.ajax({
                        type: "POST",
                        url: "/add_teacher",
                        data: data,
                        dataType: "json",
                        success: function (response) {
                            if (response.success) {
                                toggle_alert(response.success, "", response.message);
                            }
                            else {
                                toggle_alert(response.success, "", response.message);
                            }
                        },
                        error: function () {
                            toggle_alert("False", "", "请求失败!");
                        }
                    });
                }
            }
            else{
                $.ajax({
                        type: "POST",
                        url: "/add_teacher",
                        data: data,
                        dataType: "json",
                        success: function (response) {
                            if (response.success) {
                                toggle_alert(response.success, "", response.message);
                            }
                            else {
                                toggle_alert(response.success, "", response.message);
                            }
                        },
                        error: function () {
                            toggle_alert("False", "", "请求失败!");
                        }
                    });
            }
        }
    });
}

function clear_info() {
    //清空教师信息
    $("#name").val("");
    $("#university").val("");
    $("#college").val("");
    $("#title").val("");
    $("#email").val("");
    $("#birth_year").val("");
    $("#phone_number").val("");
    $("#office_number").val("");
    $("#edu_exp").val("");
}