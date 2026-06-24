from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
import webbrowser
import threading
import random
import os
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "grandmasrecipes"
app.config['SESSION_PERMANENT'] = True


app.config['MYSQL_HOST'] = 'mainline.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tqMSxumfFaZLERMWgQUjRdlziQQmuyrK'
app.config['MYSQL_PORT'] = 26574
app.config['MYSQL_DB'] = 'grandmas_recipes'

# PROFILE IMAGE UPLOAD
UPLOAD_FOLDER = os.path.join('static', 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'yourgmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


# SPLASH
@app.route('/')
def splash():
    return render_template('splash.html')


# HOME

@app.route('/home')
def home():

    category = request.args.get('category')

    cur = mysql.connection.cursor()

    # Products Filter
    if category:

        cur.execute("""
        SELECT * FROM products
        WHERE category=%s
        """,(category,))

    else:

        cur.execute("""
        SELECT * FROM products
        """)

    products = cur.fetchall()

    # Variants
    cur.execute("""
    SELECT * FROM product_variants
    """)

    variants = cur.fetchall()

    # Wishlist 
    wishlist_ids = []

    if 'user_id' in session:

        cur.execute("""
        SELECT product_id
        FROM wishlist
        WHERE user_id=%s
        """,(session['user_id'],))

        wishlist = cur.fetchall()

        wishlist_ids = [x[0] for x in wishlist]

    cur.close()

    return render_template(
        'index.html',
        products=products,
        variants=variants,
        wishlist_ids=wishlist_ids
    )

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute("""
        INSERT INTO users
        (fullname,email,phone,password)
        VALUES (%s,%s,%s,%s)
        """,(fullname,email,phone,password))

        mysql.connection.commit()
        cur.close()

        flash("Registration Successful")

        return redirect('/login')

    return render_template('register.html')


# LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute("""
        SELECT * FROM users
        WHERE email=%s AND password=%s
        """, (email, password))

        user = cur.fetchone()

        cur.close()

        if user:

            session.permanent = True
            session['user_id'] = user[0]
            session['user_name'] = user[1]

            return redirect('/home')

        flash("Invalid Login")

    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


# PROFILE
@app.route('/profile')
def profile():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM users WHERE id=%s",
        (session['user_id'],)
    )

    user = cur.fetchone()

    cur.close()

    return render_template(
        'profile.html',
        user=user
    )

# update profile

@app.route('/upload_profile', methods=['POST'])
def upload_profile():

    if 'user_id' not in session:
        return redirect('/login')

    file = request.files['profile_image']

    if file.filename != "":

        filename = secure_filename(file.filename)

        file.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

        cur = mysql.connection.cursor()

        cur.execute("""
        UPDATE users
        SET profile_image=%s
        WHERE id=%s
        """,(filename, session['user_id']))

        mysql.connection.commit()
        cur.close()

    return redirect('/profile')

# remove profile

@app.route('/remove_profile_photo', methods=['POST'])
def remove_profile_photo():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    UPDATE users
    SET profile_image=NULL
    WHERE id=%s
    """,(session['user_id'],))

    mysql.connection.commit()
    cur.close()

    return redirect('/profile')

# edit profile

@app.route('/edit_profile', methods=['GET','POST'])
def edit_profile():

    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':

        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']

        cur = mysql.connection.cursor()

        cur.execute("""
        UPDATE users
        SET address=%s,
            city=%s,
            state=%s,
            pincode=%s
        WHERE id=%s
        """,(
            address,
            city,
            state,
            pincode,
            session['user_id']
        ))

        mysql.connection.commit()
        cur.close()

        return redirect('/profile')

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM users WHERE id=%s",
        (session['user_id'],)
    )

    user = cur.fetchone()

    cur.close()

    return render_template(
        'edit_profile.html',
        user=user
    )

# favourites

