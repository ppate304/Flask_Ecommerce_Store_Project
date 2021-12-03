from os import name
from flask import render_template, request, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import login_user, current_user, logout_user, login_required
from .import bp as auth
from app.models import User, Item, Cart

@auth.route('/home')
@login_required
def home():
    return render_template('home.html.j2')

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        #do Login stuff
        email = request.form.get("email").lower()
        password = request.form.get("password")
                                #Database col = form inputted email
        u = User.query.filter_by(email=email).first()

        if u and u.check_password_hash(password):
            login_user(u)
            # Give the user Feedback thats you logged in successfully
            flash('You have logged in', 'success')
            return redirect(url_for("auth.home"))
        error_string = "Invalid Email password combo"
        return render_template('login.html.j2', error = error_string, form=form)
    return render_template('login.html.j2', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:

            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
        }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()

        except:
            error_string = "There was an error"
            return render_template('register.html.j2', form=form, error= error_string)
        return redirect(url_for('auth.login'))
    return render_template('register.html.j2', form=form)

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'danger')
        return redirect(url_for('auth.login'))

@auth.route('/shop_items/')
@login_required
def shop_items():
    items = Item.query.all()
    # if current_user.shop_items(items):
    #     flash(f"Added {items.name}to your cart", 'success')  
    #     return redirect(url_for('auth.shop_items'))
    return render_template('shop_item.html.j2', items=items)

@auth.route('/buy_items/<int:id>')
@login_required
def buy_items(id):
    buy_items = Item.query.get(id)
    current_user.buy_items(buy_items)
    flash(f"Added {buy_items.name} to your cart", 'success')  
    return redirect(url_for('auth.shop_items'))

@auth.route('/remove_items/<int:id>')
@login_required
def remove_items(id):
    remove_items = Item.query.get(id)
    current_user.remove_items(remove_items)
    flash(f"Added {remove_items.name} to your cart", 'success')  
    return redirect(url_for('auth.shop_items'))


@auth.route('/cart_items')
@login_required
def cart_items():
    cart_items = Item.query.join(Cart, Cart.item_id == Item.id).filter(Cart.user_id == current_user.id).all()
    print(cart_items)
    return render_template('show_items.html.j2', cart_items=cart_items)

@auth.route('/Check_out')
@login_required
def check_out():
    flash("Items have been checked out! Thank you for shopping at The Jewlery Store!", 'success')
    return render_template('home.html.j2')


