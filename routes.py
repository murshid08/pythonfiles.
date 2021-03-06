
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from source import app, db, bcrypt
from source.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods=["GET","POST"])
@app.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('new_post'))
    if request.method=="POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user, remember=request.form['remember'])
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('new_post'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login')


@app.route("/home")
def home():
    page=request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method=="POST":
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=request.form['username'], email=request.form['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register')








@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)

#     return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if request.method=="POST":

        # if request.form['picture']:
        #     picture_file = save_picture(request.form['picture'])
            # current_user.image_file = picture_file
        current_user.username = request.form['username']
        current_user.email = request.form['email']
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        request.form['username'] = current_user.username
        request.form['email'] = current_user.email
    # image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account')


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method=="POST":
        post = Post(title=request.form['title'], content=request.form['content'], author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                            legend='New Post')


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
    if request.method=="POST":
        post.title = request.form['title']
        post.content =request.form['content']
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        request.form['title'] = post.title
        request.form['content'] = post.content
    return render_template('create_post.html', title='Update Post',
                         legend='Update Post')


@app.route("/post/<int:post_id>/delete",  methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page=request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=5)
    return render_template('user_posts.html', posts=posts ,user=user)