@app.route('/favorites')
def favorites():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT products.*
        FROM wishlist
        JOIN products
        ON wishlist.product_id = products.id
        WHERE wishlist.user_id=%s
    """, (session['user_id'],))
    products = cur.fetchall()

    cur.execute("""
        SELECT * FROM product_variants
    """)
    variants = cur.fetchall()

    cur.close()

    return render_template(
        'favorites.html',
        products=products,
        variants=variants
    )

#  add to favourites

@app.route('/add_favorite/<int:product_id>')
def add_favorite(product_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    INSERT INTO favorites(user_id, product_id)
    VALUES(%s,%s)
    """,(
        session['user_id'],
        product_id
    ))

    mysql.connection.commit()
    cur.close()

    return redirect('/home')
# ADD TO CART

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():

    if 'user_id' not in session:
        return redirect('/login')

    product_id = request.form['product_id']
    variant_id = request.form['variant_id']
    quantity = request.form['quantity']

    if variant_id == "" or variant_id == "Select Weight":
        flash("Please Select Weight")
        return redirect('/home')

    cur = mysql.connection.cursor()

    cur.execute("""
    INSERT INTO cart
    (user_id,product_id,variant_id,quantity)
    VALUES (%s,%s,%s,%s)
    """,(
        session['user_id'],
        product_id,
        variant_id,
        quantity
    ))

    mysql.connection.commit()
    cur.close()

    flash("Added To Cart")

    return redirect('/cart')
#  buy product

@app.route('/buy_now', methods=['POST'])
def buy_now():

    if 'user_id' not in session:
        return redirect('/login')

    product_id = request.form['product_id']
    variant_id = request.form['variant_id']
    quantity = request.form['quantity']

    if variant_id == "":
        return redirect('/home')

    session['buy_now_product_id'] = product_id
    session['buy_now_variant_id'] = variant_id
    session['buy_now_quantity'] = quantity
    session['buy_now'] = True

    return redirect('/payments')

# CART

@app.route('/cart')
def cart():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT
    cart.id,
    products.name,
    products.image,
    product_variants.weight,
    product_variants.price,
    cart.quantity

    FROM cart
    JOIN products
    ON cart.product_id = products.id

    JOIN product_variants
    ON cart.variant_id = product_variants.id

    WHERE cart.user_id=%s
    """,(session['user_id'],))

    items = cur.fetchall()

    cur.close()

    return render_template(
        'cart.html',
        items=items
    )


# REMOVE CART
@app.route('/remove_cart/<int:id>')
def remove_cart(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM cart WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()
    cur.close()

    return redirect('/cart')

# whishlist

@app.route('/wishlist')
def wishlist():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT products.*
    FROM wishlist

    JOIN products
    ON wishlist.product_id=products.id

    WHERE wishlist.user_id=%s
    """,(session['user_id'],))

    products = cur.fetchall()

    cur.close()

    return render_template(
        'wishlist.html',
        products=products
    )


# TOGGLE WISHLIST

@app.route('/toggle_wishlist/<int:product_id>')
def toggle_wishlist(product_id):

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT * FROM wishlist
    WHERE user_id=%s AND product_id=%s
    """,(user_id, product_id))

    existing = cur.fetchone()

    if existing:

        cur.execute("""
        DELETE FROM wishlist
        WHERE user_id=%s AND product_id=%s
        """,(user_id, product_id))

    else:

        cur.execute("""
        INSERT INTO wishlist
        (user_id, product_id)
        VALUES (%s,%s)
        """,(user_id, product_id))

    mysql.connection.commit()
    cur.close()

    return redirect('/home')

# CHECKOUT

@app.route('/checkout')
def checkout():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT fullname, address, city, state, pincode, phone
        FROM users
        WHERE id=%s
    """, (session['user_id'],))

    user = cur.fetchone()
    cur.close()

    if not user[1]:
        return redirect('/addresses?from=checkout')

    return redirect('/payments')

# save profile address

