#!/usr/bin/env python3
"""Simple Flask app"""
from flask import render_template, request
from flask import render_template, abort
from models import Product, ProductSchema
from flask import redirect, url_for, session
import os
from flask import request, flash
from werkzeug.utils import secure_filename

from config import app, db


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def show_product():
    """Show product"""
    market = Product.query.all()
    productSchema = ProductSchema(many=True)
    return render_template("index.html", market=productSchema.dump(market))


@app.route('/add_to_cart/<int:product_id>', methods=['POST', 'GET'])
def add_to_cart(product_id):
    # Retrieve the product from the database using the product_id
    product = Product.query.get_or_404(product_id)

    # Get the current cart from the session or initialize an empty list
    cart = session.get('cart', [])

    if request.method == 'POST':
        # Get the quantity selected from the input field
        quantity_selected = int(request.form['quantity'])

        # Check if the product is already in the cart
        product_in_cart = next((item for item in cart if item['id'] == product.an_id), None)

        if product_in_cart:
            # If the product is already in the cart, update the quantity
            product_in_cart['quantity'] += quantity_selected
        else:
            # If the product is not in the cart, add it to the cart with the selected quantity
            cart.append({
                'id': product.an_id,
                'item': product.item,
                'price': product.price,
                'quantity': quantity_selected,
                'original_quantity': product.quantity  # Store the original quantity
            })

        # Update the cart in the session
        session['cart'] = cart

        # Update the quantity in the database
        product.quantity -= quantity_selected

        # Commit the changes to the database
        db.session.commit()

        # Redirect to the cart page
        return redirect(url_for('show_product'))

    # If it's a GET request, you might want to render a template or handle it differently
    return render_template('cart.html', product=product)



@app.route('/view_cart')
def view_cart():
    # Retrieve the cart from the session
    cart = session.get('cart', [])

    # Render a template to display the cart
    return render_template('cart.html', cart_items=cart)


@app.route('/update_cart_quantity/<int:product_id>', methods=['POST'])
def update_cart_quantity(product_id):
    # Retrieve the cart from the session
    cart = session.get('cart', [])

    # Find the item with the specified product_id in the cart
    item_to_update = next((item for item in cart if item['id'] == product_id), None)

    if item_to_update:
        # Update the quantity in the cart
        new_quantity = int(request.form['quantity'])
        item_to_update['quantity'] = new_quantity

        # Update the quantity in the database
        product = Product.query.get_or_404(product_id)
        product.quantity = (item_to_update['original_quantity'] - new_quantity)

        # Commit the changes to the database
        db.session.commit()

        # Update the cart in the session
        session['cart'] = cart

    # Redirect to the cart page
    return redirect(url_for('view_cart'))


@app.route("/admin_dashboard")
def admin_dashboard():
    market = Product.query.all()
    app.logger.info(market)  # Check the Flask console for this information
    productSchema = ProductSchema(many=True)
    return render_template("admin.html", market=productSchema.dump(market))

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        # Update the product details based on the submitted form data
        product.item = request.form['item']
        product.available = request.form['available']
        product.species = request.form['species']
        product.price = request.form['price']
        product.quantity = request.form['quantity']

        # Commit the changes to the database
        db.session.commit()
        
        # Redirect to the admin dashboard after editing
        return redirect(url_for('admin_dashboard'))
    
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Delete the product from the database
    db.session.delete(product)
    db.session.commit()
    
    # Redirect to the admin dashboard after deletion
    return redirect(url_for('admin_dashboard'))


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        # Get form data
        item = request.form.get("item")
        available = request.form.get("available")
        species = request.form.get("species")
        price = request.form.get("price")
        quantity = request.form.get("quantity")

        # Validate that the quantity is a positive integer
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be a positive integer")
        except ValueError:
            flash('Invalid quantity. Please enter a positive integer.')
            return redirect(request.url)

        # Check if the user provided an image URL
        image_url = request.form.get("image_url")

        if not image_url:
            flash('Image URL is required.')
            return redirect(request.url)

        # Create a new product and add it to the database with the image URL
        new_product = Product(
            item=item,
            available=available,
            species=species,
            price=price,
            quantity=quantity,
            image_url=image_url  # Use the provided image URL
        )
        db.session.add(new_product)
        db.session.commit()

        # Redirect to the admin dashboard
        return redirect(url_for("admin_dashboard"))

    return render_template("add_product.html")


@app.route('/remove_all_from_cart', methods=['POST'])
def remove_all_from_cart():
    # Retrieve the cart from the session
    cart = session.get('cart', [])

    # Iterate through the items in the cart and update the database
    for item in cart:
        product_id = item['id']
        quantity_removed = item['quantity']

        # Update the quantity in the database
        product = Product.query.get_or_404(product_id)
        product.quantity += quantity_removed

    # Clear the cart in the session to remove all items
    session['cart'] = []

    # Commit the changes to the database
    db.session.commit()

    # Redirect to the cart page
    return redirect(url_for('view_cart'))


@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    # Retrieve the cart from the session
    cart = session.get('cart', [])

    # Find the item with the specified product_id in the cart
    item_to_remove = next((item for item in cart if item['id'] == product_id), None)

    if item_to_remove:
        # Update the cart: Remove the item
        cart.remove(item_to_remove)

        # Update the quantity in the database
        product = Product.query.get_or_404(product_id)
        product.quantity += item_to_remove['quantity']  

        # Commit the changes to the database
        db.session.commit()

        # Update the cart in the session
        session['cart'] = cart

    # Redirect to the cart page
    return redirect(url_for('view_cart'))


if __name__ == "__main__":
    app.run()
