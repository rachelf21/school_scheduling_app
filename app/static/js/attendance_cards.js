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

  //console.log(present_icon);
  if (present_icon.style.background == "rgb(92, 184, 92)") {
    s.value = "";
    present_icon.style.background = "rgba(200, 200, 200,.5)";
    card.style.background = "whitesmoke";
    card.style.borderColor = "rgba(0, 0, 0, 0.125)";
  } else {
    s.value = "P";
    present_icon.style.background = "rgb(92, 184, 92)";
    card.style.background = "#eeffee";
    card.style.borderColor = "rgba(0, 255, 0, 0.65)";
    absent_icon.style.background = "rgba(200, 200, 200,.5)";
    late_icon.style.background = "rgba(200, 200, 200,.5)";
  }

  if (submitted == 1) {
    $("#submitted").css("display", "none");
    $("#update").css("display", "block");
  }
}

function mark_absent(id) {
  id = id - 1;
  s = document.getElementById("students-" + id + "-status");
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

  //console.log(absent_icon);
  if (absent_icon.style.background == "rgb(220, 20, 60)") {
    s.value = "";
    absent_icon.style.background = "rgba(200, 200, 200,.5)";
    card.style.background = "whitesmoke";
    card.style.borderColor = "rgba(0, 0, 0, 0.125)";
  } else {
    s.value = "A";
    absent_icon.style.background = "rgb(220, 20, 60)";
    card.style.background = "MistyRose";
    card.style.borderColor = "rgba(255, 0, 0, 0.2)";
    present_icon.style.background = "rgba(200, 200, 200,.5)";
    late_icon.style.background = "rgba(200, 200, 200,.5)";
  }
  if (submitted == 1) {
    $("#submitted").css("display", "none");
    $("#update").css("display", "block");
  }
}

