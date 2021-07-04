# flask-ecommerce-site-by-sak
Setup Project in Production Server (LocalHost) Steps


Just copy-paste this steps No need to Worry 



Requirements-> Python 3.8 Interpreter

Step 1:
Clone Repository 

- $git clone https://github.com/supsa-ak/flask-ecommerce-site-by-sak/  


Step 2:
Go to directory-> flask-ecommerce-site-by-sak


Step 3:
Create Virtual Environment

- $virtualenv myenv  


Step 4:
Activate Virtual Environment 

- $myenv/Scripts/activate


Step 5:
Install packages 

- $pip install -r requirements.txt


Step 6:
Run the Flask app 

- $python run.py


Step 7:
Open localhost in browser 

127.0.0.1:5000/


Don't forget to activate virtual environment after opening terminal

1. Home
    - Homepage is redirected to product page where list of 20 products is shown
    
2. to go to admin 127.0.0.1:5000/admin 
    - Operations CRUD
    - Form to add new product to website 
        Can add
        - Name of product
        - External image link
        - Price
    - Can see previously added products on website 
    - Update button to update product on website
    - Delete product from website

3. Products
    - Can see Name, Image and Price of product
    - By clicking on name of product goes to sub page with name, image and price
    - Add to Cart Button
   
4. Cart
    - Can add products to cart from product sub page and homepage
    -  cancel  button 
        - remove all items from cart
    - checkout button
        - goes to checkout page to place a card number
5. Json response api
    -  Go to http://127.0.0.1:5000/shop_api/(id of product)
        - It will give information of product in json format as api 