@app.route('/save_profile_address', methods=['POST'])
def save_profile_address():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    UPDATE users
    SET address=%s,
        city=%s,
        state=%s,
        pincode=%s,
        phone=%s
    WHERE id=%s
    """,(
        request.form['address'],
        request.form['city'],
        request.form['state'],
        request.form['pincode'],
        request.form['phone'],
        session['user_id']
    ))

    mysql.connection.commit()
    cur.close()

    flash("Address Saved Successfully")
    return redirect('/profile')


# save / update address

@app.route('/save_address', methods=['POST'])
def save_address():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    UPDATE users
    SET address=%s,
        city=%s,
        state=%s,
        pincode=%s,
        phone=%s
    WHERE id=%s
    """,(
        request.form['address'],
        request.form['city'],
        request.form['state'],
        request.form['pincode'],
        request.form['phone'],
        session['user_id']
    ))

    mysql.connection.commit()
    cur.close()

    source = request.referrer

    if source and "from=buy" in source:
        return redirect('/payments')

    return redirect('/addresses')

# PAYMENTS
@app.route('/payments')
def payment():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT fullname, phone, address, city, state, pincode
    FROM users
    WHERE id=%s
    """,(session['user_id'],))

    user = cur.fetchone()

    address_missing = False
    
    if not user[2] or not user[3] or not user[5]:
        address_missing = True

    # BUY NOW
    if session.get('buy_now'):

        cur.execute("""
        SELECT price
        FROM product_variants
        WHERE id=%s
        """,(session['buy_now_variant_id'],))

        variant = cur.fetchone()

        total = float(variant[0]) * int(session['buy_now_quantity'])

    else:

        cur.execute("""
        SELECT c.quantity,pv.price
        FROM cart c
        JOIN product_variants pv
        ON c.variant_id=pv.id
        WHERE c.user_id=%s
        """,(session['user_id'],))

        items = cur.fetchall()

        total = 0

        for item in items:
            total += float(item[1]) * int(item[0])

    city = str(user[3]).lower()
    city = city.replace(".", "").replace(" ", "")
    print("CITY =", city)

    # FREE DELIVERY
    if city in ['jangareddygudem', 'jangareddigudem']:
        delivery_charge = 0
        free_delivery = True
    else:
        delivery_charge = 50
        free_delivery = False

    grand_total = total + delivery_charge

    cur.close()

    return render_template(
    "payment.html",
    user=user,
    total=total,
    delivery_charge=delivery_charge,
    grand_total=grand_total,
    free_delivery=free_delivery,
    address_missing=address_missing
)

# PLACE ORDER

@app.route('/place_order', methods=['POST'])
def place_order():

    if 'user_id' not in session:
        return redirect('/login')

    payment_method = request.form.get('payment_method')

    if not payment_method:
        flash("Please Select Payment Method")
        return redirect('/payments')
    
    cur = mysql.connection.cursor()

    # USER DETAILS
    cur.execute("""
    SELECT fullname,address,city,state,pincode,phone
    FROM users
    WHERE id=%s
    """,(session['user_id'],))

    user = cur.fetchone()

    customer_name = user[0]

    full_address = f"{user[1]}, {user[2]}, {user[3]}, {user[4]}"
    phone = user[5]


    # BUY NOW OR CART
    if session.get('buy_now'):

        cart_items = [(
            session['buy_now_product_id'],
            session['buy_now_variant_id'],
            session['buy_now_quantity']
        )]

    else:

        cur.execute("""
        SELECT product_id,variant_id,quantity
        FROM cart
        WHERE user_id=%s
        """,(session['user_id'],))

        cart_items = cur.fetchall()

    # TOTAL CALCULATION
    total = 0

    for item in cart_items:

        variant_id = item[1]
        quantity = int(item[2])

        cur.execute("""
        SELECT price
        FROM product_variants
        WHERE id=%s
        """,(variant_id,))

        variant = cur.fetchone()

        if variant:

            price = float(variant[0])

            total += (price * quantity)
            
            city = user[2].strip().lower()
            city = city.replace(".", "").replace(" ", "")
            print("CITY =", city)


# FREE DELIVERY AREA
    if city in ['jangareddygudem', 'jangareddigudem']:
        delivery_charge = 0
        free_delivery = True

    else:
        free_delivery = False
        
        if total < 500:
            delivery_charge = 50

        elif total < 1000:
            delivery_charge = 30

        else:
            delivery_charge = 0
        grand_total = total + delivery_charge

# CREATE SINGLE ORDER

        cur.execute("""
        INSERT INTO orders
        (
            user_id,
            total_amount,
            status,
            address,
            phone,
            customer_name,
            payment_method,
            payment_status,
            delivery_charge
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,(
            session['user_id'],
            grand_total,
            'Placed',
            full_address,
            phone,
            customer_name,
            payment_method,
            'Paid',
            delivery_charge
        ))

        order_id = cur.lastrowid

        # SAVE ORDER ITEMS
        
        for item in cart_items:
            
            product_id = item[0]
            variant_id = item[1]
            quantity = int(item[2])

            cur.execute("""
            SELECT name
            FROM products
            WHERE id=%s
            """,(product_id,))

            product = cur.fetchone()

            product_name = product[0]

            cur.execute("""
            SELECT price
            FROM product_variants
            WHERE id=%s
            """,(variant_id,))

            variant = cur.fetchone()

            price = float(variant[0])

            cur.execute("""
            INSERT INTO order_items
            (
                order_id,
                product_id,
                product_name,
                price,
                quantity
            )
            VALUES(%s,%s,%s,%s,%s)
            """,(
                order_id,
                product_id,
                product_name,
                price,
                quantity
            ))

    # CLEAR CART
    if session.get('buy_now'):

        session.pop('buy_now_product_id', None)
        session.pop('buy_now_variant_id', None)
        session.pop('buy_now_quantity', None)
        session.pop('buy_now', None)

    else:

        cur.execute("""
        DELETE FROM cart
        WHERE user_id=%s
        """,(session['user_id'],))

    mysql.connection.commit()
    cur.close()

    return render_template(
        "order_success.html",
        total=total,
        delivery_charge=delivery_charge,
        grand_total = total + delivery_charge
    )

