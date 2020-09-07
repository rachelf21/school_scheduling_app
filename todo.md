## TODO

- [x] try/catch exceptions before commiting to database
- [x] create classes for all tables
- [x] **set relationships among tables** - add attendance relationship when create attendance table
- [x] check db.models methods for accessing data
- [x] display data on html page
- [] generate csv files from data
- [] use environment variables for username, password, database
- [] write information to database
- [] automate day/time - class for that period should come up automatically
- [] upload and run from heroku - where does the database reside???
- [x] default entry for Status = P
- [] format time to display in more user friendly format

### HTML PAGES

- [x] create HTML pages for each table
- [] create a form for data
- [x] save information from form into table

<!-- <form method="POST" action="#" name="att_form">
  {{ att_form.hidden_tag() }}

  <div class="form-group">
    <legend class="border-bottom mb-4"> Include prefilled fields for: Week, Date, DOW, Period</legend>

  <div class = "row">

    <div class = "col-3">{{ form.email.label(class="form-control-label") }} {{ form.email(class="form-control form-control-lg") }}</div>

    <div class = "col-3">{{ form.student.label(class="form-control-label") }} {{ form.student(class="form-control form-control-lg") }}</div>
    <div class = "col-3">{{ form.status.label(class="form-control-label") }} {{ form.status(class="form-control form-control-lg") }}</div>
    <div class = "col-3">{{ form.comment.label(class="form-control-label") }} {{ form.comment(class="form-control form-control-lg") }}</div>

    <div class = "col-2 d-flex flex-column justify-content-end"> {{ form.save(class="btn btn-outline-info  form-control-lg") }} </div>
</div>

</form> -->
