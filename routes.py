from flask import render_template, redirect, flash, url_for, jsonify, request,session
from os import path
from forms import RegisterForm, LoginForm, ProductForm, ClubForm,ContactForm
from ext import app, db
from models import Product, User, Club, CartItem, ContactMessage
from flask_login import login_user , logout_user, login_required , current_user
from sqlalchemy import or_




profiles = []
@app.route("/")
def home():
    products = Product.query.all()
    role = current_user.role if current_user.is_authenticated else None
    return render_template("davaleba.html", products=products, role=role)




@app.route("/add_to_cart/<int:product_id>", methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem(product=product)
    cart_item.create()

    return redirect("/")


@app.route('/update_cart/<int:cart_item_id>', methods=['POST'])
def update_cart(cart_item_id):
     new_quantity = int(request.form.get('quantity'))
     cart_item = CartItem.query.get_or_404(cart_item_id)
     cart_item.quantity = new_quantity

     cart_item.save()
     return redirect("/cart")


@app.route("/remove_from_cart/<int:cart_item_id>",methods=['POST',"DELETE"])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    cart_item.delete()
    return redirect("/cart")
@app.route("/cart")
@login_required
def cart():
    cart_items = CartItem.query.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total_price=total_price)


@app.route("/cartitem/<int:item_id>")
@login_required
def view_cart_item(item_id):
    cart_item = CartItem.query.get(item_id)
    if cart_item is None:

        return render_template("not_found.html"), 404


    return render_template("cart_item.html", cart_item=cart_item)

@app.route("/stadium")
def stadium():
    clubs = Club.query.all()
    role = current_user.role if current_user.is_authenticated else None
    return render_template("stadium.html", clubs=clubs, role=role)

@app.route("/club/<int:club_id>")
def club(club_id):



    club = Club.query.get(club_id)
    return render_template("club_details.html", club=club)
@app.route("/product/<int:product_id>")
def product(product_id):


    product = Product.query.get(product_id)

    return render_template("product_details.html", product=product )




@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        else:
            flash("იუზერნეიმი ან პაროლი არ ემთხვევა")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")
@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        User.query.filter_by(username="username").first()
        new_user = User(username=form.username.data, password=form.password.data)
        new_user.create()
        return redirect("/login")
    return render_template("register.html", form=form)

@app.route("/profile/<int:profile_id>")
def profile(profile_id):
    print("Received profile id", profile_id)
    return render_template("profile.html", user=profiles[profile_id])






@app.route("/create_club", methods=["GET", "POST"])
@login_required
def create_club():
    form = ClubForm()
    if form.validate_on_submit():
        new_club = Club(name=form.name.data, address=form.address.data)

        image = form.img.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)

        new_club.img = image.filename
        new_club.create()
        return redirect("/stadium")
    return render_template("create_clubs.html", form=form)


@app.route("/edit_club/<int:club_id>", methods=["GET", "POST"])
@login_required
def edit_club(club_id):
    club = Club.query.get(club_id)
    form = ClubForm(name=club.name, address=club.address)
    if form.validate_on_submit():
        club.name = form.name.data
        club.address = form.address.data



        club.save()
        return redirect("/stadium")
    return render_template("create_clubs.html", form=form)
@app.route("/delete_club/<int:club_id>")
@login_required
def delete_club(club_id):
    club = Club.query.get(club_id)
    club.delete()

    return redirect("/stadium")

@app.route("/order")
@login_required
def order():
    return render_template("order.html")

@app.route("/create_product", methods=["GET", "POST"])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data)

        image = form.img.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)

        new_product.img = image.filename
        new_product.create()
        return redirect("/")
    return render_template("create_product.html", form=form)


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data



        product.save()
        return redirect("/")
    return render_template("create_product.html", form=form)

@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    product.delete()

    return redirect("/")

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_message = ContactMessage(
            email=form.email.data,
            username=form.username.data,
            city=form.city.data,
            problem=form.problem.data

        )

        new_message.create()
        return redirect("/thankyou")




    return render_template('contact.html', form=form)

@app.route("/succesfuladd")
@login_required
def successfuladd():
    return render_template("addtocart.html")

