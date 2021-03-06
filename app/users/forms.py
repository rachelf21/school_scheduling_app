from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, SelectMultipleField,TextAreaField
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
        if not "@mdyschool.org" in email.data:
            raise ValidationError('Email must be @mdyschool.org.')
                
#%% 
class RegisterClassesForm(FlaskForm):
    class7B101 = BooleanField('7B-201')
    class7B102 = BooleanField('7B-202')
    class7B103 = BooleanField('7B-203')
    class7B111 = BooleanField('7B-211')
    class7G101 = BooleanField('7G-101')
    class7G102 = BooleanField('7G-102')
    class7G103 = BooleanField('7G-103')
    class7G111 = BooleanField('7G-111')
    
    class8B101 = BooleanField('8B-201')
    class8B102 = BooleanField('8B-202')
    class8B103 = BooleanField('8B-203')
    class8B111 = BooleanField('8B-211')
    class8G101 = BooleanField('8G-101')
    class8G102 = BooleanField('8G-102')
    class8G103 = BooleanField('8G-103')
    class8G111 = BooleanField('8G-111')  
    
    
    subject_options = [('Select', '--Select Subject--'),('ELA', 'ELA'), ('Computers', 'Computers'), ('Gemara', 'Gemara'), ('Halacha', 'Halacha'), ('Hashkafah', 'Hashkafah'), ('Humash', 'Humash'), ('Jewish History', 'Jewish History'), ('Judaic Studies', 'Judaic Studies'), ('Keria', 'Keria'), ('Lunch', 'Lunch'),('Math', 'Math'), ('Minha', 'Minha'),('Nabi', 'Nabi'), ('Parasha', 'Parasha'), ('Recess', 'Recess'), ('Safah', 'Safah'), ('Safe', 'Safe'), ('Science', 'Science'), ('Social Studies', 'Social Studies'), ('Tamim', 'Tamim'), ('Tefila', 'Tefila')]
    
    subject = SelectField('Subject', choices = subject_options)
    
    def validate_subject(self, subject):
        if subject.data == 'Select':
            raise ValidationError('Please select a subject.')
        
    add = SubmitField('Reset')
    submit = SubmitField('Add selected classes')


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
                           validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Apply selected picture')

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

class SetMsgBodyForm(FlaskForm):
    content = TextAreaField(u"Update email message below:", render_kw={'class': 'form-control', 'rows': 7})
    submit = SubmitField('Submit')
    subject = StringField('Update email subject below:')
    changeText = SubmitField('Set Message Body')
    cancel = SubmitField('Cancel')
    
class SuggestionsForm(FlaskForm):
    content = TextAreaField(u"Suggestion", render_kw={'class': 'form-control', 'rows': 7})
    submit = SubmitField('Submit')
    cancel = SubmitField('Cancel')