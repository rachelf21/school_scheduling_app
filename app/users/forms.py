from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from app.models import Users

#%%
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    last = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=25)])
    first = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=25)]) 
    title_options = [('',''),('Miss','Miss'),( 'Ms.','Ms.'), ('Mrs.','Mrs.'), ('Mr.','Mr.' ), ('Rabbi', 'Rabbi'), ('Dr.','Dr.')]
    title = SelectField('Title', choices=title_options)
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Continue')
    
    def validate_username(self, username):
        user = Users.query.filter_by(username= username.data).first()        
        if user:
            raise ValidationError('User already exists.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()        
        if user:
            raise ValidationError('Email already exists.')
                
#%% 
class RegisterClassesForm(FlaskForm):
    class7B101 = BooleanField('7B-101')
    class7B102 = BooleanField('7B-102')
    class7B103 = BooleanField('7B-103')
    class7B111 = BooleanField('7B-111')
    class7G101 = BooleanField('7G-101')
    class7G102 = BooleanField('7G-102')
    class7G103 = BooleanField('7G-103')
    class7G111 = BooleanField('7G-111')
    
    class8B101 = BooleanField('8B-101')
    class8B102 = BooleanField('8B-102')
    class8B103 = BooleanField('8B-103')
    class8B111 = BooleanField('8B-111')
    class8G101 = BooleanField('8G-101')
    class8G102 = BooleanField('8G-102')
    class8G103 = BooleanField('8G-103')
    class8G111 = BooleanField('8G-111')  
    
    subject_options = [('Select', '--Select Subject--'),('ELA', 'ELA'), ('Computers', 'Computers'), ('Gemara', 'Gemara'), ('Halacha', 'Halacha'), ('Hashkafah', 'Hashkafah'), ('Humash', 'Humash'), ('Jewish History', 'Jewish History'), ('Judaic Studies', 'Judaic Studies'), ('Keria', 'Keria'), ('Math', 'Math'), ('Nabi', 'Nabi'), ('Parasha', 'Parasha'), ('Safah', 'Safah'), ('Safe', 'Safe'), ('Science', 'Science'), ('Social Studies', 'Social Studies'), ('Tamim', 'Tamim')]
    
    subject = SelectField('Subject', choices = subject_options)
    
    def validate_subject(self, subject):
        if subject.data == 'Select':
            raise ValidationError('Please select a subject.')
        
    add = SubmitField('Add another subject')
    submit = SubmitField('Done!')



#%%            
class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#%%
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=25)],render_kw = {'disabled': 'disabled'})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],render_kw = {'disabled': 'disabled'})
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Upload')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
 
#%%
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset', )

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
 
    
 #%%
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password', )

 