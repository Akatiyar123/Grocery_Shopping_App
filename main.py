from flask import Flask , render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
import matplotlib
import os
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
from flask_bcrypt import Bcrypt
from datetime import datetime
matplotlib.use('Agg')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.sqlite3"
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(15))

class StoreManager(db.Model):
    __tablename__ = "admin"
    manager_id = db.Column(db.Integer , primary_key = True , autoincrement = True)
    manager_name = db.Column(db.String , nullable = False)
    manager_pass = db.Column(db.String , nullable = False)    
    

class Category(db.Model):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    category_image_url = db.Column(db.String(200))
    # image_data = db.Column(db.LargeBinary, nullable=False)



class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    product_image = db.Column(db.String(200))
    quantity = db.Column(db.Integer, nullable=False)
    remaining = db.Column(db.Integer)
    product_date = db.column(db.Integer)
    # expiry_date = db.Column(db.Date)  # Date field for product expiry date
    # manufactured_date = db.Column(db.Date)  # Date field for product manufactured date
    product_category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    # category = db.relationship('Category', backref=db.backref('products', lazy=True))


class Cart(db.Model):
    __tablename__ = "cart"
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    user_id = db.Column(db.Integer)
    cname = db.Column(db.String(100), nullable=False)
    pname = db.Column(db.String(200), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    # product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    cquantity = db.Column(db.Integer, default=1)
    cart_total = db.Column(db.Integer , nullable = False) 
    # product = db.relationship('Product', backref=db.backref('carts', lazy=True))
    # user = db.relationship('User', backref=db.backref('cart', lazy=True))

    def __init__(self,user_id, cname, pname, cquantity, cart_total):
        self.user_id = user_id
        self.cname = cname 
        self.pname = pname
        self.cquantity = cquantity
        self.cart_total = cart_total
        self.cart_id = None
# class CartItem(db.Model):
#     __tablename__ = "cartitem"
#     item_id = db.Column(db.Integer, primary_key=True)
#     cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
#     quantity = db.Column(db.Integer, default=1)
#     cart = db.relationship('Cart', backref=db.backref('items', lazy=True))
#     product = db.relationship('Product', backref=db.backref('carts', lazy=True))

# class Order(db.Model):
#     __tablename__ = "order"
#     order_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
#     order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
#     total_amount = db.Column(db.Float, nullable=False)
#     user = db.relationship('User', backref=db.backref('orders', lazy=True))

# class OrderItem(db.Model):
#     __tablename__ = "orderitem"
#     order_item_id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
#     product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
#     quantity = db.Column(db.Integer, default=1)
#     price_per_unit = db.Column(db.Float, nullable=False)
#     order = db.relationship('Order', backref=db.backref('items', lazy=True))
#     product = db.relationship('Product', backref=db.backref('orders', lazy=True))

# class DeliveryAddress(db.Model):
#     __tablename__ = "deliveryaddress"
#     address_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
#     address_line1 = db.Column(db.String(200), nullable=False)
#     address_line2 = db.Column(db.String(200))
#     city = db.Column(db.String(100), nullable=False)
#     state = db.Column(db.String(100), nullable=False)
#     pin_code = db.Column(db.String(10), nullable=False)
#     user = db.relationship('User', backref=db.backref('addresses', lazy=True))




db.create_all()

@app.route("/")
def hello_world():

    return render_template("index.html")

@app.route("/user_signup" , methods = ['GET' , 'POST'])
def user_signup():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        username = request.form['username']
        mail = request.form['email']
        phone_no = request.form['phone_number']

        # return [name , password , username , mail, phone_no]

        user_confirm = User.query.filter_by(username = username).all()
        if(user_confirm == []):
            password = bcrypt.generate_password_hash(password)
            user = User(username = username , name = name , password = password , email = mail, phone_number = phone_no)
            db.session.add(user)
            db.session.commit()

            id = User.query.filter_by(username = username).all()[0].user_id
            return redirect(url_for("category_list" , user_id = id ))
        else:
            # print(1)
            return render_template("user_login.html", msg = "User already exist, Please Login")
        

        # [0]
        # return (str(user == None))
    
        # pass
    else:
        return render_template("user_signup.html")

@app.route("/user_login" , methods = ['GET' , 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username = username).all()
        if(len(user)>0):
            if bcrypt.check_password_hash(user[0].password, password):
                id = user[0].user_id
                # name = user[0].user_name
                return redirect(url_for("category_list", user_id = id))
            else:
                return render_template("user_login.html" , msg = "Incorrect Password" , msg1 = "Please Enter a Valid Password.")
        else:
            return render_template("user_login.html" , msg = "User not Found." , msg1 = "Please Enter a Valid Usename.") 
    else:
        return render_template("user_login.html")
    
@app.route("/<user_id>/category_list" , methods = ['GET' , 'POST'])
def category_list(user_id):
    if request.method == "POST":
        param = request.form["search"]
        categoryList = Category.query.filter_by(category_name = param).all()
        user = User.query.filter_by(user_id = user_id).first()
        name = user.username
        return render_template("category_list.html" , user_id=user_id , categories = categoryList , name = name)


        # pass
    else:
        categoryList = Category.query.all()
        user = User.query.filter_by(user_id = user_id).first()
        name = user.username
        return render_template("category_list.html" , user_id=user_id , categories = categoryList , name = name)
    

    
@app.route("/<user_id>/<category_id>/product_list" , methods = ['GET' , 'POST'])
def product_list(user_id , category_id):
    if request.method == "POST":
        # print("balle ballle")
        param = request.form["search"]
        # cquantity = request.form["quantity"]
        # cart = Cart(cquantity = cquantity)
        # db.session.add(cart)
        # db.session.commit()
        productList = Product.query.filter_by(product_name = param).all()
        # showList.reverse()
        user = User.query.filter_by(user_id = user_id).first()
        name = user.username
        return render_template("product_list.html" , user_id=user_id ,category_id=category_id, name = name ,products = productList)

        # return ["Search Param : ",param]
    else:
        # print("dukh hua")
        productList = Product.query.filter_by(product_category_id = category_id ).all()
        category_name = Category.query.filter_by(category_id=category_id).first().category_name
        print(category_name)
        # showList.reverse()
        user = User.query.filter_by(user_id = user_id).first()
        print(user_id)
        name = user.username
        print(productList[0])

        

        return render_template("product_list.html" , user_id=user_id ,category_id=category_id, name = name ,products = productList,category_name = category_name)
    


@app.route("/<user_id>/<category_id>/<product_id>/add_cart" , methods = ['GET' , 'POST'])
def add_cart(user_id , category_id , product_id) :
    if request.method == "POST":
        print("balle ballle")
        # param = request.form["search"]
        cquantity = request.form["quantity"]

        product = Product.query.filter_by(product_id = product_id).all()[0]
        category = Category.query.filter_by(category_id = category_id).all()[0]
        cname = category.category_name
        pname = product.product_name
        quantity = cquantity
        user_id = user_id
        total = int(quantity)*product.price
        cart = Cart(cquantity = cquantity, cname = cname, pname = pname, cart_total = total, user_id = user_id)
        db.session.add(cart)
        db.session.commit()
        curr_quantity = Product.query.filter_by(product_id = product_id).first().remaining

        Product.query.filter_by(product_id = product_id).first().remaining = int(curr_quantity) - int(quantity)
        db.session.commit()
        productList = Product.query.filter_by(product_category_id = category_id ).all()
        category_name = Category.query.filter_by(category_id=category_id).first().category_name
        print(category_name)
        # showList.reverse()
        user = User.query.filter_by(user_id = user_id).first()
        print(user_id)
        name = user.username
        

        return render_template("product_list.html" , user_id=user_id ,category_id=category_id, name = name ,products = productList,category_name = category_name)
        # productList = Product.query.filter_by(product_name = param).all()
        # showList.reverse()
        # user = User.query.filter_by(user_id = user_id).first()
        # name = user.username
        # return render_template("product_list.html" , user_id=user_id ,category_id=category_id, name = name ,products = productList)

        # return ["Search Param : ",param]
    else:
        print("dukh hua")
        productList = Product.query.filter_by(product_category_id = category_id ).all()
        category_name = Category.query.filter_by(category_id=category_id).first().category_name
        print(category_name)
        # showList.reverse()
        user = User.query.filter_by(user_id = user_id).first()
        print(user_id)
        name = user.username
        

        return render_template("product_list.html" , user_id=user_id ,category_id=category_id, name = name ,products = productList,category_name = category_name)
from sqlalchemy.sql import select   
@app.route("/<user_id>/cart", methods = ['GET','POST'])
def cart(user_id):
    if request.method == 'POST':
        return render_template("cart.html")
    else:
        items = db.session.query(Cart).filter_by(user_id=user_id).all()
        total = 0
        for item in items:
            total+=item.cart_total
        print(total)
        return render_template("cart.html" , cart = items, total = total)

    
@app.route("/admin_login" , methods = ['GET' , 'POST'])
def admin_login():
    if request.method == 'POST':
        ad_name = request.form['username']
        passw = request.form['password']
        print(ad_name , passw)
        # admin = AdminLogin.query.filter_by(admin_name = ad_name).all()
        admin = {"admin_name" : "Aman" , "admin_pass" : "12345"}
        print(admin)
        if(admin["admin_name"] == ad_name):
            if(admin["admin_pass"] == passw):
                name = admin["admin_name"]
                return redirect(url_for("category_list_admin" , name = name ))
                # return "user found"

            else:
                return render_template("admin_login.html" , msg = "Incorrect Password")
        else:
            return render_template("admin_login.html" , msg = "Please input valid UserName.")
    else:
        return render_template("admin_login.html" )
    
@app.route("/<name>/category_list_admin" , methods = ['GET' , 'POST'])
def category_list_admin(name):
    if request.method == "POST":
        pass
    else:
        CategoryList = Category.query.all()
        # venueList.reverse()
        # print(venueList)

        return render_template("category_list_admin.html" , name=name , categories = CategoryList)
    
app.config['UPLOAD_FOLDER'] = 'static'
    
@app.route("/<name>/create_category" , methods = ['GET' , 'POST'])
def create_category(name):
    # print(name)
    if request.method == "POST":
        category_name = request.form["category_name"]
        category_image = request.files["category_image"]
        if category_image:
            # Save the image file to the server
            filename = secure_filename(category_image.filename)
            category_image.save(os.path.join(app.config['UPLOAD_FOLDER'] , filename))
            # Create a new Category object and save it to the database
            category = Category(category_name=category_name,category_image_url='/static/'+filename)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for("category_list_admin" , name = name ))

        # return("ruko jara sabar kro")
    else:
        return render_template("create_category.html" , name = name)
    
@app.route("/<name>/<category_id>/remove_category" , methods = ['GET' , 'POST'])
def remove_category(name , category_id):
    if request.method == "POST":
        pass
    else:
        # print("inside remove_category" ,category_id )
        return render_template("remove_category_confirmation.html" , name=name , category_id=category_id)
        # return redirect(url_for("confirm_remove", name=name , category_id=category_id))
    
@app.route("/<name>/<category_id>/confirm_remove" , methods = ['GET' , 'POST'])
def confirm_remove(name,category_id):
    if request.method == "POST":
        pass
    
    else:
        # print("inside confirm" , category_id)
        cat = Category.query.filter_by(category_id=category_id).first()
        # db.session.query(Product).filter(Product.product_category_id==category_id).delete()
        db.session.delete(cat)

        db.session.query(Product).filter(Product.product_category_id==category_id).delete()
        db.session.commit()

        db.session.commit() 
        # return render_template("category_list_admin.html", name = name)
        return redirect(url_for("category_list_admin",name = name))
    
@app.route("/<name>/<category_id>/product_list_admin" , methods = ['GET' , 'POST'])
def product_list_admin(name , category_id):
    if request.method == "POST":
        pass
    else:
        # print(product_category_id, category_id)
        productList = Product.query.filter_by(product_category_id = category_id ).all()
        print(productList)
        # showList.reverse()
        # show_list.reverse()
        category_name = Category.query.filter_by(category_id=category_id).first().category_name
        print(category_name)

        return render_template("product_list_admin.html" ,name = name , category_id=category_id, products = productList , category_name = category_name)
    
@app.route("/<name>/<category_id>/create_product" , methods = ['GET' , 'POST'])
def create_product(name , category_id):
    if request.method == "POST":
        # return "I am here."
        product_name = request.form["product_name"]
        product_quantity = request.form["quantity"]
        product_image = request.files["product_image"]
        product_price = request.form["price"]
        product_date = request.form["date"]

        # category_capacity = Category.query.filter_by(category_id = category_id).first().category_capacity
        if product_image:
            # Save the image file to the server
            file = secure_filename(product_image.filename)
            product_image.save(os.path.join(app.config['UPLOAD_FOLDER'] , file))
            # Create a new Category object and save it to the database
            product = Product(product_name = product_name, product_category_id = category_id ,quantity = product_quantity, product_image = '/static/'+file, price = product_price , remaining = product_quantity , product_date = product_date)
            db.session.add(product)
            db.session.commit()
            return redirect(url_for("product_list_admin",name = name, category_id = category_id))
            # return([product_name, product_quantity, product_price ])

    else:
        return render_template("create_product.html" , category_id = category_id , name = name)
    
@app.route("/<name>/<category_id>/<product_id>/remove_product" , methods = ['GET' , 'POST'])
def remove_product(name , category_id , product_id):
    if request.method == "POST":
        pass
    else:
        return render_template("remove_product_confirmation.html" , name = name , product_id = product_id , category_id=category_id)
    
@app.route("/<name>/<category_id>/<product_id>/confirm_remove_product" , methods = ['GET' , 'POST'])
def confirm_remove_product(name , category_id , product_id):
    if request.method == "POST":
        pass
    else:
        product = Product.query.filter_by(product_id = product_id).first()
        # print(ven)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for("product_list_admin" , category_id = category_id , name = name))

@app.route("/<name>/<category_id>/edit_category", methods=['GET', 'POST'])
def edit_category(name, category_id):
    category = Category.query.filter_by(category_id=category_id).first()
    print(category)
    if request.method == "POST":
        print(1)
        category_name = request.form.get("category_name", category.category_name)
        category_image = request.files.get("category_image")
        if category_image:
            filename = secure_filename(category_image.filename)
            category_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            category.category_image_url = '/static/' + filename

        category.category_name = category_name

        # Commit the changes to the database
        db.session.commit()

        # Redirect to the category list page
        return redirect(url_for("category_list_admin", name=name))

    else:
        # Render the edit category template with the current category information
        # print('Yhan aaye ho')
        return render_template("edit_category.html", name=name, category_id=category_id, category=category)

@app.route("/<name>/<category_id>/<product_id>/edit_product" , methods = ['GET' , 'POST'])
def edit_show(name , category_id , product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    if request.method == "POST":
        product_name = request.form.get("product_name", product.product_name)
        product_capacity = request.form.get("product_capacity", product.quantity)
        product_image = request.files.get("category_image")
        if product_image:
            filename = secure_filename(product_image.filename)
            product_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.product_image_url = '/static/' + filename

        product.product_name = product_name
        product.quantity = product_capacity

        db.session.commit()
        return redirect(url_for("product_list_admin", name=name, category_id = category_id))
    else:
               
        return render_template("edit_product.html" , name=name , category_id=category_id, product_id = product_id, product = product) 

if __name__ == "__main__":
    app.run(debug=True , port = 8000)
