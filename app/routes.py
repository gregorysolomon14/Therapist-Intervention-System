from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import RegistrationForm
from app.forms import LoginForm
from app.forms import FollowForm
from app.forms import PatientRegistrationForm
from app.forms import CreateSessionForm
from app.models import Therapist
from app.models import Patient
from app.models import Intervention
from app.models import Session
from sqlalchemy import text


@app.route('/')
@app.route('/home')
@login_required
def home():
    connection=db.session.connection()
    t=text("select Patient.username from Patient where Patient.username='aj1'")
    result=connection.execute(t)
    patient=str(result)
    return render_template('home (updated).html', title='Home',patient=patient)


@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        therapist = Therapist.query.filter_by(username=form.username.data).first()
        if therapist is None or not therapist.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(therapist, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Therapist(username=form.username.data, fname=form.fname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/patient_Confirmation', methods= ['GET','POST'])
def patient_confirmation():
    return render_template('patientConfirmation.html', title = 'Patient Confirmation')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = Therapist.query.filter_by(username=username).first_or_404
    return render_template('user.html',user=user)

@app.route('/assign',methods=['GET','POST'])
@login_required
def assign():
    form=FollowForm()
    if form.validate_on_submit():
        pat=Patient.query.filter_by(username=form.username.data).first()
        thep=Therapist.query.filter_by(username=current_user.username).first()
        int= Intervention(intervention_name=form.name.data,patient_id=pat.id,therapist_id=thep.id)
        db.session.add(int)
        db.session.commit()
        flash('The patient has successfully been assigned!')
        return redirect(url_for('assign'))
    return render_template('assign.html', title='Assignment', form=form)

@app.route('/follow/<username>')
@login_required
def follow(thepuser,patuser):
    therapist= Therapist.query.filter_by(username=thepuser).first()
    patient = Patient.query.filter_by(username=patuser).first()
    current_therapist.follow(patient)
    db.session.commit()
    flash('You are following {}!'.format(patuser))
    return redirect(url_for('patient', username=thepuser))

@app.route('/viewPatients')
@login_required
def view_patient_all():
    patients = Patient.query.all()
    return render_template('view_patient_all.html', title='View All Patients', patients=patients)

@app.route('/sessionmanager',methods=['GET','POST'])
@login_required
def sessionmanager():
        currentid=Therapist.query.filter_by(username=current_user.username).first()
        # The session manager displays only sessions that are assigned by the signed-in therapist.
        sessionview= Session.query.filter_by(therapist_id=currentid.id).all()
        return render_template('sessionmanager.html',title='Session Manager',sessionview=sessionview)

@app.route('/register_patient', methods=['GET', 'POST'])
def register_patient():
    form = PatientRegistrationForm()
    if form.validate_on_submit():
        user = Patient(username=form.username.data, fname=form.fname.data,lname=form.lname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('CONFIRMATION: The patient has been registered.')
        return redirect(url_for('view_patient_all'))
    return render_template('register_patient.html', title='Register Patient', form=form)

@app.route('/createsession', methods=['GET', 'POST'])
@login_required
def createsession():
    form= CreateSessionForm()
    if form.validate_on_submit():
        session=Session(session_number=form.session_number.data,gametype=form.gametype.data,
        patient_id=form.patient_id.data,therapist_id=form.therapist_id.data,intervention_id=form.intervention_id.data,
        date_started=form.date_started.data)
        db.session.add(session)
        db.session.commit()
        flash('CONFIRMATION: Session has been created')
    return render_template('createsession.html',title='Create Session',form=form)
