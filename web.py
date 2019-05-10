#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import codecs

def template_home():

    path = "./web/index.html"
    buffer = open(path, 'r').read()
    return buffer


def template_search_artists():

    path = "./web/search_artists.html"
    buffer = open(path, 'r').read()
    return buffer


def template_view(List):
    printResult = """<style type='text/css'>  </style> <table border = '1' frame = 'above'>"""

    header = '<tr><th>' + '</th><th>'.join([str(x) for x in List[0]]) + '</th></tr>'
    data = '<tr>' + '</tr><tr>'.join(['<td>' + '</td><td>'.join([str(y) for y in row]) + '</td>' + '<td><form action="/update" method="post"> <input value="Edit me" input type = "submit" ></form></td>' for row in List[1:]]) + '</tr>'
    printResult += header + data + '</table>'

    return '<h2>View Artist Results</h2>' + '<hr>' + printResult + '<hr>'


def template_update(name, surname, year):
    html = "<html><head><title>Update</title></head><body><h2>Update Artist Information</h2><hr>" \
           "<form action='/do_update' method='post'>" \
           "Name: <input name='name' type='text' value='" + (name if name is not None else '') + "' />" \
            "<br>Surname: <input name='surname' type='text' value='" + (surname if surname is not None else '') + "' />" \
            "<br>Birth Year: <input name='year' type='year' value='" + (year if year is not None else '') + "' /><br>" \
            "<input value='Update information' type='submit' />" \
            "</form><hr></body></html>"
    return html


def template_search_songs():
    path = "./web/search_songs.html"
    buffer = open(path, 'r').read()
    return buffer


def template_do_search_songs(List):
    printResult = """<style type='text/css'>  </style> <table border = '1' frame = 'above'>"""

    header = '<tr><th>' + '</th><th>'.join([str(x) for x in List[0]]) + '</th></tr>'
    data = '<tr>' + '</tr><tr>'.join(['<td>' + '</td><td>'.join([str(y) for y in row]) + '</td>' for row in List[1:]]) + '</tr>'

    printResult += header + data + '</table>'

    return '<h2>View songs Results</h2>' + '<hr>' + printResult + '<hr>'


def template_insert_artist():

    path = "./web/insert_artist.html"
    buffer = open(path, 'rU').read()
    return buffer

def template_insert_song():
    path = "./web/insert_songs.html"
    f = codecs.open(path, 'r', encoding='utf8')
    buffer = f.read()
    return buffer
