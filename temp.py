@app.route('/session/cart', methods=['GET','POST'])
def session_cart():
    # use these defaults if cart isn't in session
    cart = session.get('cart', {'beer':0, 'wine':0, 'soda':0}) 
    ## TODO: determine from the session whether to show the cart
    ## Also, whether the customer is of age
    show = True
    print('show: {}'.format(show))
    print('cart: {}'.format(cart))
    if request.method == 'POST':
        # ordering something
        ## TODO: determine whether the person is of age and can order this
        ## item. Refuse if not
        item = request.form.get('itemid')
        cart[item] += 1
        flash('Thank you for buying a glass of '+item)
        session['cart'] = cart # store the updated cart
    return render_template('cart-template.html',
                           title='Beverage Orders',
                           cartContents=show,
                           cart=cart)