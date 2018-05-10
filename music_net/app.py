from flask import Flask, url_for, render_template,\
        request, flash, redirect, get_flashed_messages
import redis
import random


app = Flask(__name__)
app.secret_key = 'peter'
app.config['SESSION_TYPE'] = 'redis'
r = redis.Redis()

SONGS = eval(r.get('songs'))
base_url = 'http://music.163.com/song/media/outer/url?id='


@app.route('/')
def hello_world():
    return 'hello peter'


@app.route('/songs', methods=['POST', 'GET'])
def songs():
    songs_list = random.sample(SONGS, 10)
    return render_template('index.html', songs=songs_list)


@app.route('/search', methods=['POST'])
def search():
    text = request.form.get('text')
    songs_list = []
    if text:
        songs_list = [s for s in SONGS if text in s['songs_name'] or text in s['singer']]
        flash('{} results found !'.format(len(songs_list)))
        return render_template('index.html', songs=songs_list)
    else:
        flash('please input something to search !')
        return redirect(url_for('songs'))
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
