from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Therapist, Patient, Intervention, Session

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        therapist = Therapist.query.filter_by(username=username.data).first()
        if therapist is not None:
            raise ValidationError('Please use a different username.')

    def validate_fname(self, fname):
        therapist = Therapist.query.filter_by(fname=fname.data).first()
        if therapist is not None:
            raise ValidationError('Please use a different First Name')

class PatientRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        patient = Patient.query.filter_by(username=username.data).first()
        if patient is not None:
            raise ValidationError('Please use a different username.')

class FollowForm(FlaskForm):
    username=StringField('Username:',validators=[DataRequired()])
    name=StringField('Intervention Session:',validators=[DataRequired()])
    submit=SubmitField('Assign')

class CreateSessionForm(FlaskForm):
    therapist_id = IntegerField('Please enter your Therapist ID:', validators=[DataRequired()])
    intervention_id = IntegerField('Please enter ID of the Intervention you would like to assign a session to:', validators=[DataRequired()])
    patient_id = IntegerField('Please enter ID of desired Patient:', validators=[DataRequired()])
    gametype = StringField('Desired Game Type:', validators=[DataRequired()])
    date_started = StringField('Please enter Current Date:', validators=[DataRequired()])
    session_number = StringField('Is this the First, Second or Third session assigned to this intervention?', validators=[DataRequired()])
    submit = SubmitField('Create Session')

    def validate_therapistid(self, therapist_id):
        therapist = Therapist.query.filter_by(id=therapist_id.data).first()
        if therapist is None:
            raise ValidationError('Please use a different username.')
