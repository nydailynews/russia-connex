#!/usr/bin/env python
import os
import json
from flask import Flask
from flask import Markup
from datetime import date

app = Flask(__name__)
app.debug = True

page = {
    'title': '',
    'url': '',
    'description': '',
    'author': '',
    'datestamp': '',
    'keywords': '',
    'keywords_array': '',
    'shareimg': '',
    'shareimgdesc': '',
}

with app.app_context():
    app.url_root = '/'
    app.page = page
    app.sitename = ''

@app.route('/')
def index():
    app.page['title'] = ''
    app.page['description'] = ''

    response = {
        'app': app
    }
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run()
