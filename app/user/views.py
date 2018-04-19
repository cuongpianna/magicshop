from flask import render_template,url_for,redirect,g,request,flash,g,session
from ..models import User,Category,Product,Order
from .forms import ProfileForm
from werkzeug.utils import secure_filename
from app import db,ALLOW_EXTENSIONS,UPLOAD_FOLDER
from flask_login import current_user


import os
from . import user

def allowed_file(filename):
    return '.' in filename and filename.lower().rsplit('.', 1)[1] in ALLOW_EXTENSIONS

def count(session,cart):
    count = 0
    if cart in session:
        for d in session[cart]:
            for k,v in d.items():
                count = count+v
    else:
        count = 0
    return count

@user.before_request
def before_request():
    g.id = current_user.id
    g.number = count(session,'cart')
    g.categories = Category.query.all()
    g.order = {}
    g.total_cost = 0
    if "cart" in session:
        product_list = session['cart']
        for pl in product_list:
            for k,v in pl.items():
                product = Product.query.filter_by(name=k).first()
                g.order[k] = {
                    'price':product.price,
                    'name':k,
                    'quantity':v,
                    'subtotal':v*product.price,
                    'image':product.image,
                    'id':product.id
                }
    g.order = g.order.values()
    if g.order:
        for o in g.order:
            g.total_cost += o['subtotal']

@user.route('/edit',methods=['GET','POST'])
def edit_profile():
    form = ProfileForm()
    user = User.query.get(g.id)
    if form.validate_on_submit():
        user.address = form.address.data
        user.phone_number=form.phone_number.data
        avartar = form.avartar.data
        if 'avartar' in request.files:
            avartar = request.files['avartar']
            if avartar and allowed_file(avartar.filename):
                filename = secure_filename(avartar.filename)
                avartar.save(os.path.join(UPLOAD_FOLDER,filename))
                user.avartar = filename
        db.session.add(user)
        db.session.commit()
        flash('Cập nhật thành công.')
        return redirect(url_for('user.edit_profile'))
    else:
        form.address.data = user.address
        form.phone_number.data = user.phone_number
    return render_template('user/edit_profile.html',
                           form=form,
                           title='Chỉnh sửa thông tin')

@user.route('/orders')
def user_orders():
    orders = Order.query.filter_by(user_id=current_user.id)
    return render_template('user/orders.html',orders=orders,title='Đơn hàng')





