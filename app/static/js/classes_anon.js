function select_period(classs, course) {
  var per = prompt("Enter period from 1 to 10.");
  if (per >= 1 && per <= 10) {
    attendancelink = "/attendance/" + classs + "/" + classs + "-" + course + "/" + my_day + "/" + per;
    console.log(attendancelink);
    window.location.href = attendancelink;
  } else {
    alert("Invalid period number. \nNumber must be from 1 to 10");
  }
}

function select_current_period(classs, course) {
  var per_input = document.getElementById("current_period");
  console.log("current period " + per_input);
  var per = parseInt(per_input.value);
  console.log("period nubmer " + per);
  var x = document.getElementById("current_class").value;
  var y = document.getElementById("current_subject").value;

  if (per >= 1 && per <= 10) {
    attendancelink = "/attendance/" + x + "/" + x + "-" + y + "/" + my_day + "/" + per;
    console.log(attendancelink);
    window.location.href = attendancelink;
  } else {
    alert("Invalid period number. \nNumber must be from 1 to 10");
  }
}

function set_values(classs, course) {
  var x = document.getElementById("current_class");
  x.value = classs;
  var y = document.getElementById("current_subject");
  y.value = course;
}

$("document").ready(function () {
  console.log("noclasses = " + noclasses);
  if (noclasses == 0) {
    console.log("no classes");
    $("#no_classes").css("display", "block");
  } else {
    $("#no_classes").css("display", "none");
  }
});
