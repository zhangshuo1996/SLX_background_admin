
function myFunction() {
  // 声明变量
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value;
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  // 循环表格每一行，查找匹配项
  for (i = 1; i < tr.length; i++) {
          td = tr[i].getElementsByTagName("td")[0].innerHTML + tr[i].getElementsByTagName("td")[1].innerHTML +tr[i].getElementsByTagName("td")[2].innerHTML+tr[i].getElementsByTagName("td")[3].innerHTML+tr[i].getElementsByTagName("td")[4].innerHTML;
          if (td) {
              if (td.indexOf(filter) > -1) {
                  tr[i].style.display = "";
              } else {
                  tr[i].style.display = "none";
              }
          }
      }
}
function add_newuser() {
    let name = $("#name").val();
    let tel_number = $("#tel_number").val();
    let email = $("#email").val();
    let school = $("#school").val();
    var  myselect=document.getElementById("type");
    var index=myselect.selectedIndex ;
    var type = myselect.options[index].text;
    if(name==""){
        toggle_alert("False", "", "用户名不能为空！");
        return false;
    }
    if(tel_number==""){
        toggle_alert("False", "", "联系电话不能为空！");
        return false;
    }
    var re = /^1\d{10}$/;
    if (!re.test(tel_number)) {
        toggle_alert("False", "", "请输入正确的联系号码！");
        return false;
    }
    if(email==""){
        toggle_alert("False", "", "用户邮箱不能为空！");
        return false;
    }
     var re =  /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
    if(!re.test(email)){
        toggle_alert("False", "", "请输入正确的邮箱！");
        return false;
    }
    if(school==""){
        toggle_alert("False", "", "所在学校不能为空！");
        return false;
    }

    let data = {"name": name, "tel_number": tel_number, "email": email, "school": school, "type": type}
    $.ajax({
    type: "post",
    url: "/add_user",
    data: data,
    dataType: "json",
    success: function (response) {
        console.log(response);
        toggle_alert(response.success, "", response.message);
         $("#name").val("");
         $("#tel_number").val("");
         $("#email").val("");
         $("#school").val("");
    },
    error: function(response){
        console.log(response);
        toggle_alert(response.error, "", response.message);
    }
});
}

function update_user() {
    let id = $("#id").val();
    let name = $("#name").val();
    let tel_number = $("#tel_number").val();
    let email = $("#email").val();
    let school = $("#school").val();
    var  myselect=document.getElementById("type");
    var index=myselect.selectedIndex ;
    var type = myselect.options[index].text;
    if(name==""){
        toggle_alert("False", "", "用户名不能为空！");
        return false;
    }
    if(tel_number==""){
        toggle_alert("False", "", "联系电话不能为空！");
        return false;
    }
    var re = /^1\d{10}$/;
    if (!re.test(tel_number)) {
        toggle_alert("False", "", "请输入正确的联系号码！");
        return false;
    }
    if(email==""){
        toggle_alert("False", "", "用户邮箱不能为空！");
        return false;
    }
     var re =  /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
    if(!re.test(email)){
        toggle_alert("False", "", "请输入正确的邮箱！");
        return false;
    }

    let data = {"id":id, "name": name, "tel_number": tel_number, "email": email, "school": school, "type": type}
    console.log(data)
    $.ajax({
    type: "post",
    url: "/update_user",
    data: data,
    dataType: "json",
    success: function (response) {
        console.log(response);
        toggle_alert(response.success, "", response.message);
         $("#name").val("");
         $("#tel_number").val("");
         $("#email").val("");
         $("#school").val("");
    },
    error: function(response){
        console.log(response);
        toggle_alert(response.error, "", response.message);
    }
});
}

function edit(e) {
    tds = e.parent().siblings();
    let name = tds[0].innerText;
    let tel_number = tds[1].innerText;
    let email = tds[2].innerText;
    let school = tds[3].innerText;
    let type = tds[4].innerText;
    let id = tds[5].innerText;
    $("#name").val(name);
    $("#tel_number").val(tel_number);
    $("#email").val(email);
    $("#school").val(school);
    $("#id").val(id);
    console.log(id)
    var  myselect=document.getElementById("type");
    myselect.value=type
}

function del_user(){
    if(confirm('确定要删除此用户吗?')) {
        let id = $("#id").val();
        let data = {"id":id}
        $.ajax({
            type: "post",
            url: "/del_user",
            data: data,
            dataType: "json",
            success: function (response) {
                console.log(response);
                toggle_alert(response.success, "", response.message);
            },
            error: function (response) {
                console.log(response);
                toggle_alert(response.error, "", response.message);
            }
        });
    }
    else{
        return false;
    }
}
