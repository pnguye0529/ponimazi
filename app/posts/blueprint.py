import bcrypt
from flask import Blueprint, render_template, session, flash
from flask import request, redirect, url_for

from flask_security import login_required

from models import *
from .forms import *
from app import db

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def post_create():
    form = PostForm()

    if request.method == 'POST':
        title = request.form.get('title')
        abstract = request.form.get('abstract')
        body = request.form.get('body')

        try:
            post = Post(title=title, abstract=abstract, body=body)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
        except:
            print('Traceback is too long')
        return redirect(url_for('posts.post_detail', slug=post.slug))
    return render_template('posts/post_create.html', form=form)


# localhost:5000/list
@posts.route('/')
def posts_list():
    search = request.args.get('search')
    if search:
        posts = Post.query.filter(Post.title.contains(search) | Post.body.contains(search) | Post.abstract.contains(search))
        flash('Search Found', category='success')
    else:
        posts = Post.query.order_by(Post.created.desc())

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = posts.paginate(page=page, per_page=2)

    return render_template('posts/posts.html', posts=posts, pages=pages)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('posts/post_detail.html', post=post)


@posts.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    return render_template('posts/tag_detail.html', tag=tag)


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
def post_update(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        flash('Edit Completed!', category='success')
        return redirect(url_for('posts.post_detail', slug=post.slug))
    form = PostForm(obj=post)
    return render_template('posts/edit.html', post=post, form=form)




