from flask import Flask, render_template, request
from redis import Redis
import json
import time
import snudown

app = Flask(__name__)

rds = Redis()

def _force_unicode(text):
    if text == None:
        return u''

    if isinstance(text, unicode):
        return text

    try:
        text = unicode(text, 'utf-8')
    except UnicodeDecodeError:
        text = unicode(text, 'latin1')
    except TypeError:
        text = unicode(text)
    return text

def _force_utf8(text):
    return str(_force_unicode(text).encode('utf8'))

@app.route("/varmidirkiacaba", methods=['POST'])
def answer():
    if len(request.form['answer']) > 5000:
        return redirect('/')
    d = dict(msg=request.form['answer'], ts=int(time.time()), username="anonim")
    rds.zadd("goygoy", json.dumps(d), time.time())
    return redirect('/')

@app.route("/")
def hello():
    messages = rds.zrevrangebyscore('goygoy', '+inf', '-inf')
    msgs = []
    for i in messages:
        msg = json.loads(i)
        msgs.append(dict(
            msg = _force_unicode(snudown.markdown(_force_utf8(msg['msg']))),
            username='anonim'
        ))
    return render_template('index.html', messages=msgs)

if __name__ == "__main__":
    app.run(debug=True)