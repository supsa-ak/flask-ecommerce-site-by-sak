from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SECRET_KEY'] = 'qpowiecmnIhpjasdIaY'

db = SQLAlchemy(app)

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(200), nullable=False)
    imageurl = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Shop %r>' % self.productname

# db.create_all()

@app.route('/')
def home():
    title = "Home"
    return render_template('index.html', title=title)

@app.route('/cart/<int:id>', methods=['POST', 'GET'])
def cart(id):
    title = "Cart"

    cart = {}
    product_to_cart = Shop.query.get_or_404(id)
    print(product_to_cart, "sarthak")
    try:    
        cart.update(product_to_cart)
        return redirect('/cart')                
    except:
        return "There was a problem adding Product to cart"
    return render_template('cart.html', title=title, cart=cart)

@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    title = "Checkout"
    return render_template('checkout.html', title=title)

@app.route('/product')
def product():
    title = "Product"
    products = Shop.query.order_by(Shop.date_created)
    return render_template('product.html', title=title, products=products)

@app.route('/productdetails')
def productdetails():
    title = "Product Details"
    return render_template('productdetails.html', title=title)

@app.route('/success')
def success():
    title = "Success!"
    return render_template('success.html', title=title)

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    title = "Admin"
    
    products = Shop.query.order_by(Shop.date_created)
    if request.method == "POST":
        Product_Name = request.form['pname']
        Image_Url = request.form['imgurl']
        Product_Price = request.form['price']

        new_product = Shop(productname=Product_Name, imageurl=Image_Url, price=Product_Price)
       
        try: 
            db.session.add(new_product)
            db.session.commit()
            return redirect('/admin')
        except: 
            return "There was an error adding your Product"
    else:
        return render_template('admin.html', title=title, products=products)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    title = "Update Product"
    product_to_update = Shop.query.get_or_404(id)
    if request.method == "POST":
        product_to_update.name = request.form['pname']
        product_to_update.imageurl = request.form['imgurl']
        product_to_update.price = request.form['price']
        try:
            db.session.commit()
            return redirect('/admin')
        except: 
            return "There was a problem updating product"
    else:
        return render_template('update.html', title=title, product_to_update=product_to_update)

@app.route('/delete/<int:id>')
def delete(id):
    title = "Delete Product!"

    product_to_delete = Shop.query.get_or_404(id)
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        return redirect('/admin')
    except:
        return "There was a problem deleting Product"
    return render_template('admin.html', title=title)

app.run(debug=True)