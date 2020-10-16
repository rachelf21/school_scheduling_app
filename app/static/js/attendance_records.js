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
  if (category != "date") {
    $(".hid").css("display", "none");
  } else {
    $(".hidedate").css("display", "none");
  }
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
  new_comment = new_comment.replace(/'/g, "") + " -edited";
  //console.log("new comment = " + new_comment);
  var date = document.getElementById("current_date").value;
  var courseid = document.getElementById("current_courseid").value;
  var email = document.getElementById("current_email").value;
  var name = document.getElementById("current_name").value;

  var test = "/edit_attendance/" + date + "/" + courseid + "/" + email + "/" + new_status + "/" + new_comment;
  //console.log(test);
  window.location.href = "/edit_attendance/" + date + "/" + courseid + "/" + email + "/" + new_status + "/" + new_comment;
}
//href="/send_email/{{att.email}}/{{att.courseid}}"

function email_absences(student_email, name, course, date) {
  var pos = name.indexOf(",", 0);
  var first = name.substring(pos + 2);
  var last = name.substring(0, pos);
  if (confirm("Are you sure you want to email " + first + " " + last + " and parents?")) {
    var studentObj = { student_email: student_email, student_name: name, course: course, attdate: date };

    $.ajax({
      type: "POST",
      contentType: "application/json",
      url: "/send_email",
      //context: document.body,
      dataType: "json",
      data: JSON.stringify(studentObj),
      success: function (data) {
        //window.location.reload;
        //alert("Email sent to " + name + " and parents.\r\nAx copy has been sent to your email.");
        $("#ajax_alerts").html("Emails sent to student and parents.\r\nCheck your email for confirmation.");
        $("#ajax_alerts").css("display", "block");
        console.log("response: " + data);
        $(this).addClass("done");
      },
      error: function (error) {
        console.log("error " + error);
      },
    });
  } else {
    console.log("user canceled email request");
  }
}

function formatDate(date) {
  var d = new Date(date),
    month = "" + (d.getUTCMonth() + 1),
    day = "" + d.getUTCDate(),
    year = d.getFullYear();

  if (month.length < 2) month = "0" + month;
  if (day.length < 2) day = "0" + day;

  return [year, month, day].join("-");
}

function email_all(attendance) {
  for (var i = 0; i < attendance.length; i++) {
    student_email = attendance[i].email;
    student_name = attendance[i].name;
    status = attendance[i].status;
    course = attendance[i].courseid;
    longdate = attendance[i].date;
    date = formatDate(longdate);
    if (status == "A") {
      console.log(student_email + ", " + student_name + ", " + course + ", " + date);
      email_absences(student_email, student_name, course, date);
    }
  }
}
