from flask import render_template,redirect,url_for,flash,session,request,jsonify,g
from . import home
from ..models import Product,Category,Order,OrderDetail
from .forms import SearchForm,CheckOutForm
from flask_login import current_user,login_required
import datetime

from app import db


def count(session,cart):
    count = 0
    if cart in session:
        for d in session[cart]:
            for k,v in d.items():
                count = count+v
    else:
        count = 0
    return count

@home.before_request
def before_request():
    g.search = SearchForm()
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

@home.route('/products/',defaults={'page_num': 1})
@home.route('/products/<int:page_num>')
@home.route('/products')
def index(page_num):
    pl = Product.query.paginate(per_page=12,page=page_num,error_out=False)
    return render_template('home.html',pl=pl,page_num=page_num,title='Sản phẩm')

@home.route('/search',methods = ['GET','POST'])
def search():
    #search = SearchForm()
    if request.method == 'POST' and g.search.validate_on_submit():
        return redirect(url_for('home.search_result',query=g.search.search.data))
    return redirect(url_for('home.index'))


@home.route('/search_results/<query>/',defaults={'page_num': 1})
@home.route('/search_results/<query>/<int:page_num>')
@home.route('/search_results/<query>')
def search_result(query,page_num):
    #products = Product.query.filter(Product.query.contains(query))
    products = Product.query.filter(Product.name.contains(query)).paginate(per_page=12,page=page_num,error_out=False)
    return render_template('search.html',query=query,products = products,title='Kết quả tìm kiêm',page_num=page_num)

@home.route('/product/<id>')
def product_detail(id):
    product = Product.query.get(id)
    categories = Category.query.all()
    return render_template('product_detail.html',product=product,categories=categories,title='Chi tiết sản phẩm')

@home.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    product = Product.query.get(id)
    q = 1
    #result =
    if session.get('cart'):
        if not any(product.name in d for d in session['cart']):
            session['cart'].append({product.name:q})
            #result=session['cart']
        elif any(product.name in d for d in session['cart']):
            for d in session['cart']:
                for k,v in d.items():
                    if k == product.name:
                        d[product.name]=v+1
                        session['cart'][0][k] = v+1

    else:
        session['cart'] = [{product.name:q}]
        #result=session['cart']
    # return jsonify(session['cart'])
    flash('Thêm thành công!')
    return redirect(url_for('home.cart'))

# @home.route('/add_to_cart')
# def add_to_cart():
#     return jsonify(result="helo")

@home.route('/cart')
def cart():
    categories = Category.query.all()
    order = {}
    total_cost = 0
    if "cart" in session:
        product_list = session['cart']
        for pl in product_list:
            for k,v in pl.items():
                product = Product.query.filter_by(name=k).first()
                order[k] = {
                    'price':product.price,
                    'name':k,
                    'quantity':v,
                    'subtotal':v*product.price,
                    'image':product.image,
                    'id':product.id
                }
    order = order.values()
    if order:
        for o in order:
            total_cost += o['subtotal']
    return render_template('carts.html',order=order,total_cost=total_cost,categories=categories,title='Giỏ hàng')

#ham nay bo?

@home.route('/remove_from_cart/<int:id>')
def remove_from_cart(id):
    product = Product.query.get(id)
    q = 1
    if session.get('cart'):
        if not any(product.name in d for d in session['cart']):
            session['cart'].append({product.name:q})
        elif any(product.name in d for d in session['cart']):
            for d in session['cart']:
                for k,v in d.items():
                    if k == product.name:
                        if v > 1:
                            d[product.name]=v-1
                        else:
                            session['cart'].remove(d)
                #d.update((k,q) for k,v in d.items() if k == product.name)
    else:
        session['cart'] = [{product.name:q}]

    flash('Bớt thành công!')
    return redirect(url_for('home.cart'))

@home.route('/genre/<category>/',defaults={'page_num': 1})
@home.route('/genre/<category>/<int:page_num>')
@home.route('/genre/<category>')
def category(category,page_num):
    categories = Category.query.all()
    cat = Category.query.filter_by(name = category).first()
    products = Product.query.filter_by(category=cat).all()
    pl = Product.query.filter_by(category=cat).paginate(per_page=12,page=page_num,error_out=False)
    return render_template('category.html',products=products,pl=pl,category=category,page=page_num,title='Sản phẩm')

@home.route('/checkout',methods=['GET','POST'])
@login_required
def check_out():
    form = CheckOutForm()
    if form.validate_on_submit():
        if 'cart' in session:
            order = Order(user_id=current_user.id, user_adress=form.user_adress.data, message=form.message.data,
                          created=datetime.datetime.now(),total_cost=g.total_cost)
            db.session.add(order)
            db.session.commit()
            id = order.id
            for o in g.order:
                s = OrderDetail(order_id=id, product_id=o['id'], quantity=o['quantity'])
                db.session.add(s)
                db.session.commit()
            flash('Hoàn tất quá trình giao dịch!')
            session.pop('cart')
            return redirect(url_for('home.check_out'))
        else:
            flash('Giỏ hàng trống! Vui lòng mua hàng để tiến hành thanh toán!')
    return render_template('checkout.html',form=form,title='Thanh toán')


