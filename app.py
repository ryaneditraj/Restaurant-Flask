from flask import Flask, request
from flask import render_template, redirect
import random
import smtplib

# initialize variables
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
sender_email = "ryansfreefire@gmail.com"
sender_pass = "ryansfreefire123"
recipients_email = "ryansfreefire@gmail.com"
server.login(sender_email, sender_pass)



app = Flask(__name__)
orderid = 0
food = {
    'None':0,
    'Mango Juice':50,
    'Orange Juice':50,
    'Oreo Shake':120,
    'Lemon Juice':40,
    'Lemon Soda':80,
    'Apple Soda':90,
    'Apple Juice':70,
    'Burger':150,
    'Burger(4)':400,
    'Veg Pizza':200,
    'Chicken Pizza':400,
    'Pepperoni Pizza':500,
    'Hawaiian Pizza':450,
    'Naan':50,
    "Naan (2)":80,
    "Shawarma":120,
    'Shawarma(2)':200,
    'Chicken butter masala':230,
    'Panneer butter masala':190,
    'Chicken Biryani':350,
    'Mutton Biryani':300,
    'Veg Biryani':260,
    'Beef Biryani':320,
    'Chicken Fried Rice':200,
    'Veg Fried Rice':160,
    'Chicken Tandoori(Half)':300,
    'Chicken Tandoori':500,
    'French Fries':100,
    'Chicken Cutlet':35,
    'Chicken Cutlet(4)':100,
    'Chicken Nuggets':80,
    'Chicken Nuggets(4)':200,
    'Chicken 65':190,
}
total_price = 0
li_food = list(food)
cart = {}
print(type(food), type(cart))
foodk = []
foodv = []
len_food = len(food)


for key, value in food.items():
    print (key, value)
    foodk.append(key)
    foodv.append(value)
    
print(foodk, foodv)
print(f"food               price")
for k,v in food.items():
    print(f"{k}          {v}")
print(food.items())
app.secret_key="ryanisnotgretguyihope"
@app.route('/', methods=['GET', 'POST'])
def index():
    len_cart = len(cart)
    return render_template('index.html', food = food, foodk = foodk, foodv = foodv, len_food = len_food, len_cart = len_cart )

@app.route('/placeorder')
def placeorder():
    return render_template('placeorder.html')

@app.route('/order', methods=['GET', 'POST'])

def cart_add():
    if request.method == 'GET':
      product = request.args.get('food')
      number = (request.args.get('no'))

      print_cart(product, number)
      print(product)
      
      
    return redirect('/')
    
def print_cart(product, number):

    if food in cart:
        al_price = int(cart[product])
        num = al_price+int(number)
        cart[product] = num
    else:
        num = int(number)
        cart[product] = num
    print(cart)

@app.route('/cart', methods=['GET', 'POST'])

def food():
    
    print(total_price)
    return render_template('cart.html', cart = cart)


    
@app.route('/remove', methods=['GET', 'POST'])
def remove():

    if request.method == 'GET':
        rem_food = request.args.get('delete')
        cart.pop(rem_food)

    return redirect('/cart')
          
@app.route('/ordering', methods=['GET', 'POST'])
def ordering():
    if request.method == 'POST':
        name = request.form.get('name')
        phonenumber = request.form.get('phonenumber')
        numofpeo = request.form.get('numofpeo')
        table = request.form.get('table')
        order_status_var = name, phonenumber, numofpeo, table
        send_content = ("")
        orderid += random.randint(10000, 99999)
        for k, v in cart.items():
                send_content +=("{:<8} {:<15}\n".format(k, v))
        server.sendmail(str(sender_email),
                            recipients_email,
                            f"""
                            Name:{name}
                            Mobile Number:{phonenumber}
                            Number of people:{numofpeo}
                            Table:{table}
                            Order Id:{orderid}
                            {send_content}
                            """)
        return redirect('/orderplaced')
        print(name, phonenumber, numofpeo, table)
    return render_template('ordering.html')
@app.route('/orderplaced')
def orderplaced():
    
    
    cart.clear()
    return f"<h1>Dear User your order is placed.Your order id is {orderid}. Please note it down.<br><a href=\"/\">Go back to home</a></h1>"
app.run(debug=False, host="0.0.0.0")
