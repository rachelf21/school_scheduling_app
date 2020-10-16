## TODO

- [x] try/catch exceptions before commiting to database
- [x] create classes for all tables
- [x] **set relationships among tables** - add attendance relationship when create attendance table
- [x] check db.models methods for accessing data
- [x] display data on html page
- [x] generate csv files from data
- [ ] use environment variables for username, password, database
- [ ] create new user for each teacher
- [x] add ability to upload and retrieve lesson info for each class
- [x] write information to database
- [x] automate day/time - class for that period should come up automatically (based on schedule click)
- [x] allow manual entry of date and period
- [x] upload and run from heroku - where does the database reside???
- [x] default entry for Status = P
- [x] format time to display in more user friendly format
- [x] add ability to retrieve attendance records for specific class
- [x] add ability to retrieve attendance records for specific student
- [x] add ability to retrieve attendance records for specific day
- [ ] attendance records to display latest dates first
- [x] add student detail when click on student
- [x] add ability to click on student when taking attendance to bring up past attendance
- [ ] adjust display on phone
- [x] edit lesson when in view lesson mode
- [x] delete lesson
- [ ] add bootstrap flash success when added lesson and attendance
- [x] add feature to add lesson plan
- [x] display lesson plan in schedule view
- [x] option to display all students
- [x] display total absences for attendance records
- [ ] freeze first column in student table, attendance tracking table, class table
- [x] display dismissal lists
- [x] create student info view
- [x] password protect student info pages
- [ ] enable check/uncheck students called for dismissal, based on numbers
- [x] initialize to WeekA or WeekB, automatically go to today's schedule based on week
- [x] change colors of Status items - highlight absences
- [x] display absence amount next to students name for attendance
- [x] button to mark/unmark all as present
- [ ] when clicking All, trigger color change on relevant status buttons
- [ ] change color for status on phone
- [x] weekly schedule
- [ ] on weekly schedule, turn cell into link instead of text
- [ ] remove sidebar from pages
- [x] add Edit button on attendance page to edit attendance record, for individual student
- [x] add present/absent/late/clear icons to attendance page
- [x] **add users and user authentication**
- [x] change page titles to include classs of attendance
- [x] highlight current period on full schedule and on daily schedules
- [x] change colors for absences when display all attendance records
- [x] add late feature to attendance and display late count
- [ ] bottom borders for new classes on dates page
- [x] different buttons on comfirmation page
- [x] separate abs and late titles, change colors, mute titles
- [x] hide input field from student names, show names only, adjust styling
- [x] display names in card format
- [x] ajax to retrieve classes for specified date only
- [x] add backgrounds
- [x] replace javascript alerts for edit status, add comment to modal popup

- [ ] change submit attendance button to update if these fields are equal: teacher, date, class, period.
- [ ] change take_attendance function not to accept blank values
- [ ] create new function for update - only retrieve cards which are not blank, update attendance table with new values.
- [ ] flash message on screen that attendance has been updated and take to attendance records screen.

- [ ] allow update of custom message

### HTML PAGES

- [x] create HTML pages for each table
- [x] save information from form into table
- [x] dropdown for status A/P
- [x] add time to daily attendance sheet
- [x] class in All Classes list should link to that class
- [x] scheduleid's should be listed for each class
- [x] remove my classes sidebar, make first col biger
- [x] show room number on class list
- [ ] change mdy logo to white

  Add this requirement manually: Flask-Bcrypt==0.7.1
