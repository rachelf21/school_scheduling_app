function select_period(classs, course) {
  var per = prompt("Enter period from 0 to 10.");
  if (per >= 0 && per <= 10) {
    attendancelink = "/attendance/" + classs + "/" + classs + "-" + course + "/" + my_day + "/" + per;
    console.log(attendancelink);
    window.location.href = attendancelink;
  } else {
    alert("Invalid period number. \nNumber must be from 0 to 10");
  }
}

function select_current_period(classs, course) {
  var per_input = document.getElementById("current_period");
  console.log("current period " + per_input);
  var per = parseInt(per_input.value);
  console.log("period nubmer " + per);
  var x = document.getElementById("current_class").value;
  var y = document.getElementById("current_subject").value;

  if (per >= 0 && per <= 10) {
    attendancelink = "/attendance/" + x + "/" + x + "-" + y + "/" + my_day + "/" + per;
    console.log(attendancelink);
    window.location.href = attendancelink;
  } else {
    alert("Invalid period number. \nNumber must be from 0 to 10");
  }
}

function set_values(classs, course) {
  var x = document.getElementById("current_class");
  x.value = classs;
  var y = document.getElementById("current_subject");
  y.value = course;
}

function highlight_current_period(periodid, curr_per) {
  console.log(periodid + " " + curr_per);
  if (periodid == curr_per) {
    console.log("in this period");
    document.currentScript.parentElement.style.background = "#e6ffe6";
  }
}

//SET CURSOR POSITION
$.fn.setCursorPosition = function (pos) {
  this.each(function (index, elem) {
    if (elem.setSelectionRange) {
      elem.setSelectionRange(pos, pos);
    } else if (elem.createTextRange) {
      var range = elem.createTextRange();
      range.collapse(true);
      range.moveEnd("character", pos);
      range.moveStart("character", pos);
      range.select();
    }
  });
  return this;
};

function AutoRefresh(t) {
  var date = new Date(new Date().getTime()).toLocaleTimeString();
  console.log("Refreshed " + date);
  setTimeout("location.reload(true);", t);
}

$("document").ready(function () {
  AutoRefresh(300000);

  if (noclasses == 0) {
    console.log("no classes");
    $("#no_classes").css("display", "block");
  } else {
    $("#no_classes").css("display", "none");
  }
});
