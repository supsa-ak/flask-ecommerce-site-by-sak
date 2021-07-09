from flask import Flask, render_template, request, redirect, session, url_for, jsonify, flash, abort
from flask_http_response import success, result, error
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from datetime import datetime
from flask_migrate import Migrate
from requests.exceptions import Timeout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SECRET_KEY'] = 'qpowiecmnIhpjasdIaY'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def MagerDicts(dict1,dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return dict1  + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String(200), nullable=False)
    imageurl = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, default=5)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): 
        return '<Shop %r>' % self.id

# db.create_all()

@app.route('/')
def home():
    title = "Home"
    return redirect(url_for('product'))

@app.route('/total')
def totalfun():
    total = 0 
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
            total +=  float(product['price'])  * int(product['quantity'])
            t = "%.2f" % total
    return t

@app.route('/cart', methods=['POST', 'GET'])
def cart():
    title = "Cart"
    if 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    return render_template('cart.html', title=title, total=totalfun)

@app.route('/check-cart', methods=['POST', 'GET'])
def checkcart():
    title = "Cart Check"
    if 'Shoppingcart' in session:                
        if id in session['Shoppingcart']:
            for key, item in session['Shoppingcart'].items():
                if int(key) == int(id):
                    session.modified = True                        
        return render_template('check-cart.html', title=title)
    elif 'Shoppingcart' not in session or len(session['Shoppingcart'])<=0:
        return redirect(url_for('home'))
    else:
        abort(404)

@app.route('/checkout', methods=['POST'])
def checkout():
    title = "Checkout"
    return render_template('checkout.html', title=title, t=totalfun())

@app.route('/check-checkout', methods=['POST', 'GET'])
def checkcheckout():
    title = "Checkout Check"
    if 'Shoppingcart' in session:                
        if id in session['Shoppingcart']:
            for key, item in session['Shoppingcart'].items():
                if int(key) == int(id):
                    session.modified = True                        
        return render_template('check-checkout.html', title=title)
    else:
        abort(404)

@app.route('/product', methods=['POST', 'GET'])
def product():
    title = "Home | Products"
    products = Shop.query.order_by(Shop.date_created)
    quantity = 1
    try:
        id  = request.form.get('pid')
        quantity = request.form.get('quantity')
        # print(quantity)
        if id and request.method == "POST":
            product_cart = Shop.query.filter_by(id=id).first()
            DictItems = {id:{'id':product_cart.id, 'name':product_cart.productname, 'imgurl':product_cart.imageurl, 'quantity':quantity, 'price':product_cart.price}}
            # print(DictItems)
            if 'Shoppingcart' in session:                
                if id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    return render_template('product.html', title=title, products=products)

@app.route('/productdetails/<int:id>', methods=['GET', 'POST'])
def productdetails(id):
    title = "Product Details"
    productDetails = Shop.query.get_or_404(id)
    return render_template('productdetails.html', title=title, productDetails=productDetails)

@app.route('/success', methods=['POST'])
def success():
    title = "Success"
    if request.method == "POST":
        purchase = request.form.get('purchase')
        t = totalfun()
        if purchase == t:
            return render_template('success.html', title=title, purchase=purchase)
        elif purchase != t:
            abort(417)
        else: 
            return render_template('problem.html')
    
@app.route('/check-card', methods=['POST', 'GET'])
def checkcard():
    title = "Checkout Card"
    if 'Shoppingcart' in session:                
        if id in session['Shoppingcart']:
            for key, item in session['Shoppingcart'].items():
                if int(key) == int(id):
                    session.modified = True                        
        return render_template('check-card.html', title=title, t=totalfun())
    else:
        abort(404)

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    title = "Admin"
    
    products = Shop.query.order_by(Shop.date_created)
    if request.method == "POST":
        Product_Name = request.form['pname']
        Image_Url = request.form['imgurl']
        Product_Price = request.form['price']
        Stock = request.form['stock']
        new_product = Shop(productname=Product_Name, imageurl=Image_Url, price=Product_Price, stock=Stock)
       
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
        product_to_update.productname = request.form['pname']
        product_to_update.imageurl = request.form['imgurl']
        product_to_update.price = request.form['price']
        product_to_update.stock = request.form['stock']
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

@app.route('/delcartitem/<int:id>')
def delcartitem(id):
    title = "Delete Cart Item!"
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return render_template(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('cart'))


@app.route('/clearcart')
def clearcart():
    title = "clearcart"
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
    return redirect(url_for('home'))

@app.route('/shop_api/<int:id>')
def shop_api(id):
    title = "Json"
    product_to_api = Shop.query.get_or_404(id)
    json_res = {id:{'name':product_to_api.productname, 'imgurl':product_to_api.imageurl, 'price':product_to_api.price}}

    return jsonify(json_res)

@app.errorhandler(417)
def page_not_found(e):
   
    return render_template('code_417.html'), 417

@app.errorhandler(400)
def page_not_found(e):
    return render_template('code_400.html'), 400

@app.errorhandler(403)
def page_not_found(e):
    return render_template('code_403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('code_404.html'), 404

@app.errorhandler(405)
def page_not_found(e):
    return render_template('code_405.html'), 405

@app.errorhandler(500)
def page_not_found(e):
    return render_template('code_500.html'), 500

app.run(debug=True)