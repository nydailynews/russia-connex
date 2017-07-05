#!/usr/bin/env python
import os
import json
from flask import Flask
from flask import Markup
from flask import g, render_template, url_for, redirect, abort, request
from datetime import date, timedelta, datetime
#from misaka import Markdown, HtmlRenderer
import misaka as m


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

    content = { 'story': '', 'sections': [] }
    #rndr = HtmlRenderer()
    #md = Markdown(rndr)
    fh = open('story.md', 'rb')
    story = fh.read().split('^^^^^^')
    content['intro'] = m.html(story[0])
    
    for section in story[1:]:
        items = []
        parts = section.split("\n\n")
        for item in parts:
            items.append(m.html(item))
        markup = '</li><li>\n'.join(items)
        
        # Add the hr's
        markup = markup.replace('</h3>', '</h3>\n<hr>')
        # Add the opening ul
        markup = markup.replace('</h2>', '</h2>\n<ul><li>')

        content['sections'].append('%s\n</ul>' % markup)

    response = {
        'app': app,
        'content': content
    }
    return render_template('index.html', response=response)

@app.template_filter(name='next_update')
def next_update(blank, value, delta=0):
    """ When is this / the next Tuesday, Wednesday, Thursday, Friday or Saturday?
        Returns a formatted date object, ala "Friday Feb. 20"
        Legit values for var value: "this" and "next"
        """
    today = date.today() + timedelta(delta)
    i = 1
    if value == 'this':
        i = 0
    while i < 7:
        new_day = today + timedelta(i)
        wd = new_day.weekday()
        if wd in [0, 1,2,3,4,5]:
            return new_day.strftime('%A %b. %d')
        i += 1
    pass

@app.template_filter(name='timestamp')
def timestamp(blank):
    """ What's the current date and time?
        """
    today = datetime.today()
    return today.strftime("%A %b. %d, %-I:%M %p")

if __name__ == '__main__':
    app.run()
