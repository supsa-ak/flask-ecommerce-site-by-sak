from flask import Flask, render_template, request, redirect, url_for, abort, Response, jsonify

app = Flask(__name__)

app.config['SECRET_KEY'] = 'qpowiecmnIhpjasdIaY'

def MergeDict(dict1, dict2):
    return dict(list(dict1.items()) + list(dict2.items()))

@app.route('/')
def home():
    title = "Home"
    return redirect(url_for('product'))

def notpresent(var):
  for i in cart:
    if i["id"] == var["id"]:
      return False
  else:
    return True

def total():
    total = 0
    for i in cart:
      total += i["subtotal"]   
    return total

@app.route('/product', methods=['POST', 'GET'])
def product():
    title = "Product"    
    if request.method == 'POST':
        d = request.form.get('pid')
        q = int(request.form.get('quantity'))
        # print(q,'this is q')
        id = int(d) 
        id -= 1 
        p = products[id]   
        price = int(p["price"])
        # print(p, "this is product selected") 
        subtotal = 0
        for i in range (q):
          subtotal += price 
        # print(subtotal, 'this is price of selected product')
        if notpresent(p): 
          p["quantity"] = q
          p["subtotal"] = subtotal
          cart.append(p)
        # print(cart,  'This is product funciton')        
    length = len(cart)
    return render_template('product.html', title=title, products=products, l=length) 

@app.route('/productdetails/<int:id>', methods=['GET', 'POST'])
def productdetails(id):
    title = "Product Details"
    length = len(cart)
    return render_template('productdetails.html', title=title, l=length, products=products, id=id) 

@app.route('/cart')
def cart():
    title = "Cart"
    if len(cart)<=0:
        return redirect(url_for('home'))
    length = len(cart)
    return render_template('cart.html', title=title, cart=cart, l=length, total=total())

@app.route('/delete/<int:id>')
def delete(id):   
    for i in cart:
      if i["id"] == id:
        cart.remove(i)
    return redirect(url_for('cart'))

@app.route('/clearcart')
def clearcart():   
    cart.clear()
    return redirect(url_for('home'))

@app.route('/checkout', methods=['POST'])
def checkout():
    title = "Checkout"
    return render_template('checkout.html', title=title, t=total())

@app.route('/success', methods=['POST'])
def success():
    title = "Success"
    if request.method == "POST":
        purchase = request.form.get('purchase')
        purchase = int(''.join(c for c in purchase if c.isdigit()))
        t = total()
        if purchase == t:
            return render_template('success.html', title=title, purchase=purchase)
        elif purchase != t:
            abort(417)
        else: 
            return render_template('problem.html')

@app.route('/shop_api/<int:id>')
def shopapi(id): 
    id = id - 1  
    p = products[id] 
    return p

@app.route('/shop_api/')
def shopallapi():
    p = products
    return jsonify(p)

@app.route('/check-cart', methods=['POST'])
def checkcart():    
    if request.get_json:
        dataGet = request.get_json(force=True) 
        dataReply = 200
    else:         
        dataReply = 404
    return jsonify(dataReply)

@app.route('/check-checkout', methods=['POST'])
def checkcheckout():    
    if request.get_json:
        dataGet = request.get_json(force=True) 
        dataReply = 200
    else:         
        dataReply = 404
    return jsonify(dataReply)

@app.route('/check-card', methods=['POST'])
def checkcard():    
    if request.get_json:
        dataGet = request.get_json(force=True) 
        print(dataGet)
        dataReply = 200
    else:         
        dataReply = 404
    return jsonify(dataReply)


@app.route('/error')
def error():
    return render_template('code_404.html')

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

cart = []

products = [
 {
    "id":1,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/oneplus/oneplus-8-1.jpg", 
    "name": "OnePlus 8", 
    "price": 500,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":2,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/alcatel/tcl-10-pro-1.jpg", 
    "name": "TCL 10 Pro", 
    "price": 399,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":3,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s10-1.jpg", 
    "name": "Samsung Galaxy S10", 
    "price": 254,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":4,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/google/google-pixel-6-pro-r1.jpg", 
    "name": "Google Pixel 6 Pr", 
    "price": 299 ,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":5,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-12-pro-max-1.jpg", 
    "name": "Apple iPhone 12 Pro Max ", 
    "price": 999,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":6,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/nokia/nokia-x20-1.jpg", 
    "name": "Nokia X20", 
    "price": 199,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":7,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note10-pro-1.jpg", 
    "name": "Xiaomi Redmi Note 10 Pro", 
    "price": 354,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":8,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/sony/sony-xperia-1-iii-02.jpg", 
    "name": "Sony Xperia 1 III", 
    "price": 365,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":9,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/lg/lg-velvet-1.jpg", 
    "name": "LG Velvet 5G", 
    "price": 329.99,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":10,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/asus/asus-rog-phone-5-0.jpg", 
    "name": "Asus ROG Phone 5", 
    "price":829 ,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":11,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/htc/htc-desire-21-pro-5g-1.jpg", 
    "name": "HTC Desire 21 Pro 5G", 
    "price": 226,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":12,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/huawei/huawei-mate40-pro-1.jpg", 
    "name": "Huawei Mate 40 Pro 4G", 
    "price":271 ,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":13,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/oppo/oppo-reno6-pro-plus-1.jpg", 
    "name": "Oppo Reno6 Pro+ 5G", 
    "price": 499,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":14,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/vivo/vivo-iqoo-7-india-2.jpg", 
    "name": "vivo iQOO 7 (India)", 
    "price": 99.09,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":15,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/vivo/vivo-x60-pro-plus-1.jpg", 
    "name": "vivo X60t Pro+", 
    "price": 200,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":16,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/motorola/motorola-moto-g60-1.jpg", 
    "name": "Motorola Moto G60", 
    "price": 279,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":17,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/realme/realme-gt-5g-1.jpg", 
    "name": "Realme GT 5G", 
    "price": 549,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":18,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/tecno/tecno-phantom-x-1.jpg", 
    "name": "Tecno Phantom X", 
    "price":299 ,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":19,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/microsoft/microsoft-surface-duo-01.jpg", 
    "name": "Microsoft Surface Duo", 
    "price": 238,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  },
 {
    "id":20,
    "imgurl": "https://fdn2.gsmarena.com/vv/pics/lava/lava-z2-max-1.jpg", 
    "name": "Lava Z2 Max", 
    "price": 300,
    "quantity": 1,
    "stock": 5,
    "subtotal": 0
  }
]

app.run(debug=True)