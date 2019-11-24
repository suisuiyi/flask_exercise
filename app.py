# -*- coding: utf-8 -*-

"""
@author: peter.dai
@project: flask_exercise
@file: app.py.py
@time: 2019/11/24 11:10
@desc:
"""

# HTTP 进阶实战，重定向回到上一个页面。


# url安全验证
from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for, Flask
from jinja2.utils import generate_lorem_ipsum
from jinja2 import escape

app = Flask(__name__)

# AJAX请求
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data) {
                $('.body').append(data);
            }
        })

    })

})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)

@app.route('/foo')
def foo():
    return '<h1> Foo page </h1> <a href="%s">Do something </a>' % url_for('do_something')


@app.route('/bar')
def bar():
    return '<h1> Bar page </h1> <a href="%s">Do something </a>' % url_for('do_something')


@app.route('/do_something')
def do_something():
    # do something
    return redirect(url_for('hello'))


@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')
    response = '<h1>Hello, %s! </h1>' % escape(name)
    return response


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue

        if is_safe_url(target):
            return redirect(target)

    return redirect(url_for(default, **kwargs))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


if __name__ == '__main__':
    app.run(debug=True)



