var paleyellow = "rgb(252, 255, 217)";
var dow = ["A_M", "A_T", "A_W", "A_Th"]; //change this to wk variable later
var per = [0, 1, 2, 3, 4, 5, "L", 6, 7, 8, 9, 10];
var per_fri = [0, 1, 2, 3, 4, "L", 5, 6, 7, 8, 9, 10];

function highlight_period(start_time, end_time) {
  var today = new Date();
  var date = today.getFullYear() + "-" + ("0" + (today.getMonth() + 1)).slice(-2) + "-" + today.getDate();

  var time_now = Date.now();
  console.log("time now: " + time_now);

  var startdatestring = date + "T0" + start_time + ":00.000+05:00";
  console.log(startdatestring);
  var time_per_start = Date.parse(startdatestring);
  console.log(time_per_start);

  var enddatestring = date + "T0" + end_time + ":00.000+05:00";
  //console.log(enddatestring);
  var time_per_end = Date.parse(enddatestring);

  if (time_per_start < time_now) {
    console.log("this period has passed");
  } else {
    console.log("this period has not happened yet");
  }
}

//computers or stem
function color_code_cs(user, sched, period) {
  if (user == "rfriedman") {
    if (curr_course.includes("Computers")) {
      document.currentScript.parentElement.parentElement.style.background = paleyellow;
    } else if (curr_course.includes("STEM")) {
      if (curr_course.includes("7")) document.currentScript.parentElement.parentElement.style.background = "HoneyDew";
      else document.currentScript.parentElement.parentElement.style.background = "LavenderBlush";
    }
  } else if (user == "tnahary") {
    if (curr_course.includes("7-111")) {
      document.currentScript.parentElement.parentElement.style.background = paleyellow;
    } else if (curr_course.includes("7-103")) {
      document.currentScript.parentElement.parentElement.style.background = "LavenderBlush";
    } else if (curr_course.includes("8-111")) {
      document.currentScript.parentElement.parentElement.style.background = "HoneyDew";
    }
  } else if (user == "rafriat") {
    if (curr_course.includes("8-101")) {
      document.currentScript.parentElement.parentElement.style.background = paleyellow;
    } else if (curr_course.includes("8-103")) {
      document.currentScript.parentElement.parentElement.style.background = "CornSilk";
    } else if (curr_course.includes("8-102")) {
      document.currentScript.parentElement.parentElement.style.background = "HoneyDew";
    } else if (curr_course.includes("7-102")) {
      document.currentScript.parentElement.parentElement.style.background = "LavenderBlush";
    }
  }
}

//G or B
function color_code(sched, period) {
  if (classid.includes("G")) {
    document.currentScript.parentElement.parentElement.style.background = paleyellow;
  } else if (classid.includes("B")) {
    document.currentScript.parentElement.parentElement.style.background = "HoneyDew";
  }
}

//Lunch. unusued function. did not work.
function color_lunch() {
  if (curr_per == "L") document.currentScript.parentElement.style.backgroundColor = "Gainsboro !important";
}

//Recess - unused function. did not work.
function color_recess() {
  if (curr_course.includes("Recess")) {
    //console.log("Recess is now. Current period is " + curr_per);
    element = document.currentScript.parentElement.parentElement;
    element.style.background = "Gainsboro !important";
  }
}
function convert_day(dow) {
  if (dow.includes("M")) return "Monday";
  else if (dow.includes("T") && !dow.includes("Th")) return "Tuesday";
  else if (dow.includes("W")) return "Wednesday";
  else if (dow.includes("Th")) return "Thursday";
  else if (dow.includes("F")) return "Friday";
  else return "Saturday/Sunday";
}

function write_linktocourse(sched, period) {
  var link_text = "/attendance/" + curr_class + "/" + curr_course + "/" + schedid + "/" + curr_per;
  parent.setAttribute("href", link_text);
  parent.setAttribute("style", "display:block; width:100%; height:100%");

  //console.log("dow= " + dow);
  if (!sched.includes(dow)) {
    var today = convert_day(dow);
    var day = convert_day(schedid);

    var message =
      "Today is " + today + ". You are entering attendance for " + day + ". Click OK to continue or click Cancel to choose another day.";
    var wrong_att = "return confirm('" + message + "')";
    //console.log("schedid = " + schedid);
    parent.setAttribute("onclick", wrong_att);
  }

  if (sched.substring(2) == period) {
    //console.log(sched.substring(2));
    document.currentScript.parentElement.parentElement.style.background = "#00FFFF";
  }
}

function AutoRefresh(t) {
  var date = new Date(new Date().getTime()).toLocaleTimeString();
  console.log("Refreshed " + date);
  setTimeout("location.reload(true);", t);
}
