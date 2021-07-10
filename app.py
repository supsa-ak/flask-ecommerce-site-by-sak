from flask import Flask, render_template, request, redirect, session, url_for, jsonify, flash, abort
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'qpowiecmnIhpjasdIaY'

def MergeDict(dict1, dict2):
    return dict(list(dict1.items()) + list(dict2.items()))

@app.route('/')
def home():
    title = "Home"
    return redirect(url_for('product'))

@app.route('/product', methods=['POST', 'GET'])
def product():
    title = "Product"    
    if request.method == 'POST':
        d = request.form.get('pid')
        id = int(d) 
        id -= 1
        # print(id)
        product_cart = products[id]
        DictItems = {id:{'id':product_cart['id'], 'name':product_cart['name'], 'imgurl':product_cart['imgurl'], 'price':product_cart['price'],'quantity':0, 'stock':product_cart['stock']}}
        print(DictItems, "this is dictitem")
        if 'Shoppingcart' in session:
            # print(type(session['Shoppingcart']), 'waht is this')
            # print("session is there", id)
            # dist = session['Shoppingcart']
            # dist.update(DictItems)
            # session['Shoppingcart'] = dist
            # # session['Shoppingcart'] = MergeDict((session['Shoppingcart']), DictItems)
            # print(session['Shoppingcart'], 'this is session cart')
            # print(len(session['Shoppingcart']), 'this is lenght')
            return redirect(request.referrer)
        else:
            print("bye")
            session['Shoppingcart'] = DictItems
            return redirect(request.referrer)
    return render_template('product.html', title=title, products=products) 

@app.route('/productdetails/<int:id>', methods=['GET', 'POST'])
def productdetails(id):
    title = "Product Details"
    return render_template('productdetails.html', title=title, products=products, id=id) 


products = [
 {
    "id":1,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/oneplus/oneplus-8-1.jpg", 
    "name": "OnePlus 8", 
    "price": 500,
    "stock": 5
  },
 {
    "id":2,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/alcatel/tcl-10-pro-1.jpg", 
    "name": "TCL 10 Pro", 
    "price": 399,
    "stock": 5
  },
 {
    "id":3,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s10-1.jpg", 
    "name": "Samsung Galaxy S10", 
    "price": 254,
    "stock": 5
  }
]





app.run(debug=True)