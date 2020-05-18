import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from Flask_SEproj.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, PostAdminForm, RequestResetForm, ResetPasswordForm, PostAdminOTPForm, SearchForm
from Flask_SEproj.models import User, Post
from Flask_SEproj import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import requests
import random

x = 0
url = "https://www.fast2sms.com/dev/bulk"


@app.route('/')
def page():
    return render_template('about.html', title='About')


@app.route('/home')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, mobile_number=form.mobile_number.data, admin=form.admin.data)
        db.session.add(user)
        db.session.commit()
        if form.admin.data:
            flash('Your admin account has been created! You will now be able to login', 'success')
        else:
            flash('Your account has been created! You will now be able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsucessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.mobile_number = form.mobile_number.data
        db.session.commit()
        flash('your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.mobile_number.data = current_user.mobile_number
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/search/otp2/", methods=['GET', 'POST'])
@login_required
def search_otp():
    form = PostAdminOTPForm()
    x = request.args.get('x', None)
    name = request.args.get('name', None)
    if form.validate_on_submit():
        if(str(x) == form.otp.data):
            flash('OTP successfully verified', 'success')
            return redirect(url_for('search_result', name=name))

    return render_template('search_otp.html', legend="Enter OTP to continue!!", form=form)


@app.route("/search/search_result/", methods=['GET', 'POST'])
@login_required
def search_result():
    name = request.args.get('name', None)
    posts = Post.query.order_by(Post.date_posted.desc())
    flash('OTP worked!', 'success')
    return render_template('search_result.html', posts=posts, name=name)


@app.route("/post/newadmin/otp/", methods=['GET', 'POST'])
@login_required
def otp():
    x = request.args.get('x', None)
    title1 = request.args.get('title1', None)
    content1 = request.args.get('content1', None)

    author1 = request.args.get('author1', None)
    userq = User.query.filter_by(username=author1).first()
    form = PostAdminOTPForm()
    if form.validate_on_submit():
        if(str(x) == form.otp.data):
            post = Post(title=title1, content=content1, author=userq)
            db.session.add(post)
            db.session.commit()

            flash('The post has been saved!', 'success')
        else:
            flash('The post has not been saved!' + str(x), 'danger')
        return redirect(url_for('about'))
    return render_template('userpost_otp.html', legend="THis", form=form)


@app.route("/post/newadmin", methods=['GET', 'POST'])
@login_required
def new_adminpost():
    form = PostAdminForm()

    if form.validate_on_submit():

        userq = User.query.filter_by(username=form.name.data).first()
        x = random.randint(100001, 999999)
        payload = "sender_id=FSTSMS&message= otp is :" + str(x) + "&language=english&route=p&numbers=" + str(userq.mobile_number) + ",9677092057"
        headers = {
            'authorization': "kL6b0FUP3jTWfmN2KMhnaEOp5iQsHdV9Xr1weolB8xvGZuzAyqFluxeSonCryRfNbE7apHBqI4hXDgtM",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        otp = True
        flash('OTP sent successfully. Please check your register phone number', 'success')
        return redirect(url_for('otp', x=x, title1=form.title.data, content1=form.content.data, author1=form.name.data))
    return render_template('create_userpost.html', title='New Post', form=form, legend='New Post')


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        userq = User.query.filter_by(username=form.name.data).first()
        x = random.randint(100001, 999999)
        payload = "sender_id=FSTSMS&message= otp is :" + str(x) + "&language=english&route=p&numbers=" + str(userq.mobile_number) + ",9677092057"
        headers = {
            'authorization': "kL6b0FUP3jTWfmN2KMhnaEOp5iQsHdV9Xr1weolB8xvGZuzAyqFluxeSonCryRfNbE7apHBqI4hXDgtM",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        otp = True
        flash('OTP sent successfully. Please check your registered phone number', 'success')
        return redirect(url_for('search_otp', x=str(x), name=userq.username))
    return render_template('search.html', form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
@login_required
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, simply ignore. No changes will be made
    '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset ypur password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been update! You will now be able to login', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
