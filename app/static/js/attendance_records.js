function test() {
  console.log("working");
}

function convert_date(mydate) {
  const d = new Date(mydate + "T00:00:00.000-05:00");
  const ye = new Intl.DateTimeFormat("en-US", { year: "numeric" }).format(d);
  const mo = new Intl.DateTimeFormat("en-US", { month: "long" }).format(d);
  const da = new Intl.DateTimeFormat("en-US", { day: "numeric" }).format(d);

  formatted_date = `${mo} ${da}, ${ye}`;
  return formatted_date;
}

$("document").ready(function () {
  //alert("in attendance records.js");
});

function set_values(id, date, courseid, email, name, status, comment) {
  var i = document.getElementById("current_id");
  i.value = id;
  var d = document.getElementById("current_date");
  d.value = date;
  var c = document.getElementById("current_courseid");
  c.value = courseid;
  var e = document.getElementById("current_email");
  e.value = email;
  var n = document.getElementById("current_name");
  n.value = name;
  var s = document.getElementById("new_status");
  s.value = status;
  var t = document.getElementById("new_comment");
  t.value = comment;
}

function edit_attendance() {
  //console.log("edit_attendance ");
  var new_status = document.getElementById("new_status").value.toUpperCase();
  var new_comment = document.getElementById("new_comment").value;
  //new_comment = new_comment.replace(/'/g, "");
  //console.log("new comment = " + new_comment);
  var date = document.getElementById("current_date").value;
  var courseid = document.getElementById("current_courseid").value;
  var email = document.getElementById("current_email").value;
  var name = document.getElementById("current_name").value;

  var test = "/edit_attendance/" + date + "/" + courseid + "/" + email + "/" + new_status + "/" + new_comment;
  //console.log(test);
  window.location.href = "/edit_attendance/" + date + "/" + courseid + "/" + email + "/" + new_status + "/" + new_comment;
}
