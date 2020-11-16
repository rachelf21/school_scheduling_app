var links_exports = [
  "https://classroom.google.com/u/0/c/MTYwMDIyMjgxMDU0/a/MTg3ODcwNTYwNzg2/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTYzMjYzNTQxNTI2/a/MTUwNzkzMzg3NTQ3/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTYzMjYzNTQxNTY0/a/MTg3ODcwNjExNzEy/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTY0MTQ5OTEyMzc1/a/MTUwODE5NzcyNDEw/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTYzNDA5NjI0MDYw/a/MTUwODE5NzcyNDU0/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTYzMjUzNjg4MTI2/a/MTg3ODcwNTYxMDAw/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTYwMDQ4MDQ1NjQ0/a/MTg3ODcwNTYwODYy/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTYzMTQ0MzQ0NjI2/a/MTUwOTYzNTUyMzg0/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTY0MTQ5OTEyMzg2/a/MTUwOTYzNTUyMzMz/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTYwMDQxNjQ4NzE3/a/MTg3NzAwMjI4Mzk3/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTY0MTQ5OTEyMzQ3/a/MTgwMjk5MTczMjE2/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTYzMDc1MjE2Nzc0/a/MTg3NzcxMjUwODIw/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTY0MTQ5OTEyMzY1/a/MTUwNzkzMzg3NjY0/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTYzMDc1MjE2NjM0/a/MTg3NzcxMjUwNzY3/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTY0MTQ5OTEyMzU2/a/MTUwNjQ3NDA3NDIy/submissions/by-status/and-sort-name/all",
  "https://classroom.google.com/u/0/c/MTYzMjYzNTQxNTQ4/a/MTg3ODcwNTYxMDcx/submissions/by-status/and-sort-name/all",
];

var links_grades = [
  "https://classroom.google.com/u/0/c/MTYwMDIyMjgxMDU0/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTYzMjYzNTQxNTI2/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTYzMjYzNTQxNTY0/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTY0MTQ5OTEyMzc1/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTYzNDA5NjI0MDYw/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTYzMjUzNjg4MTI2/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTYwMDQ4MDQ1NjQ0/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTYzMTQ0MzQ0NjI2/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTY0MTQ5OTEyMzg2/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTYwMDQxNjQ4NzE3/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTY0MTQ5OTEyMzQ3/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTYzMDc1MjE2Nzc0/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTY0MTQ5OTEyMzY1/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTYzMDc1MjE2NjM0/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTY0MTQ5OTEyMzU2/gb/sort-name",
  "https://classroom.google.com/u/0/c/MTYzMjYzNTQxNTQ4/gb/sort-name",
];

var classes = [
  "7G-101",
  "7G-102",
  "7G-103",
  "7G-111",
  "7B-201",
  "7B-202",
  "7B-203",
  "7B-211",
  "8G-101",
  "8G-102",
  "8G-103",
  "8G-111",
  "8B-201",
  "8B-202",
  "8B-203",
  "8B-211",
];

function open_class_grades(i) {
  //console.log(links_grades[i]);
  window.open(links_grades[i]);
}

function view_grades7() {
  for (var i = 0; i < 8; i++) {
    var button = document.getElementById("gradelink" + i);
    button.setAttribute("onclick", window.open(links_grades[i]));
  }
}

function view_grades8() {
  for (var i = 8; i < 16; i++) {
    var button = document.getElementById("gradelink" + i);
    button.setAttribute("onclick", window.open(links_grades[i]));
  }
}

function create_buttons() {
  var div1 = document.createElement("div");
  div1.setAttribute("id", "div1");
  div1.setAttribute("class", "col");
  var div2 = document.createElement("div");
  div2.setAttribute("id", "div2");
  div2.setAttribute("class", "col");

  var div_grades = document.getElementById("div_grades");
  div_grades.appendChild(div1);
  div_grades.appendChild(div2);

  for (var i = 0; i < 8; i++) {
    var button = document.createElement("input");
    button.setAttribute("id", "gradelink" + i);
    button.setAttribute("type", "button");
    button.setAttribute("class", "mb-1");
    button.setAttribute("value", classes[i]);
    button.setAttribute("onclick", "open_class_grades(" + i + ")");
    div1.appendChild(button);
    div1.appendChild(document.createElement("br"));
  }
  for (var i = 8; i < 16; i++) {
    var button = document.createElement("input");
    button.setAttribute("id", "gradelink" + i);
    button.setAttribute("type", "button");
    button.setAttribute("class", "mb-1");
    button.setAttribute("value", classes[i]);
    button.setAttribute("onclick", "open_class_grades(" + i + ")");
    div2.appendChild(button);
    div2.appendChild(document.createElement("br"));
  }
}