# USER ORDERS

@app.route('/orders')
def orders():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT *
    FROM orders
    WHERE user_id=%s
    ORDER BY id DESC
    """,(session['user_id'],))

    orders = cur.fetchall()

    cur.close()

    return render_template(
        'orders.html',
        orders=orders
    )

# cancel orders

@app.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    UPDATE orders
    SET status='Cancelled'
    WHERE id=%s
    AND user_id=%s
    """, (order_id, session['user_id']))

    mysql.connection.commit()
    cur.close()

    flash("Order Cancelled Successfully")

    return redirect('/orders')
# adminn

@app.route('/admin')
def admin():

    if 'admin_id' not in session:
        return redirect('/admin/login')

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cur.fetchall()

    cur.close()

    return render_template('admin.html', orders=orders)

# ADMIN DASHBOARD
@app.route('/admin/dashboard')
def admin_dashboard():

    if 'admin_id' not in session:
        return redirect('/admin/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT
        id,
        customer_name,
        phone,
        address,              
        total_amount,
        payment_method,
        status,
        created_at

    FROM orders 

    ORDER BY id DESC
    """)

    orders = cur.fetchall()

    cur.execute("""
    SELECT COUNT(*) FROM users
    """)
    users_count = cur.fetchone()[0]

    cur.execute("""
    SELECT COUNT(*) FROM orders
    """)
    orders_count = cur.fetchone()[0]

    cur.execute("""
    SELECT SUM(total_amount)
    FROM orders
    """)
    sales = cur.fetchone()[0]

    cur.close()

    return render_template(
        'admin/dashboard.html',
        orders=orders,
        users_count=users_count,
        orders_count=orders_count,
        sales=sales
    )

# admin status

@app.route('/admin/update_status/<int:order_id>', methods=['POST'])
def update_status(order_id):

    if 'admin_id' not in session:
        return redirect('/admin/login')

    status = request.form['status']

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE orders
        SET status=%s
        WHERE id=%s
    """,(status, order_id))

    mysql.connection.commit()

    cur.close()

    flash("Order Status Updated Successfully")

    return redirect('/admin/dashboard')


