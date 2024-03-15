import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from Qcart import app, db, bcrypt
from Qcart.forms import ContactForm,RegistrationForm, LoginForm
from Qcart.models import User,Contact,Order
from flask_login import login_user, current_user, logout_user, login_required


from flask import jsonify
app.app_context().push()

db.create_all()



@app.route("/")
def home():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    cform = ContactForm()
    return render_template('bindex.html',cform=cform)

@app.route("/register", methods=['GET', 'POST'])
def register():
    cform = ContactForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('bregister.html', title='Register', form=form,cform=cform)


@app.route("/login", methods=['GET', 'POST'])
def login():
    cform = ContactForm()

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('store'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('blogin.html', title='Login', form=form,cform=cform)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/success')
def success():
    return "Your message has been sent. Thank you!"



@app.errorhandler(404)
def error_404(error):
    cform = ContactForm()

    return render_template('errors/404.html',cform=cform),404



@app.errorhandler(403)
def error_404(error):
    cform = ContactForm()

    return render_template('errors/404.html',cform=cform),403


@app.errorhandler(500)
def error_404(error):
    cform = ContactForm()

    return render_template('errors/404.html',cform=cform),500


@app.route('/contact', methods=['POST'])
def contact():
    cform = ContactForm()

    form = ContactForm()
    if form.validate_on_submit():
        new_message = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('success'))
    
    return render_template('bindex.html', form=form,cform=cform)  




def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    cform = ContactForm()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('baccount.html', title='Account',
                           image_file=image_file, cform=cform)

@app.route("/cart")
@login_required
def cart():    
    cform = ContactForm()
    user_id = current_user.id
    user_orders = Order.query.filter_by(user_id=current_user.id).all()

    return render_template('bcart.html',cform=cform,
                            user_id=user_id)


@app.route("/store")
def store():    
    cform = ContactForm()

    return render_template('bstore.html',cform=cform)


@app.route("/order", methods=['POST'])
def order():
    # Assuming you're receiving JSON data in the request body
    data = request.json

    # Extract data from JSON
    items = data.get('items')
    prices = data.get('prices')
    watch7 = data.get('Apple Watch Series 7')
    watch3 = data.get('Apple Watch SE')
    watchSE = data.get('Apple Watch Series 3')
    user_id = data.get('user_id')

    # Create a new order instance
    order = Order(user_id=user_id,items=items, prices=prices, watch7=watch7, watchSE=watch3, watch3=watchSE)

    # Add the new order to the database session
    db.session.add(order)

    # Commit the changes to the database
    db.session.commit()

    # Return a JSON response
    return jsonify({'message': 'Order received successfully'})



@app.route("/orders")
@login_required
def displayorders():
    cform = ContactForm()
    user_id = current_user.id
    user_orders = Order.query.filter_by(user_id=current_user.id).all()

    return render_template('borders.html', cform=cform, user_id=user_id, user_orders=user_orders if user_orders else [])