function mark_late(id) {
  id = id - 1;
  var s = document.getElementById("students-" + id + "-status");
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

  //console.log(absent_icon);
  if (late_icon.style.background == "rgb(2, 117, 216)") {
    s.value = "";
    late_icon.style.background = "rgba(200, 200, 200,.5)";
    card.style.background = "whitesmoke";
    card.style.borderColor = "rgba(0, 0, 0, 0.125)";
  } else {
    s.value = "L";
    late_icon.style.background = "rgb(2, 117, 216)";
    card.style.background = "Lightcyan";
    card.style.borderColor = "rgba(0, 0, 255, 0.2)";
    absent_icon.style.background = "rgba(200, 200, 200,.5)";
    present_icon.style.background = "rgba(200, 200, 200,.5)";
  }

  if (submitted == 1) {
    $("#submitted").css("display", "none");
    $("#update").css("display", "block");
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
      card.style.borderColor = "rgba(90, 255, 90, .85)";
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

  if (submitted == 1) {
    $("#submitted").css("display", "none");
    $("#update").css("display", "block");
  }
}

function set_value_comment(id) {
  var element = document.getElementById("card_comment_" + id);
  document.getElementById("current_id").value = id;
  //console.log("comment " + id);
  var student = document.getElementById("students-" + parseInt(id - 1) + "-student_name");
  var comment_element = document.getElementById("students-" + parseInt(id - 1) + "-comment");
  var n = document.getElementById("current_name");
  n.value = student.value;
  //console.log(n.value);
}

function add_comment() {
  var comment = document.getElementById("new_comment").value;
  //comment = comment.replace(/'/g, "");
  if (comment === null || comment == "") {
    //console.log("null commment");
    return;
  } else {
    var id = document.getElementById("current_id").value;
    var element = document.getElementById("card_comment_" + id);
    //console.log("element " + element);
    element.childNodes[0].innerHTML = comment;
    //console.log("comment = " + comment);
    element.style.display = "block";
    var comment_element = document.getElementById("students-" + parseInt(id - 1) + "-comment");
    comment_element.value = comment;
  }
  if (submitted == 1) {
    $("#submitted").css("display", "none");
    $("#update").css("display", "block");
  }
}

function delete_comment(id) {
  //("comment");
  var element = document.getElementById("card_comment_" + id);
  element.childNodes[0].innerHTML = "";
  element.style.display = "none";
  var c = document.getElementById("students-" + parseInt(id - 1) + "-comment");
  c.value = "";
}

function edit_attendance(id, email) {
  id = id - 1;
  //console.log(email);
  var changed_status = document.getElementById("students-" + id + "-status").value;
  var changed_comment = document.getElementById("students-" + id + "-comment").value;
  changed_comment = changed_comment.replace(/'/g, "") + " -edited";
  //console.log(changed_comment);
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

function hide_update() {
  $("#submitted").css("display", "block");
  $("#update").css("display", "none");
  //window.location.replace = "/update_attendance";
}

// function check_for_blanks() {
//   var cards = document.getElementsByClassName("card");
//   for (i = 0; i < cards.length; i++) {
//     status = document.getElementById("students-" + i + "-status").value;
//     if (status == "") {
//       console.log("BLANKS!");
//       //$("#warning").css("display", "block");
//       alert("Cannot leave fields blank. Please mark each student as Present, Absent, or Late.");
//       //location.reload();
//       break;
//     } else {
//       window.location.replace("/record_attendance");
//     }
//   }
// }

function set_values(id, date, courseid, email, name, status, comment) {
  var i = document.getElementById("current_id2");
  i.value = id;
  var d = document.getElementById("current_date2");
  d.value = get_today();
  var c = document.getElementById("current_courseid2");
  c.value = courseid;
  var e = document.getElementById("current_email2");
  e.value = email;
  var n = document.getElementById("current_name2");
  n.value = name;
  var s = document.getElementById("new_status2");
  s.value = status;
  var t = document.getElementById("new_comment2");
  t.value = comment;
}

function edit_attendance() {
  //console.log("edit_attendance ");
  var new_status = document.getElementById("new_status2").value.toUpperCase();
  var new_comment = document.getElementById("new_comment2").value;
  new_comment = new_comment.replace(/'/g, "") + " -edited";
  //console.log("new comment = " + new_comment);
  var date = document.getElementById("current_date2").value;
  var courseid = document.getElementById("current_courseid2").value;
  var email = document.getElementById("current_email2").value;
  var name = document.getElementById("current_name2").value;

  var test = "/edit_attendance/" + date + "/" + courseid + "/" + email + "/" + new_status + "/" + new_comment;
  console.log(test);
  window.location.href = "/edit_attendance/" + date + "/" + courseid + "/" + email + "/" + new_status + "/" + new_comment;
}
//href="/send_email/{{att.email}}/{{att.courseid}}"

function color_cards_if_submitted() {
  var cards = document.getElementsByClassName("card");
  for (i = 0; i < cards.length; i++) {
    status = document.getElementById("students-" + i + "-status").value;
    if (status == "P") {
      var present_icon = document.getElementById("mark_present_" + parseInt(i + 1));
      present_icon.style.background = "rgb(92, 184, 92)";
      cards[i].style.background = "#eeffee";
      cards[i].style.borderColor = "rgba(0, 255, 0, 0.65)";
    } else if (status == "A") {
      var absent_icon = document.getElementById("mark_absent_" + parseInt(i + 1));
      absent_icon.style.background = "rgb(220, 20, 60)";
      cards[i].style.background = "MistyRose";
      cards[i].style.borderColor = "rgba(255, 0, 0, 0.2)";
    } else if (status == "L") {
      var late_icon = document.getElementById("mark_late_" + parseInt(i + 1));
      late_icon.style.background = "rgb(2, 117, 216)";
      cards[i].style.background = "Lightcyan";
      cards[i].style.borderColor = "rgba(0, 0, 255, 0.2)";
    }
    var element = document.getElementById("card_comment_" + parseInt(i + 1));
    comment = document.getElementById("students-" + i + "-comment").value;

    if (comment != "") {
      console.log(comment);
      element.childNodes[0].innerHTML = comment;
      element.style.display = "block";
    }
  }
}

$("document").ready(function () {
  if (performance.navigation.type == 2) {
    location.reload(true);
  }

  if (submitted == 0) {
    $("#submit").show();
    $("#update").hide();
    $("#submitted").hide();
  } else {
    $("#submit").hide();
    //$("#update").show();
    //$("#submitted").css("display", "block");
    $("#all").hide();
    $(".att_buttons").hide();
    $(".edit_button").show();
    color_cards_if_submitted();
  }
});
