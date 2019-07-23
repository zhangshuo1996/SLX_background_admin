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
    console.log(data)
    $.ajax({
        type:"POST",
        url:"/get_teacher_info",
        data: data,
        dataType: "json",
        success: function (response) {
            if(response.success) {
                //将获取到的教师信息在表格中展示
                $("#name").val(response.teacher_info['name'])
                $("#university").val(response.teacher_info['university'])
                $("#college").val(response.teacher_info['college'])
                $("#title").val(response.teacher_info['title'])
                $("#field").val(response.teacher_info['field'])
                $("#birthyear").val(response.teacher_info['birthyear'])
                $("#tel_num").val(response.teacher_info['tel_num'])
                $("#mobile_phone").val(response.teacher_info['mobile_phone'])
                $("#edu-exp").val(response.teacher_info['edu-exp'])
            }
            else {
                toggle_alert("False", "", "没有此老师信息！");
            }
        },
        error: function(response){
            toggle_alert("False", "", "请求失败！");
    }
    });
}