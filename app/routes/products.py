# ============================================================================
# app/routes/products.py
# ============================================================================

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Product

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/')
@login_required
def list_products():
    products = Product.query.all()
    return render_template('products/list.html', products=products)

@products_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            category=request.form.get('category'),
            description=request.form.get('description'),
            active=request.form.get('active') == 'on',
            created_by_user_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('products.list_products'))

    return render_template('products/form.html', product=None)

@products_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.category = request.form.get('category')
        product.description = request.form.get('description')
        product.active = request.form.get('active') == 'on'
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products.list_products'))

    return render_template('products/form.html', product=product)

@products_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products.list_products'))
