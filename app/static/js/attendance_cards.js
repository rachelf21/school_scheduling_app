function test() {
  console.log("it is working");
}

function get_today() {
  var today = new Date();
  month = ("0" + (today.getMonth() + 1)).slice(-2);
  day = ("0" + today.getDate()).slice(-2);
  year = today.getFullYear();
  today_date = year + "-" + month + "-" + day;
  return today_date;
}

function mark_present(id) {
  id = id - 1;
  var s = document.getElementById("students-" + id + "-status");
  s.value = "P";
  s.style.color = "black";
  s.setAttribute("style", "background-color: none");
  var n = document.getElementById("students-" + id + "-student_name");
  n.style.color = "black";
  n.setAttribute("style", "background-color: none");
  //var student_td = n.parentElement.parentElement;
  //student_td.setAttribute("style", "color: black; font-weight: normal; ");
  //student_td.classList.remove("mark");
  var present_icon = document.getElementById("mark_present_" + parseInt(id + 1));
  var absent_icon = document.getElementById("mark_absent_" + parseInt(id + 1));
  var late_icon = document.getElementById("mark_late_" + parseInt(id + 1));
  var card = document.getElementById("card" + id);

  console.log(present_icon);
  if (present_icon.style.background == "rgb(92, 184, 92)") {
    present_icon.style.background = "rgba(200, 200, 200,.5)";
    card.style.background = "whitesmoke";
    card.style.borderColor = "rgba(0, 0, 0, 0.125)";
  } else {
    present_icon.style.background = "rgb(92, 184, 92)";
    card.style.background = "#eeffee";
    card.style.borderColor = "rgba(0, 255, 0, 0.65)";
    absent_icon.style.background = "rgba(200, 200, 200,.5)";
    late_icon.style.background = "rgba(200, 200, 200,.5)";
  }
}

function mark_absent(id) {
  id = id - 1;
  s = document.getElementById("students-" + id + "-status");
  s.value = "A";
  s.style.color = "rgb(220, 20, 60)";
  s.setAttribute("style", "background-color: " + PaleRed);
  n = document.getElementById("students-" + id + "-student_name");
  n.style.color = "rgb(220, 20, 60)";
  n.setAttribute("style", "background-color: " + PaleRed);
  //   var student_td = n.parentElement.parentElement;
  //   student_td.setAttribute("style", "color: rgb(220, 20, 60); font-weight: bold; "); //overriden by later style
  //student_td.setAttribute("class", "mark");
  var absent_icon = document.getElementById("mark_absent_" + parseInt(id + 1));
  var present_icon = document.getElementById("mark_present_" + parseInt(id + 1));
  var late_icon = document.getElementById("mark_late_" + parseInt(id + 1));
  var card = document.getElementById("card" + id);

  console.log(absent_icon);
  if (absent_icon.style.background == "rgb(220, 20, 60)") {
    //217, 83, 79
    absent_icon.style.background = "rgba(200, 200, 200,.5)";
    card.style.background = "whitesmoke";
    card.style.borderColor = "rgba(0, 0, 0, 0.125)";
  } else {
    absent_icon.style.background = "rgb(220, 20, 60)";
    card.style.background = "MistyRose";
    card.style.borderColor = "rgba(255, 0, 0, 0.2)";
    present_icon.style.background = "rgba(200, 200, 200,.5)";
    late_icon.style.background = "rgba(200, 200, 200,.5)";
  }
}

function mark_late(id) {
  id = id - 1;
  var s = document.getElementById("students-" + id + "-status");
  s.value = "L";
  s.style.color = "blue";
  s.setAttribute("style", "background-color: none");
  var n = document.getElementById("students-" + id + "-student_name");
  n.style.color = "black";
  n.setAttribute("style", "background-color: none");
  //   var student_td = n.parentElement.parentElement;
  //   student_td.setAttribute("style", "color: rgb(3, 132, 252); font-weight: normal; ");
  //   student_td.classList.remove("mark");
  var absent_icon = document.getElementById("mark_absent_" + parseInt(id + 1));
  var present_icon = document.getElementById("mark_present_" + parseInt(id + 1));
  var late_icon = document.getElementById("mark_late_" + parseInt(id + 1));
  var card = document.getElementById("card" + id);

  console.log(absent_icon);
  if (late_icon.style.background == "rgb(2, 117, 216)") {
    late_icon.style.background = "rgba(200, 200, 200,.5)";
    card.style.background = "whitesmoke";
    card.style.borderColor = "rgba(0, 0, 0, 0.125)";
  } else {
    late_icon.style.background = "rgb(2, 117, 216)";
    card.style.background = "Lightcyan";
    card.style.borderColor = "rgba(0, 0, 255, 0.2)";
    absent_icon.style.background = "rgba(200, 200, 200,.5)";
    present_icon.style.background = "rgba(200, 200, 200,.5)";
  }
}

