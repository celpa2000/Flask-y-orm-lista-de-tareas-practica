from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarea.db'

db = SQLAlchemy(app)

class Tarea(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    contenido = db.Column(db.String(100)) 
    hecho = db.Column(db.Boolean)

@app.route('/')
def home():
    tareas = Tarea.query.all()
    return render_template('index.html',tareas=tareas)


@app.route('/crear-tarea',methods=['POST'])
def crear_tarea():
    tarea = Tarea(contenido=request.form['content'],hecho=False)
    db.session.add(tarea)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/realizada/<int:id>")
def realizada(id):
    tarea = Tarea.query.filter_by(id=id).first()
    tarea.hecho = not(tarea.hecho)
    db.session.commit()
    return redirect(url_for("home"))
@app.route("/eliminar/<int:id>")
def eliminar(id):
    tarea = Tarea.query.filter_by(id=id).delete() 
    db.session.commit()
    return redirect(url_for("home")) 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
