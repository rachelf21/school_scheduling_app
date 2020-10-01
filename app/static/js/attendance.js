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
  var student_td = n.parentElement.parentElement;
  student_td.setAttribute("style", "color: black; font-weight: normal; ");
  student_td.classList.remove("mark");
  var checks = document.getElementsByName("check");
  checks[id].style.display = "block";
  var exes = document.getElementsByName("ex");
  exes[id].style.display = "none";
  var lates = document.getElementsByName("late");
  lates[id].style.display = "none";
  var empty = document.getElementsByName("empty");
  empty[id].style.display = "none";
}

function mark_absent(id) {
  id = id - 1;
  s = document.getElementById("students-" + id + "-status");
  s.value = "A";
  s.style.color = "Crimson";
  s.setAttribute("style", "background-color: " + PaleRed);
  n = document.getElementById("students-" + id + "-student_name");
  n.style.color = "Crimson";
  n.setAttribute("style", "background-color: " + PaleRed);
  var student_td = n.parentElement.parentElement;
  student_td.setAttribute("style", "color: Crimson; font-weight: bold; "); //overriden by later style
  //student_td.setAttribute("class", "mark");
  var checks = document.getElementsByName("check");
  checks[id].style.display = "none";
  var exes = document.getElementsByName("ex");
  exes[id].style.display = "block";
  var lates = document.getElementsByName("late");
  lates[id].style.display = "none";
  var empty = document.getElementsByName("empty");
  empty[id].style.display = "none";
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
  var student_td = n.parentElement.parentElement;
  student_td.setAttribute("style", "color: rgb(3, 132, 252); font-weight: normal; ");
  student_td.classList.remove("mark");
  var checks = document.getElementsByName("check");
  checks[id].style.display = "none";
  var exes = document.getElementsByName("ex");
  exes[id].style.display = "none";
  var lates = document.getElementsByName("late");
  lates[id].style.display = "block";
  var late_icons = document.getElementsByName("late_icon");
  var empty = document.getElementsByName("empty");
  empty[id].style.display = "none";
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
function present(count) {
  toggle = -toggle;

  var checks = document.getElementsByName("check");
  var exes = document.getElementsByName("ex");
  var lates = document.getElementsByName("late");
  var empties = document.getElementsByName("empty");

  for (i = 0; i < count; i++) {
    var s = document.getElementById("students-" + i + "-status");
    var n = document.getElementById("students-" + i + "-student_name");
    s.setAttribute("style", "background-color: none");
    n.setAttribute("style", "background-color: none");
    var student_td = n.parentElement.parentElement;

    if (toggle < 0) {
      s.value = "P";
      checks[i].style.display = "block";
      exes[i].style.display = "none";
      lates[i].style.display = "none";
      empties[i].style.display = "none";
      student_td.setAttribute("style", "color: black; font-weight: normal; ");
      student_td.classList.remove("mark");
    } else {
      s.value = "";
      exes[i].style.display = "none";
      checks[i].style.display = "none";
      lates[i].style.display = "none";
      empties[i].style.display = "block";
      student_td.setAttribute("style", "color: black; font-weight: medium; ");
      student_td.classList.remove("mark");
    }
  }
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
    ele.style.color = "Crimson";
    ele.setAttribute("class", "mark");
    n.style.color = "Crimson";
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