# admin login

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute("""
        SELECT * FROM admin
        WHERE username=%s AND password=%s
        """, (username, password))

        admin = cur.fetchone()
        cur.close()

        if admin:
            session['admin_id'] = admin[0]
            return redirect('/admin/dashboard')

        flash("Invalid Login")

    return render_template('admin/login.html')


# ADMIN PRODUCTS

@app.route('/admin/products')
def admin_products():

    if 'admin_id' not in session:
        return redirect('/admin/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT *
    FROM products
    ORDER BY id DESC
    """)

    products = cur.fetchall()

    cur.close()

    return render_template(
        'admin_products.html',
        products=products
    )

# admin add product

@app.route('/admin/add_product', methods=['GET','POST'])
def add_product():

    if 'admin_id' not in session:
        return redirect('/admin/login')

    if request.method == 'POST':

        name = request.form['name']
        description = request.form['description']
        category = request.form['category']

        image_file = request.files['image']

        filename = ""

        if image_file.filename != "":

            filename = secure_filename(image_file.filename)

            image_file.save(
                os.path.join(
                    "static/images",
                    filename
                )
            )

        cur = mysql.connection.cursor()

        cur.execute("""
        INSERT INTO products
        (name,description,image,category)
        VALUES(%s,%s,%s,%s)
        """,(
            name,
            description,
            filename,
            category
        ))

        product_id = cur.lastrowid

        weights = request.form.getlist('weight[]')
        prices = request.form.getlist('price[]')

        for w,p in zip(weights,prices):

            cur.execute("""
            INSERT INTO product_variants
            (product_id,weight,price)
            VALUES(%s,%s,%s)
            """,(product_id,w,p))

        mysql.connection.commit()
        cur.close()

        return redirect('/admin/products')

    return render_template('add_product.html')

# edit product

@app.route('/admin/edit_product/<int:id>', methods=['GET','POST'])
def edit_product(id):

    if 'admin_id' not in session:
        return redirect('/admin/login')

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        name = request.form['name']
        description = request.form['description']
        category = request.form['category']

        image_file = request.files['image']

        if image_file.filename != "":

            filename = secure_filename(image_file.filename)

            image_file.save(
                os.path.join(
                    "static/images",
                    filename
                )
            )

            cur.execute("""
            UPDATE products
            SET
            name=%s,
            description=%s,
            image=%s,
            category=%s
            WHERE id=%s
            """,(
                name,
                description,
                filename,
                category,
                id
            ))

        else:

            cur.execute("""
            UPDATE products
            SET
            name=%s,
            description=%s,
            category=%s
            WHERE id=%s
            """,(
                name,
                description,
                category,
                id
            ))

        variant_ids = request.form.getlist('variant_id[]')
        weights = request.form.getlist('weight[]')
        prices = request.form.getlist('price[]')

        for vid,w,p in zip(variant_ids,weights,prices):

            cur.execute("""
            UPDATE product_variants
            SET
            weight=%s,
            price=%s
            WHERE id=%s
            """,(w,p,vid))

        mysql.connection.commit()

        return redirect('/admin/products')

    cur.execute("""
    SELECT *
    FROM products
    WHERE id=%s
    """,(id,))

    product = cur.fetchone()

    cur.execute("""
    SELECT *
    FROM product_variants
    WHERE product_id=%s
    """,(id,))

    variants = cur.fetchall()

    cur.close()

    return render_template(
        'edit_product.html',
        product=product,
        variants=variants
    )

# delete product

@app.route('/admin/delete_product/<int:id>')
def delete_product(id):

    if 'admin_id' not in session:
        return redirect('/admin/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    DELETE FROM product_variants
    WHERE product_id=%s
    """,(id,))

    cur.execute("""
    DELETE FROM products
    WHERE id=%s
    """,(id,))

    mysql.connection.commit()
    cur.close()

    return redirect('/admin/products')

# ADMIN USERS
@app.route('/admin/users')
def admin_users():

    if 'admin_id' not in session:
        return redirect('/admin/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT * FROM users
    ORDER BY id DESC
    """)

    users = cur.fetchall()

    cur.close()

    return render_template(
    'admin/users.html',
    users=users
    )


# ADMIN ORDERS
@app.route('/admin/orders')
def admin_orders():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT * FROM orders
        ORDER BY id DESC
    """)

    orders = cur.fetchall()

    cur.close()

    return render_template(
        'admin/orders.html',
        orders=orders
    )

