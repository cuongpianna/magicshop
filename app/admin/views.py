from flask import Flask, render_template,redirect, url_for, flash,request
from . import admin
from .forms import AdminAddCategory,ProductAdmin
from ..models import Category,Product,Order,OrderDetail,User
from app import db,ALLOW_EXTENSIONS,UPLOAD_FOLDER
from werkzeug.utils import secure_filename
from functools import wraps
from flask_login import login_required, current_user

import os



def allowed_file(filename):
    return '.' in filename and filename.lower().rsplit('.', 1)[1] in ALLOW_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            return redirect('/')
        return f(*args,**kwargs)
    return decorated_function


@admin.route('/')
@login_required
@admin_required
def index():
    return render_template('admin_base.html')

@admin.route('/genres/add',methods = ['GET','POST'])
@login_required
@admin_required
def add_genres():
    form = AdminAddCategory()
    if form.validate_on_submit():
        genre = Category(name = form.name.data)
        db.session.add(genre)
        db.session.commit()
        flash('Thêm thành công!')
        return redirect(url_for('admin.admin_genres'))
    return render_template('admin/admin_add_category.html',form=form)

@admin.route('/genres')
@login_required
@admin_required
def admin_genres():
    genres = Category.query.order_by(Category.name)
    return render_template('admin/genres.html',genres=genres)

@admin.route('/genres/delete/<id>')
@login_required
@admin_required
def delete_genres(id):
    genre = Category.query.get(id)
    db.session.delete(genre)
    db.session.commit()
    flash('Xoá thành công!')
    return redirect(url_for('admin.admin_genres'))

@admin.route('/genres/edit/<id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_genres(id):
    form = AdminAddCategory()
    genre = Category.query.get(id)
    if form.validate_on_submit():
        genre.name = form.name.data
        db.session.add(genre)
        db.session.commit()
        flash("Cập nhật thành công!")
        if request.args.get('next'):
            return redirect(request.args.get('next'))
        return redirect(url_for('admin.admin_genres'))
    else:
        form.name.data = genre.name
    return render_template('admin/admin_add_category.html',form=form)

@admin.route('/product/add',methods=['GET','POST'])
@login_required
@admin_required
def add_product():
    form = ProductAdmin()
    if form.validate_on_submit():
        name = form.name.data
        category = Category.query.get_or_404(form.cagetory.data).id
        price = form.price.data
        description = form.description.data
        image = form.image.data
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_FOLDER,filename))
        product = Product(name,price,category,filename,description)
        db.session.add(product)
        db.session.commit()
        flash('Thêm thành công!')
    return render_template('admin/admin_add_product.html',form=form)

@admin.route('/products')
@login_required
@admin_required
def admin_product():
    products = Product.query.order_by(Product.id)
    return render_template('/admin/product.html',products=products)

@admin.route('/product/edit/<id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_product(id):
    form = ProductAdmin()
    product = Product.query.get(id)
    if form.validate_on_submit():
        product.name=form.name.data
        product.description=form.description.data
        product.category_id=Category.query.get_or_404(form.cagetory.data).id
        product.price=form.price.data
        image = form.image.data
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_FOLDER,filename))
                product.image = filename
        db.session.add(product)
        db.session.commit()
        flash('Cập nhật thành công!')
    else:
        form.name.data = product.name
        form.description.data=product.description
        form.image.data=product.image
        form.price.data=product.price
        form.cagetory.data=product.category_id
    return render_template('admin/admin_add_product.html',form=form)

@admin.route('/product/delete/<id>',methods = ['GET','POST'])
@login_required
@admin_required
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    flash('Xóa thành công')
    return redirect(url_for('admin.admin_product'))

@admin.route('/orders')
@login_required
@admin_required
def admin_orders():
    order = Order.query.order_by(Order.id)
    return render_template('admin/orders.html',order=order)

@admin.route('/order/update/<id>',methods = ['GET','POST'])
@login_required
@admin_required
def admin_updateorders(id):
    order = Order.query.get(id)
    order.status = True
    db.session.add(order)
    db.session.commit()
    flash('Đã duyệt đơn hàng')
    return redirect(url_for('admin.admin_orders'))

@admin.route('/orders/<status>')
@login_required
@admin_required
def orders(status):
    order = Order.query.filter_by(status=status)
    return render_template('admin/orders.html',order=order)

@admin.route('/users')
@login_required
@admin_required
def admin_users():
    users = User.query.order_by(User.id.desc())
    return render_template('admin/users.html',users=users)

@admin.route('/order_details/<id>')
@login_required
@admin_required
def admin_detail(id):
    order = Order.query.get(id)
    details = OrderDetail.query.filter_by(order_id = id)
    total_cost = 0
    return render_template('admin/detail.html',details=details,order=order)




