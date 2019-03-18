"""my_code"""
from flask import request, render_template, session, Blueprint, redirect, url_for
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash

from bakc.models import db, User, Categroy, Article
from utils.functions import is_login

blue = Blueprint('first', __name__)
blueweb = Blueprint('web', __name__)


# 博客系统后台首页跳转
@blue.route('/')  # 注册路由
@is_login  # 判断是否已有账号登录
def index():
    return render_template('/back/index.html')  # 跳转致index.html页面


# 用户注册
@blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        user = User.query.filter(User.u_name == username).first()
        if not username and not password and not password2:
            erorr = '注册信息不能为空!'
            return render_template('back/register.html', erorr=erorr)
        elif user:
            erorr = '账号已被注册!'
            return render_template('back/register.html', erorr=erorr)
        elif password == password2:
            use = User()
            use.u_name = username
            use.u_pass = generate_password_hash(password)
            db.session.add(use)
            db.session.commit()
            return redirect(url_for('first.login'))
        else:
            erorr = '两次密码不一致!'
            return render_template('back/register.html', erorr=erorr)


# 用户登录
@blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/back/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.u_name == username).first()
        if not username or not password:
            erorr = '账号或密码未填写'
            return render_template('back/login.html', erorr=erorr)
        elif not user:
            erorr = '该账号不存在!'
            return render_template('back/login.html', erorr=erorr)
        elif not user.status:
            erorr = '该账号已失效!'
            return render_template('back/login.html', erorr=erorr)
        elif check_password_hash(user.u_pass, password):
            session['user_id'] = user.id
            return redirect(url_for('first.index'))
        else:
            erorr = '密码输入有误!'
            return render_template('back/login.html', erorr=erorr)


# 用户退出
@blue.route('/logout/')
def logout():
    del session['user_id']
    return redirect(url_for('first.login'))


# 用户列表
@blue.route('/user_list/<int:id>/')
def usr_list(id):
    nums = User.query.all()
    num = nums.__len__()
    if num % 8:
        pages = num // 8 + 1
    else:
        pages = num // 8
    users = User.query.offset((id - 1) * 8).limit(8).all()
    return render_template('back/user_list.html', users=users, pages=pages, id=id)


# 用户删除
@blue.route('/label_user/<int:id>/')
def label_user(id):
    user = User.query.get(id)
    user.status = 0
    db.session.add(user)
    db.session.commit()
    return redirect('/back/user_list/1/')
    # return redirect(url_for('first.user_list', id=1))


# 文章类型列表
@blue.route('/cat_list/')
def cat_list():
    cats = Categroy.query.all()
    return render_template('back/category_list.html', cats=cats)


# 文章类型添加
@blue.route('/cat_type/', methods=['GET', 'POST'])
def cat_type():
    if request.method == 'GET':
        return render_template('back/category_type.html')
    if request.method == 'POST':
        aname = request.form.get('cattype')
        cat = Categroy.query.filter(Categroy.cat_name == aname).first()
        if not aname:
            erorr = '未填写任何内容，不能添加'
            return render_template('back/category_type.html', erorr=erorr)
        elif cat:
            erorr = '此类型已经存在'
            return render_template('back/category_type.html', erorr=erorr)
        else:
            cat = Categroy()
            cat.cat_name = aname
            db.session.add(cat)
            db.session.commit()
            return redirect(url_for('first.cat_list'))


# 删除文章类型
@blue.route('/del_type/<int:id>/')
def del_type(id):
    type = Categroy.query.get(id)
    db.session.delete(type)
    db.session.commit()
    return redirect(url_for('first.cat_list'))


# 文章列表
@blue.route('/art_list/<int:id>/')
def art_list(id):
    arts = Article.query.all()
    num = arts.__len__()
    if num % 10:
        pages = num // 10 + 1
    else:
        pages = num // 10
    arts = Article.query.offset((id - 1) * 10).limit(10).all()
    return render_template('back/article_list.html', arts=arts, id=id, pages=pages)


# 文章添加
@blue.route('/art_detail/', methods=['GET', 'POST'])
def art_detail():
    if request.method == 'GET':
        cats = Categroy.query.all()
        return render_template('back/article_detail.html', cats=cats)
    if request.method == 'POST':
        name = request.form.get('name')
        sketch = request.form.get('sketch')
        category = request.form.get('category')
        content = request.form.get('content')
        if not name or not sketch or not category or not content:
            erorr = '需要添加的数据未填写完整，请重新填写'
            cats = Categroy.query.all()
            return render_template('back/article_detail.html', erorr=erorr, cats=cats)
        else:
            art = Article()
            art.art_name = name
            art.sketch = sketch
            art.type_id = category
            art.content = content
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('first.art_list', id=1))


# 删除文章
@blue.route('/del_art/<int:id>/')
def del_art(id):
    art = Article.query.get(id)
    db.session.delete(art)
    db.session.commit()
    return redirect(url_for('first.art_list', id=1))


# 前台页面首页
@blueweb.route('/')
def web_index():
    conts = Article.query.all()
    tps = Categroy.query.all()
    return render_template('web/index.html', conts=conts, tps=tps)


# 前台页面分类列表显示
@blueweb.route('/<int:id>/')
def web_type_li(id):
    conts = Article.query.filter(Article.type_id == id)
    tps = Categroy.query.all()
    return render_template('web/index.html', conts=conts, tps=tps)


@blueweb.route('/search/', methods=['GET', 'POST'])
def search():
    tps = Categroy.query.all()
    if request.method == 'POST':
        value = request.form.get('keyboard')
        if value is None:
            return redirect(url_for('web.web_index'))
        else:
            conts = Article.query.filter(
                or_(Article.content.like('%' + value + '%'), Article.art_name.like('%' + value + '%'))).all()
            return render_template('web/index.html', tps=tps, conts=conts)
    if request.method == 'GET':
        conts = Article.query.all()
        return render_template('web/index.html', conts=conts, tps=tps)


# 关于我路由跳转
@blueweb.route('/about/')
def web_about():
    tps = Categroy.query.all()
    return render_template('web/about.html', tps=tps)


# 文章详情显示
@blueweb.route('/show_detail/<int:id>/')
def detail(id):
    art = Article.query.filter(Article.id == id).first()
    artf = Article.query.filter().first().id
    artp = Article.query.filter().all()
    artp = artp[artp.__len__() - 1].id
    tps = Categroy.query.all()
    idf = id - 1
    idp = id + 1
    while id >= artf:
        art1 = Article.query.filter(Article.id == idf).first()
        if art1:
            break
        idf -= 1
        if idf < artf:
            art1 = None
            break
    while id <= artp:
        art2 = Article.query.filter(Article.id == idp).first()
        if art2:
            break
        idp += 1
        if idp > artp:
            art2 = None
            break
    return render_template('web/detail.html', art=art, tps=tps, art1=art1, art2=art2)


@blue.route('/create_db/')
def create_db():
    db.create_all()
    # db.drop_all()
    return '创建成功'
