//设置当前学校，学院
let cur_school;
let cur_institution;

//获取所有学校
$.ajax({
    url:"/get_school",
    type:"GET",
    dataType:"json"
}).done(function (data) {
    console.log(data)
    if(data["success"] == true){
        var schools = data["school"];
        console.log("schools", schools);
        var html = ``;

        for(var i = 0; i < schools.length; i++){
            var school = schools[i];
            html += '<option>'+ school + '</option>';
        }
        $('#select_school').html(html);

    //    选取默认的学校对其学院进行加载
        loadInstitution();
    }
})


/**
 * 当学校下拉框发生变化时，加载当前学校的所有学院数据
 */
$("#select_school").on("change", function () {
    loadInstitution();
})


/**
 * 加载当前学校的所有学院数据
 */
function loadInstitution(){
    cur_school = $('#select_school').children("option:selected").text();
    console.log("cur_school", cur_school);
    getInstitutions(cur_school);
}


/**
 * 根据学校名获取其所有学院信息
 * @param {String} school 学校名
 */
function getInstitutions(school){
    $.ajax({
        type: "POST",
        url: "/get_institution",
        data: {"school" : school},
        dataType: "json",
        success: function (response) {
            // console.log(response);
            if(response.success == false){
                return toggle_alert(false, "", response.message);
            }
            institution_list = response["institution"]
            setInstitution(institution_list);
        },
        error: function(error){
            console.error(error);
            toggle_alert(false, "", "服务器连接失败,请稍后再试");
        }
    });
}


/**
 * 将学院信息填充到下拉框中
 * @param {object} institution_list 学院数据 [{"name":xxx},...]
 */
function setInstitution(institution_list){
    if(institution_list.length <= 0){
        alert("学院数据为空");
        return;
    }
    let options = "";
    for (let i = 0; i < institution_list.length; i++) {
        options += `<option>${institution_list[i]}</option>`;
    }
    $("#select_institution").html(options);


//    将学院信息填充到下拉框后， 加载table中的信息
    cur_school = $('#select_school').children("option:selected").text();
    cur_institution = $('#select_institution').children("option:selected").text();

    console.log("cur_school, cur_institution", cur_school, cur_institution);
    getTeachers(cur_school, cur_institution);
}


/**
 * 当学院下拉框发生变化时，重新加载教师
 */
$("#select_institution").on("change", function () {
    cur_school = $('#select_school').children("option:selected").text();
    cur_institution = $('#select_institution').children("option:selected").text();

    getTeachers(cur_school, cur_institution);
})


/**
 * 根据学校名和学院名异步获取其下的所有教师名字和id，并加载
 * @param school， institution
 */
function getTeachers(school, institution) {
    $.ajax({
        type: "POST",
        url: "/get_teacher",
        data:{
            "school": school,
            "institution": institution,
        },
        dataType: "json",
    }).done(function (data) {
        console.log(data)
        console.log(data.success)
        if(data.success == true){
            teacher_list = data["teacher_list"];

            insert_html = ``;

            for(var i = 0; i < teacher_list.length; i++){
                insert_html += `
                <tr>
                    <th scope="col">${i}</th>
                    <th scope="col">${school}</th>
                    <th scope="col">${institution}</th>
                    <th scope="col" class="teacher">${teacher_list[i]["name"]}</th>
                    <th scope="col" class="input_row">
                        <input class="input_department" data-id=${teacher_list[i]["id"]} onchange="change(this)" value=${teacher_list[i]["department"]}>
                    </th>
                </tr>
                `
            }


            let $tr = $("#flag");
            console.log("------------------before add");
            // 删除HTML页面中现有的教师以及系的信息
            $tr.siblings("tr").remove();
            //加载新的信息
            $tr.after(insert_html);

        }else{
            console.log("error  ", data["message"]);
        }
    })
}

// $("#input_department").on("change", function () {
//     // console.log("")
//
// })


/**
 * 设置访问标志
 */
function change(e) {
    e.setAttribute("is_change", "1");
    // console.log(e.getAttribute("is_change"))
}


/**
 * 保存被更改的系的信息
 */
function save_department(){
    temp = $("#flag").siblings();
    console.log("--------");

    dept_info = [];
    for(var i = 0; i < temp.length; i++){
        // 获取当前的教师和系
        is_change = temp[i].getElementsByClassName("input_department")[0].getAttribute("is_change");
        teacher_id = temp[i].getElementsByClassName("input_department")[0].getAttribute("data-id");
        department = temp[i].getElementsByClassName("input_row")[0].getElementsByClassName("input_department")[0].value;

        // console.log(teacher);
        // console.log(department);
        if(is_change == "1"){
            // console.log(typeof (department));
            dept_info.push({
                "teacher_id": teacher_id,
                "department": department
            });
        }
    }

    dept_dict = {
        "dept_info": JSON.stringify(dept_info)
    }

    console.log(dept_dict);
    $.ajax({
        type: "POST",
        url: "/save_dept",
        data: dept_dict,
        dataType: "json",
        success:function (response) {
            console.log("插入成功")
            toggle_alert("更新成功")
        },
        error: function (response) {
            console.log("插入失败")
            toggle_alert("更新失败")
        }
    })
}

