function get_user(teacher) {
  console.log("current teacher: " + teacher);
  if (teacher == "rfriedman") {
    element = document.getElementById("my_classes");
    if (element) element.href = "/today";
  }
}
