from flask import Flask,render_template,request

app=Flask(__name__)


@app.route('/')
def index():

    column_size=[4]
    heading=('id','name','mail','address','age')
    rows=((1,'murshi','murshid@gmail.com','vphouse',22),(2,'shahad','shahadd@gmail.com','sphouse',23),(3,'adil','adil@gmail.com','aphouse',24))

    return render_template('view.html',column_size=column_size,heading=heading,rows=rows)

if __name__:                         
     app.run(debug=True)
