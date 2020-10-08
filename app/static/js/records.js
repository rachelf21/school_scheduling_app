function test() {
  console.log("working");
}

function populate(selected_date) {
  var dateObj = { date: selected_date };

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
      //console.log("len= " + all_classes.length);
      var element = document.getElementById("courseid");

      var length = element.options.length;
      for (i = length - 1; i >= 0; i--) {
        element.options[i] = null;
      }

      for (index in all_classes) {
        //console.log(all_classes[index]);
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

function populate_classes(e) {
  //console.log("populating classes");
  var all_classes = [];
  my_date = e.target.value;
  populate(my_date);
}

$("document").ready(function () {
  //alert("in records.js");
  var my_date = $("#date1").val();
  populate(my_date);
});
