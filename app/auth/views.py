from flask import Flask,render_template,redirect,url_for,flash,g,session
from . import auth
from .forms import RegisterForm,LoginForm,ChangePasswordForm
from ..models import User,Category,Product
from app import db
from flask_login import login_user, logout_user, current_user, login_required


def count(session,cart):
    count = 0
    if cart in session:
        for d in session[cart]:
            for k,v in d.items():
                count = count+v
    else:
        count = 0
    return count

@auth.before_request
def before_request():
    #g.search = SearchForm()
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


@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.user_name.data,email = form.email.data,password_hash=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Đăng ký thành công!')
    return render_template('auth/register.html',
                           form=form,
                           title='Đăng ký')

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(url_for('home.index'))
        flash('Tài khoản hoặc mật khẩu không hợp lệ')
    return render_template('auth/login.html',
                           title='Đăng nhập',
                           form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất。')
    return redirect(url_for('auth.login'))

@auth.route('/change-password', methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    user = current_user
    if form.validate_on_submit():
        if user.check_password(form.old_password.data):
            user.password_hash=form.password.data
            db.session.add(user)
            flash('Mật khẩu của bạn đã thay đổi')
            return redirect(url_for('auth.change_password'))
        else:
            flash('Mật khẩu không hợp lệ.')
    return render_template('auth/change_password.html',
                           form=form,
                           title='Đổi mật khẩu')