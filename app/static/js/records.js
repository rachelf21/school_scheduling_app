function test() {
  console.log("working");
}

function populate_classes(e) {
  console.log("populating classes");
  var all_classes = [];
  my_date = e.target.value;
  console.log("selected date=" + my_date);
  var dateObj = { date: my_date };

  $.ajax({
    type: "POST",
    contentType: "application/json",
    url: "/get_classes_today",
    //context: document.body,
    dataType: "json",
    data: JSON.stringify(dateObj),
    //data: { data: "2020-10-01" },
    success: function (response) {
      console.log("response: " + response);
      all_classes = response;
      console.log("len= " + all_classes.length);
      var element = document.getElementById("courseid");

      var length = element.options.length;
      for (i = length - 1; i >= 0; i--) {
        element.options[i] = null;
      }

      for (index in all_classes) {
        console.log(all_classes[index]);
        element.options[index] = new Option(all_classes[index], all_classes[index]);
      }

      if (all_classes.length == 0) {
        element.options[0] = new Option("No classes", "No classes on this day");
        element.value = "No classes on this day";
      }
      $(this).addClass("done");
    },
    error: function (error) {
      console.log(error);
    },
  });
}

$("document").ready(function () {
  console.log($("#date").value);
});

var Attendance = {};
function edit_attendance(id, date, courseid, email, name, status, comment) {
  id = id - 1;
  var new_status = prompt("Enter updated STATUS for " + name + ". \nEnter only A, P, or L.").toUpperCase();
  if (new_status == "A" || new_status == "P" || new_status == "L") {
    comment = comment + " -edited";
    console.log(email);
    window.location.href = "/edit_attendance/" + date + "/" + courseid + "/" + email + "/" + new_status + "/" + comment;
  } else {
    alert("This entry was not updated. Please enter  A, P, or L only.");
    console.log("not updated");
  }
}

// // Show a half-transparent DIV to "shadow" the page
// // (the form is not inside, but near it, because it shouldn't be half-transparent)
// function showCover() {
//   let coverDiv = document.createElement("div");
//   coverDiv.id = "cover-div";

//   // make the page unscrollable while the modal form is open
//   document.body.style.overflowY = "hidden";

//   document.body.append(coverDiv);
// }

// function hideCover() {
//   document.getElementById("cover-div").remove();
//   document.body.style.overflowY = "";
// }

// function showPrompt(text, callback) {
//   showCover();
//   let form = document.getElementById("prompt-form");
//   let container = document.getElementById("prompt-form-container");
//   document.getElementById("prompt-message").innerHTML = text;
//   form.status.value = "";
//   form.comment.value = "";

//   function complete(value) {
//     hideCover();
//     container.style.display = "none";
//     document.onkeydown = null;
//     callback(value);
//   }

//   form.onsubmit = function () {
//     let value = form.status.value;
//     if (value == "") return false; // ignore empty submit

//     complete(value);
//     return false;
//   };

//   form.cancel.onclick = function () {
//     complete(null);
//   };

//   document.onkeydown = function (e) {
//     if (e.key == "Escape") {
//       complete(null);
//     }
//   };

//   let lastElem = form.elements[form.elements.length - 1];
//   let firstElem = form.elements[0];

//   lastElem.onkeydown = function (e) {
//     if (e.key == "Tab" && !e.shiftKey) {
//       firstElem.focus();
//       return false;
//     }
//   };

//   firstElem.onkeydown = function (e) {
//     if (e.key == "Tab" && e.shiftKey) {
//       lastElem.focus();
//       return false;
//     }
//   };

//   container.style.display = "block";
//   form.elements.text.focus();
// }
