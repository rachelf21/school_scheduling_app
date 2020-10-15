function get_user(teacher) {
  console.log("current teacher: " + teacher);
  if (teacher == "rfriedman") {
    element = document.getElementById("my_classes");
    if (element) element.href = "/today";
    element2 = document.getElementById("my_schedule");
    //if (element2) element2.href = "/weekly_schedule";
  }
}