# upadate order

@app.route('/admin/update_order/<int:order_id>', methods=['POST'])
def update_order(order_id):

    if 'admin_id' not in session:
        return redirect('/admin/login')

    status = request.form['status']

    cur = mysql.connection.cursor()

    cur.execute("""
    UPDATE orders
    SET status=%s
    WHERE id=%s
    """,(status,order_id))

    mysql.connection.commit()
    cur.close()

    return redirect('/admin/dashboard')

# admin bill

@app.route('/admin/bill/<int:order_id>')
def admin_bill(order_id):

    if 'admin_id' not in session:
        return redirect('/admin/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT
        id,
        customer_name,
        phone,
        address,
        total_amount,
        payment_method,
        status,
        created_at

    FROM orders

    WHERE id=%s
    """,(order_id,))

    order = cur.fetchone()

    cur.execute("""
    SELECT
        p.name,
        oi.quantity,
        oi.price

    FROM order_items oi

    JOIN products p
    ON oi.product_id = p.id

    WHERE oi.order_id=%s
    """,(order_id,))

    items = cur.fetchall()

    cur.close()

    return render_template(
        'admin/bill.html',
        order=order,
        items=items
    )

# admin invoice

@app.route('/admin/invoice/<int:order_id>')
def admin_invoice(order_id):

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM orders WHERE id=%s", (order_id,))
    order = cursor.fetchone()

    return render_template("invoice.html", order=order)

# admin logout

@app.route('/admin/logout')
def admin_logout():

    session.pop('admin_id',None)

    return redirect('/admin/login')

#  address
@app.route('/addresses')
def addresses():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cur.fetchone()
    cur.close()

    return render_template('addresses.html', user=user)

# edit address

@app.route('/edit_address')
def edit_address():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
    user = cur.fetchone()
    cur.close()

    return render_template('edit_address.html', user=user)

# update address

@app.route('/update_address', methods=['POST'])
def update_address():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    UPDATE users
    SET
    fullname=%s,
    phone=%s,
    address=%s,
    city=%s,
    state=%s,
    pincode=%s
    WHERE id=%s
    """,(

        request.form['fullname'],
        request.form['phone'],
        request.form['address'],
        request.form['city'],
        request.form['state'],
        request.form['pincode'],
        session['user_id']

    ))

    mysql.connection.commit()
    cur.close()

    return redirect('/payments')

# forgot password

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'POST':

        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:

            otp = str(random.randint(100000, 999999))

            session['reset_otp'] = otp
            session['reset_email'] = email

            msg = Message(
                "Password Reset OTP",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )

            msg.body = f"Your OTP is: {otp}"

            # ✅ SAFE MAIL SEND (HERE ONLY)
            try:
                mail.send(msg)
                print("OTP sent successfully")
            except Exception as e:
                print("MAIL ERROR:", e)

            return redirect('/verify_otp')

        flash("Email not found")
        return redirect('/forgot_password')

    return render_template('forgot_password.html')

# verify otp
@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():

    if request.method == 'POST':

        entered_otp = request.form['otp']

        if entered_otp == session.get('reset_otp'):
            return redirect('/reset_password')

        flash("Invalid OTP")

    return render_template('verify_otp.html')

# reset password
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():

    if request.method == 'POST':

        new_password = request.form['new_password']
        email = session.get('reset_email')

        cur = mysql.connection.cursor()

        cur.execute("""
            UPDATE users
            SET password=%s
            WHERE email=%s
        """, (new_password, email))

        mysql.connection.commit()
        cur.close()

        flash("Password Updated Successfully")
        return redirect('/login')

    return render_template('reset_password.html')

if __name__ == "__main__":

    threading.Timer(
        1.5,
        open_browser
    ).start()

    app.run(
        debug=True,
        use_reloader=False
    )