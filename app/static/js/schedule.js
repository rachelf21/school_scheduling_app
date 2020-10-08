var paleyellow = "rgb(252, 255, 217)";
var dow = ["A_M", "A_T", "A_W", "A_Th"]; //change this to wk variable later
var per = [0, 1, 2, 3, 4, 5, "L", 6, 7, 8, 9, 10];

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

function color_code(sched, period) {
  if (curr_course.includes("Computers")) {
    document.currentScript.parentElement.parentElement.style.background = paleyellow;
  } else if (curr_course.includes("STEM")) {
    if (curr_course.includes("7")) document.currentScript.parentElement.parentElement.style.background = "HoneyDew";
    else document.currentScript.parentElement.parentElement.style.background = "LavenderBlush";
  } else if (classid.includes("G")) {
    document.currentScript.parentElement.parentElement.style.background = paleyellow;
  } else if (classid.includes("B")) {
    document.currentScript.parentElement.parentElement.style.background = "HoneyDew";
  }

  var link_text = "/attendance/" + curr_class + "/" + curr_course + "/" + schedid + "/" + curr_per;
  //console.log(link_text);
  parent.setAttribute("href", link_text);
  parent.setAttribute("style", "display:block; width:100%; height:100%");
  if (sched.substring(2) == period) {
    console.log(sched.substring(2));
    document.currentScript.parentElement.parentElement.style.background = "#00FFFF";
  }
}

function AutoRefresh(t) {
  var date = new Date(new Date().getTime()).toLocaleTimeString();
  console.log("Refreshed " + date);
  setTimeout("location.reload(true);", t);
}
