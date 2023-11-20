from flask import render_template
from app import app


@app.get('/test/')
def test():
    return render_template('base.html')
