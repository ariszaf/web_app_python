#!/usr/bin/env python

import settings
import web
import sys
sys.path.insert(0, './lib')
import pymysql
from bottle import run, get, post, request

conn = pymysql.connect(host=settings.mysql_host,
                       port=settings.mysql_port,
                       user=settings.mysql_user,
                       passwd=settings.mysql_passwd,
                       db=settings.mysql_schema)

cur = conn.cursor()
cur.execute("set names 'utf8'")


@get('/')
def home():
    return web.template_home()                  # klisi sinartisis pou eksasfalizei ta button tis arxikis selidas


@post('/search_artists')
def search_artists():
    return web.template_search_artists()        # klisi sinartisis pou eksasfalizei tin prwti forma Presentation of Artists


@post('/view')
def view():
    name = request.forms.get('name')            # me ta parakatw request eksasfalizoume ta pedia pou tha simplirwsei o xristis stin forma na apothikeutoun sis metavlites
    surname = request.forms.get('surname')
    dfrom = request.forms.get('dfrom')
    dto = request.forms.get('dto')
    type = request.forms.get('type')

    if dfrom == "":                             # ta dyo /if/ eksasfalizoun tin ektelesi tis formas akoma kai stin periptwsi pou o xristis den simplirwsei imerominies
        dfrom = "1900"
    if dto == "":
        dto = "2000"

    # oi parakatw sinthikes if/elif/else ekteloun ena erwtima analoga me to type tou kalitexni eite ena geniko erwtima gia olous tous kalitexnes se periptwsi pou o den epileksei kapoio type o xristis
    if type == "0":
        cur.execute("SELECT distinct ar_taut, onoma, epitheto, etos_gen FROM kalitexnis join singer_prod on ar_taut = tragoudistis where etos_gen BETWEEN %s and %s and onoma LIKE %s AND epitheto LIKE %s", (dfrom, dto, name+'%', surname+'%'))
    elif type == "1":
        cur.execute("SELECT distinct ar_taut, onoma, epitheto, etos_gen FROM kalitexnis join tragoudi on ar_taut = stixourgos where etos_gen BETWEEN %s and %s and onoma LIKE %s AND epitheto LIKE %s", (dfrom, dto, name+'%', surname+'%'))
    elif type == "2":
        cur.execute("SELECT distinct ar_taut, onoma, epitheto, etos_gen FROM kalitexnis join tragoudi on ar_taut = sinthetis where etos_gen BETWEEN %s and %s and onoma LIKE %s AND epitheto LIKE %s", (dfrom, dto, name+'%', surname+'%'))
    else:
        cur.execute("SELECT distinct ar_taut, onoma, epitheto, etos_gen FROM kalitexnis where etos_gen BETWEEN %s and %s and onoma LIKE %s AND epitheto LIKE %s", (dfrom, dto, name+'%', surname+'%'))

    rows = cur.fetchall()

    List = [("National ID", "Name", "Surmame", "Birth Year", "Edit?")]

    for i in rows:
        List.append(i)

    return web.template_view(List)


@post('/update')
def update():
    name = request.forms.get('name')
    surname = request.forms.get('surname')
    year = request.forms.get('year')

    return web.template_update(name, surname, year)


@post('/do_update')
def do_update():
    name = request.forms.get('name')
    surname = request.forms.get('surname')
    year = request.forms.get('year')
    national_id = request.forms.get('ar_taut')

    cur.execute("UPDATE kalitexnis SET onoma = %s, epitheto = %s, etos_gen = %s WHERE ar_taut = %s", (name, surname, year, national_id))
    conn.commit()

    return "<p>Updated successfully </p>"


@post('/search_songs')
def search_songs():
    return web.template_search_songs()


@post('/songs_results')
def do_search_songs():
    stitle = request.forms.get('stitle')
    pyear = request.forms.get('pyear')
    company = request.forms.get('company')

    cur.execute("SELECT title, etos,etaireia from cd_production join singer_prod on code_cd=cd where title LIKE %s and etos LIKE %s and etaireia LIKE %s", (stitle + '%', pyear + '%', company + '%'))

    rows = cur.fetchall()

    List = [("Song Title", "Production year", "Company")]

    for i in rows:
        List.append(i)

    return web.template_do_search_songs(List)


@post('/insert_artist')
def insert_artist():
    return web.template_insert_artist()


@post('/view_insert_artist')
def do_insert_artist():
    national_id = request.forms.get('national_id')
    name = request.forms.get('name')
    surname = request.forms.get('surname')
    byear = request.forms.get('byear')

    try:
        cur.execute("INSERT into kalitexnis Values (%s, %s, %s, %s)", (national_id, name, surname, byear))
        conn.commit()
        return "<p> The artist inserted successfully</p> "
    except pymysql.Error:
        conn.rollback()
        return "<p> The artist is already placed in the database</p>"


@post('/insert_song')
def insert_song():
    return web.template_insert_song()


@post('/view_insert_song')
def view_insert_song():
    title = request.forms.get('title')
    Pro_year = request.forms.get('Pro_year')
    cd = request.forms.get('cd')
    singer = request.forms.get('singer')
    composer = request.forms.get('composer')
    songwriter = request.forms.get('songwriter')

    try:
        cur.execute("INSERT into tragoudi Values (%s, %s, %s, %s)", (title, composer, Pro_year, songwriter))
        conn.commit()
        cur.execute("INSERT into singer_prod Values (%s, %s, %s)", (cd, singer, title))
        conn.commit()
        return "<p> The song inserted successfully</p> "
    except pymysql.Error:
        conn.rollback()
        return "<p> something goes wrong </p>"

run(host='localhost', port=settings.web_port)
cur.close()
conn.close()
