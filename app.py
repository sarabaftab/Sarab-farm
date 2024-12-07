from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from forms import ItemForm
from models import db, Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.route('/')
def inventory():
    items = Item.query.all()
    return render_template('inventory.html', items=items)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = ItemForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.id.data:  # Edit existing item
            item = Item.query.get(form.id.data)
            item.name = form.name.data
            item.description = form.description.data
            item.price = form.price.data
            item.available = form.available.data
            item.image_url = form.image_url.data  # Update image URL
            db.session.commit()
        else:  # Add new item
            new_item = Item(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                available=form.available.data,
                image_url=form.image_url.data  # Save image URL
            )
            db.session.add(new_item)
            db.session.commit()
        return redirect(url_for('admin'))
    items = Item.query.all()
    return render_template('admin.html', items=items, form=form)


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'cart' not in session:
        session['cart'] = []
    cart_items = [Item.query.get(item_id) for item_id in session['cart']]
    if request.method == 'POST':
        action = request.form['action']
        item_id = int(request.form['item_id'])
        if action == 'add':
            session['cart'].append(item_id)
        elif action == 'remove':
            session['cart'].remove(item_id)
        session.modified = True
        return redirect(url_for('cart'))
    return render_template('cart.html', cart_items=cart_items)

if __name__ == '__main__':
    app.run(debug=True)
