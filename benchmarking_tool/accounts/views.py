import os
from pathlib import Path
import secrets
from flask import Blueprint,request,render_template,redirect,flash,url_for,current_app
from flask_login import login_user, current_user, logout_user, login_required
from ..forms import *
from ..helper import *
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from benchmarking_tool import app
from benchmarking_tool.methods import *
from benchmarking_tool.decorators import *
from dotenv import load_dotenv
from sqlalchemy import or_
from benchmarking_tool.image_reckognition.bill_detection import *
from benchmarking_tool.image_reckognition.bill_detection import detect_electrical_bill
from benchmarking_tool.methods import *
from benchmarking_tool.methods import *
from difflib import get_close_matches
import re
load_dotenv()
from ..forms import *

accounts = Blueprint('accounts',__name__,template_folder='templates', url_prefix='/accounts')

bcrypt = Bcrypt()
mail = Mail()
app_root = Path(__file__).parents[1]

@accounts.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('commercial.facilityoverview'))
    if request.method == "POST":
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        form = RegistrationForm(
            email=email,
            phone_numer=phone_number,
            password=password,
            confirm_password=confirm_password,
        )
        if form.validate_on_submit():
                rows = User.query.count()
                user_id = rows + 1
                customer = Customer.query.filter_by(id = None).first()
                role = Role.query.filter_by(name='Admin').first()
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                user = User(
                    id = user_id,
                    email=form.email.data,
                    phone_number=form.phone_number.data,
                    password=hashed_password,
                    role_id=role.id)
                user.customer = customer
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('commercial.facilityoverview'))
    else:
        form = RegistrationForm(
            email="",
            first_name="",
            last_name="",
            password="",
            confirm_password="",
        )
    return render_template('register.html', title='Register', form=form, last_updated=dir_last_updated())

# Route for the user to login
@accounts.route('/login', methods=['GET', 'POST'])
def login():
    print("in login")
    if current_user.is_authenticated:
        return redirect(url_for('main.overview'))
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        form = LoginForm(
            email=email,
            password=password
        )
        if form.validate_on_submit():
            user = User.query.filter_by(email=email).first()
            role_user = user.role.name
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next')
                flash(f"Welcome {email}", 'success')
                if role_user == 'User':
                    customer = user.customer
                    survey = customer.survey
                    if survey == None:
                        return redirect(url_for('main.customer_info'))
                    else:
                        return redirect(next_page) if next_page else redirect(url_for('main.overview'))
                else:
                    return redirect(next_page) if next_page else redirect(url_for('main.overview'))
            else:
                flash(
                    f"Login Unsuccessful,Please check your email and Password!", 'danger')
                return redirect(url_for('accounts.login'))
    else:
        form = LoginForm(email="")
    return render_template('login.html', title='Login', form=form,last_updated=dir_last_updated())

@accounts.route('/commerciallogin', methods=['GET', 'POST'])
def commerciallogin():
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    if current_user.is_authenticated:
        return redirect(url_for('commercial.facilityoverview'))
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        next_url = request.form["next"]
        form = LoginForm(
            email=email,
            password=password
        )
        if form.validate_on_submit():
            user = User.query.filter_by(email=email).first()
            role_user = user.role.name
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next')
                flash(f"Welcome {email}", 'success')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(url_for('commercial.switchfacilities'))
            else:
                flash(
                    f"Login Unsuccessful,Please check your email and Password!", 'danger')
                return redirect(url_for('accounts.commerciallogin'))
    else:
        form = LoginForm(email="")
    return render_template('commerciallogin.html', title='Login', form=form,last_updated=dir_last_updated())



# route for the user to logout
@accounts.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('accounts.commerciallogin'))

# route for the user to request a new password
@accounts.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.overview'))
    if request.method == 'POST':
        email = request.form["email"]
        form = RequestResetForm(email=email)
        if form.validate_on_submit():
            user = User.query.filter_by(email=email).first()
            send_reset_email(user)
            flash(
                'An email has been sent with instructions to reset your password', 'info')
            return redirect(url_for('accounts.login'))
    else:
        form = RequestResetForm(email='')
    return render_template('reset_request.html', title='Reset Password', form=form)

# route for the user to reset his password
@accounts.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.overview'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('accounts.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f"Thank You. Your Password has been updated.You can now log in", 'success')
        return redirect(url_for('accounts.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

# route for updating the user account
@accounts.route('/update_user', methods=['GET', 'POST'])
@survey_required
@login_required
def update_user():
    if request.method == 'POST':
        email = request.form["email"]
        current_password = request.form['current_password']
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        form = UpdateAccountForm(email=email,current_password=current_password,
                new_password=new_password,confirm_password=confirm_password)
        if form.validate_on_submit():
            if bcrypt.check_password_hash(current_user.password, current_password):
                hashed_password = bcrypt.generate_password_hash(
                    new_password).decode('utf-8')
                current_user.email = form.email.data
                current_user.password = hashed_password
                db.session.commit()
                flash(f"Thank You. Your Account has been updated.", 'success')
                return redirect(url_for('main.overview'))
    else:
        form = UpdateAccountForm(email=current_user.email, current_password="",
            new_password="",confirm_password="")
    return render_template("user_update.html",title='Update Account', form=form,last_updated=dir_last_updated())


# function to send email
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='server@pollen.one',
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link :
{url_for('accounts.reset_token',token=token,_external=True)}
    If you didn't make the request, please ignore this email
    '''
    mail.send(msg)


def save_picture(form_picture,location):
	random_hex = secrets.token_hex(8)
	file_extension = os.path.splitext(form_picture.filename)[1]
	picture_filename = random_hex + file_extension
	picture_path = os.path.join(app_root,'static/'+location,picture_filename)
	form_picture.save(picture_path)
	return picture_filename

@accounts.route('/check_address',methods=['POST'])
def check_address():
    if 'gas_photo_bill' in request.files:
        picture = request.files['gas_photo_bill']
    if 'electrical_photo_bill' in request.files:
        picture = request.files['electrical_photo_bill']
    image = save_picture(picture,'temp_folder')
    address = detect_address(image,'temp_folder')
    if (address == None):
        return {'success': False,'address': None}
    else:
        return {'success': True,'address': address[0]}




@accounts.route('/offline.html', methods=['GET'])
def offline():
    return render_template('offline.html', title='offline', last_updated=dir_last_updated())


