import os
import json
import sqlite3
from flask import Flask, request, g
from .utils import json_response, JSON_MIME_TYPE
from configFileJson import configFileIni
import  create_git_repo


configFile = configFileIni()


app = Flask(__name__)


@app.before_request
def before_request():
    g.db = sqlite3.connect(app.config['DATABASE_NAME'])


# @app.route('/book')
# def book_list():
#     cursor = g.db.execute('SELECT id, author_id, title FROM book;')
#     books = [{
#         'id': row[0],
#         'author_id': row[1],
#         'title': row[2]
#     } for row in cursor.fetchall()]
#
#     return json_response(json.dumps(books))


@app.route('/book2')
def book_list():
    config = configFile.read_whole_config_file()
    for line in config.split('\n'):
        print (line)
        str='%s \n' %(line)


    print(str)



    return str, 200, {'Content-Type': JSON_MIME_TYPE}






@app.route('/book3')
def create_repo():
    configFile = configFileIni()
    get_secton_git = configFile.get_secton('Git')
    #print(get_secton_git)


    repo_ssh_link = get_secton_git[1]
    checkout_dir = get_secton_git[3]
    key_path = get_secton_git[5]



    stdout = create_git_repo.create_new_repo('True' , repo_ssh_link , checkout_dir)
    print (stdout)
    for line in stdout.split('\n'):
        print (line)
        str='%s \n' %(line)


    print(str)



    return str, 200, {'Content-Type': JSON_MIME_TYPE}






@app.route('/init_new_repo')
def init_new_repo():
    configFile = configFileIni()
    get_secton_git = configFile.get_secton('Git')
    #print(get_secton_git)
    for item in get_secton_git:
        strinnn = ('\n'.join(item))
        #print (strinnn)
        #print ('\n'.join(strinnn.split()))
        list = []
        for str in  strinnn.split(' '):
            list.append(str)
        #print (list)



        repo_ssh_link = list[1].split('=')[1]
        print ('%s repo_ssh' %(repo_ssh_link))

        checkout_dir = list[3].split('=')[1]
        print ('%s checout_dir' % (checkout_dir))
        key_path = list[5]
        print(key_path)


        stdout = create_git_repo.create_new_repo('True' , repo_ssh_link , checkout_dir)
        print (stdout)
        for line in stdout.split('\n'):
            print (line)
            str='%s \n' %(line)


        print(str)



        return str, 200, {'Content-Type': JSON_MIME_TYPE}







@app.route('/book', methods=['POST'])
def book_create():
    if request.content_type != JSON_MIME_TYPE:
        error = json.dumps({'error': 'Invalid Content Type'})
        return json_response(error, 400)

    data = request.json
    if not all([data.get('title'), data.get('author_id')]):
        error = json.dumps({'error': 'Missing field/s (title, author_id)'})
        return json_response(error, 400)

    query = ('INSERT INTO book ("author_id", "title") '
             'VALUES (:author_id, :title);')
    params = {
        'title': data['title'],
        'author_id': data['author_id']
    }
    g.db.execute(query, params)
    g.db.commit()

    return json_response(status=201)
