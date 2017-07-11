#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from flask import Flask
from flask import Markup
from flask import g, render_template, url_for, redirect, abort, request
from datetime import date, datetime
import misaka as m


app = Flask(__name__)
app.debug = True

page = {
    'title': '',
    'title_twitter': 'Donald Trump’s ties to Russia: Your at-a-glance guide to who’s who.'.decode('utf-8'),
    'url': '',
    'description': '',
    'author': '"Jason Silverstein", "Interactive Project"',
    'datestamp': '',
    'keywords': '',
    'keywords_array': '"Donald Trump", "russia", "donald trump jr"',
    'shareimg': '',
    'shareimgdesc': '',
}

with app.app_context():
    app.url_root = '/'
    app.page = page
    app.sitename = ''

@app.route('/')
def index():
    app.page['title'] = 'Donald Trump’s ties to Russia: A who’s who of the key players'.decode('utf-8')
    app.page['description'] = 'The investigation into President Trump’s ties to Russia is extremely complicated, with new revelations every day. Here’s your at-a-glance guide to who’s who and how the key players are connected. By NY Daily News reporter Jason Silverstein'.decode('utf-8')
    app.page['keywords'] = 'Donald Trump Russia investigation, Trump’s Russia connections, Trump associates, Putin and Trump, Donald Trump Jr., Jared Kushner'.decode('utf-8')

    content = { 'intro': '', 'sections': [] }
    fh = open('story.md', 'rb')
    
    story = fh.read().split('^^^^^^')
    content['intro'] = m.html(story[0])
    i = 0
    for section in story[1:]:
        items = []
        parts = section.split("\n\n")
        for item in parts:
            mkup = m.html(item)
            mkup = mkup.replace('</h4>', '</h4>\n<div id="read-more-%d" class="read-more collapsed" onclick="clicker(%d);">' % (i, i))
            items.append(mkup)
            i += 1

        markup = '</div>\n</li>\n\n<li>\n'.join(items)
        
        # Add the hr's
        markup = markup.replace('<h3>', '<hr>\n<h3>')
        # Add the opening ul
        markup = markup.replace('</h2>', '</h2>\n<ul><li>')
        # Add the closing ul
        content['sections'].append('%s\n</div>\n</li>\n</ul>' % markup)

    response = {
        'app': app,
        'content': content
    }
    return render_template('index.html', response=response)

@app.template_filter(name='last_update')
def last_update(blank):
    """ Returns the current date. That means every time the project is deployed,
        the datestamp will update.
        Returns a formatted date object, ala "Friday Feb. 20"
        """
    today = date.today()
    return today.strftime('%A %B %d')

@app.template_filter(name='timestamp')
def timestamp(blank):
    """ What's the current date and time?
        """
    today = datetime.today()
    return today.strftime("%A %B %d, %-I:%M %p")

@app.template_filter(name='ordinal')
def ordinal_filter(value):
    """ Take a number such as 62 and return 62nd. 63, 63rd etc.
        """
    digit = value % 10
    if 10 < value < 20:
        o = 'th'
    elif digit is 1:
        o = 'st'
    elif digit is 2:
        o = 'nd'
    elif digit is 3:
        o = 'rd'
    else:
        o = 'th'
    return '%d%s' % (value, o)
app.add_template_filter(ordinal_filter)

if __name__ == '__main__':
    app.run()
