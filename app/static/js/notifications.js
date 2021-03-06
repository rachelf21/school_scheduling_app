function email_progress(student_email, name, course) {
  var pos = name.indexOf(",", 0);
  var first = name.substring(pos + 2);
  var last = name.substring(0, pos);
  if (confirm("Are you sure you want to email " + first + " " + last + " and parents about their missing work?")) {
    var studentObj = { student_email: student_email, student_name: name, course: course };

    $.ajax({
      type: "POST",
      contentType: "application/json",
      url: "/send_teacher_email",
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

function email_failure_alert(teacher, student_email, name, course) {
  var pos = name.indexOf(",", 0);
  var first = name.substring(pos + 2);
  var last = name.substring(0, pos);
  if (confirm("Are you sure you want to email a Failure Alert to " + first + " " + last + " and parents?")) {
    var studentObj = { student_email: student_email, student_name: name, course: course };

    $.ajax({
      type: "POST",
      contentType: "application/json",
      url: teacher == "rfriedman" ? "/html_send_failure_alert_email" : "/send_failure_alert_email",
      //url: "/send_failure_alert_email",
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

function html_email_failure_alert(student_email, name, course) {
  var pos = name.indexOf(",", 0);
  var first = name.substring(pos + 2);
  var last = name.substring(0, pos);
  if (confirm("Are you sure you want to email (html) a Failure Alert to " + first + " " + last + " and parents?")) {
    var studentObj = { student_email: student_email, student_name: name, course: course };

    $.ajax({
      type: "POST",
      contentType: "application/json",
      url: "/html_send_failure_alert_email",
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

function test() {
  console.log("works");
}
