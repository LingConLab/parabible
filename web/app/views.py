from app import app
from flask import render_template, request
import os

PATH_TO_CORPORA = "parser/bible_json"
corpora_texts = [x for x in os.listdir(PATH_TO_CORPORA)]


@app.route('/')
@app.route('/home')
def index():
    return render_template("home.html")

@app.route('/library', methods=['post', 'get'])
def library():
    if request.method == 'POST':
        texts = request.form.get('text_choose')
        print(texts)
    return render_template("library.html", book_list={"Bible": corpora_texts})