function mark_clear(id) {
  id = id - 1;
  var c = document.getElementById("students-" + id + "-comment");
  c.value = "";
  var s = document.getElementById("students-" + id + "-status");
  s.value = "";
  s.style.color = "black";
  s.setAttribute("style", "background-color: none");
  var n = document.getElementById("students-" + id + "-student_name");
  n.style.color = "black";
  n.setAttribute("style", "background-color: none");
  var student_td = n.parentElement.parentElement;
  student_td.setAttribute("style", "color: black; font-weight: medium; ");
  student_td.classList.remove("mark");
  var checks = document.getElementsByName("check");
  checks[id].style.display = "none";
  var exes = document.getElementsByName("ex");
  exes[id].style.display = "none";
  var lates = document.getElementsByName("late");
  lates[id].style.display = "none";
  var empty = document.getElementsByName("empty");
  empty[id].style.display = "block";
}

var toggle = 1;
var comment_on = 0;

function present(count) {
  toggle = -toggle;

  var checks = document.getElementsByName("check");
  var exes = document.getElementsByName("ex");
  var lates = document.getElementsByName("late");
  var empties = document.getElementsByName("empty");
  $("#all").css("background", "whitesmoke");

  for (i = 0; i < count; i++) {
    var s = document.getElementById("students-" + i + "-status");
    var n = document.getElementById("students-" + i + "-student_name");
    var card = document.getElementById("card" + parseInt(i));
    var absent_icon = document.getElementById("mark_absent_" + parseInt(i + 1));
    var present_icon = document.getElementById("mark_present_" + parseInt(i + 1));
    var late_icon = document.getElementById("mark_late_" + parseInt(i + 1));

    s.setAttribute("style", "background-color: none");
    n.setAttribute("style", "background-color: none");
    n.setAttribute("style", "border-color: rgba(0, 0, 0, 0.125)");

    //var student_td = n.parentElement.parentElement;

    if (toggle < 0) {
      s.value = "P";
      card.style.background = "#eeffee";
      card.style.borderColor = "rgba(0, 255, 0, .65)";
      present_icon.style.background = "rgb(92, 184, 92)";
      absent_icon.style.background = "rgba(200, 200, 200,.5)";
      late_icon.style.background = "rgba(200, 200, 200,.5)";
      $("#all").css("background", "rgba(200, 200, 200,.5)");

      //student_td.setAttribute("style", "color: black; font-weight: normal; ");
      //student_td.classList.remove("mark");
    } else {
      s.value = "";
      card.style.background = "whitesmoke";
      card.style.borderColor = "rgba(0, 0, 0, 0.125)";
      present_icon.style.background = "rgba(200, 200, 200,.5)";
      absent_icon.style.background = "rgba(200, 200, 200,.5)";
      late_icon.style.background = "rgba(200, 200, 200,.5)";
      $("#all").css("background", "rgb(92, 184, 92)");

      //student_td.setAttribute("style", "color: black; font-weight: medium; ");
      //student_td.classList.remove("mark");
    }
  }
}

function set_value_comment(id) {
  var element = document.getElementById("card_comment_" + id);
  document.getElementById("current_id").value = id;
  console.log("comment " + id);
  var student = document.getElementById("students-" + parseInt(id - 1) + "-student_name");
  var comment_element = document.getElementById("students-" + parseInt(id - 1) + "-comment");
  var n = document.getElementById("current_name");
  n.value = student.value;
  console.log(n.value);
}

function add_comment() {
  var comment = document.getElementById("new_comment").value;
  //comment = comment.replace(/'/g, "");
  if (comment === null || comment == "") {
    console.log("null commment");
    return;
  } else {
    var id = document.getElementById("current_id").value;
    var element = document.getElementById("card_comment_" + id);
    console.log("element " + element);
    element.childNodes[0].innerHTML = comment;
    console.log("comment = " + comment);
    element.style.display = "block";
    var comment_element = document.getElementById("students-" + parseInt(id - 1) + "-comment");
    comment_element.value = comment;
  }
}

function delete_comment(id) {
  console.log("comment");
  var element = document.getElementById("card_comment_" + id);
  element.childNodes[0].innerHTML = "";
  element.style.display = "none";
  var c = document.getElementById("students-" + parseInt(id - 1) + "-comment");
  c.value = "";
}

function edit_attendance(id, email) {
  id = id - 1;
  console.log(email);
  var changed_status = document.getElementById("students-" + id + "-status").value;
  var changed_comment = document.getElementById("students-" + id + "-comment").value;
  changed_comment = changed_comment.replace(/'/g, "") + " -edited";
  console.log(changed_comment);
  window.location.href = "/edit_attendance/" + date + "/" + courseid + "/" + email + "/" + changed_status + "/" + changed_comment;
}

function change_color(e) {
  var ele = e.target;
  var id = ele.id;
  var x = id.indexOf("-", 9);
  var y = id.substring(9, x);
  var name = "students-" + y + "-student_name";
  var n = document.getElementById(name);

  var selected = ele.value;

  if (selected == "A") {
    ele.style.color = "rgb(220, 20, 60)";
    ele.setAttribute("class", "mark");
    n.style.color = "rgb(220, 20, 60)";
    n.setAttribute("class", "mark");
  } else if (selected == "L") {
    ele.style.color = "blue";
    n.style.color = "blue";
    n.classList.remove("mark");
    ele.classList.remove("mark");
  } else {
    ele.style.color = "black";
    n.style.color = "black";
    n.classList.remove("mark");
    ele.classList.remove("mark");
  }
}

function view_lessons() {
  var x = "/lessons/" + courseid;
  return '<div style="float:left"> <a class="font-weight-normal" href="' + x + '"> <br> View Lessons</a>';
}
