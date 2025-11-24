from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mystatement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Statement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.template_filter('currencyFormat')
def currencyFormat(value):
    value = float(value)
    return "{:,.2f}".format(value)

@app.route("/addForm")
def addForm():
    return render_template("addForm.html")

@app.route("/add", methods=["POST"])
def add():
    date = request.form["date"]
    description = request.form["description"]
    amount = request.form["amount"]
    type = request.form["type"]
    statement = Statement(date=date,description=description,amount=amount,type=type)
    db.session.add(statement)
    db.session.commit()
    return redirect("/")

@app.route("/")
def showData():
    statements = Statement.query.all()
    return render_template("statements.html", statements=statements)

@app.route("/delete/<int:id>")
def delete(id):
    statement = Statement.query.filter_by(id=id).first()
    db.session.delete(statement)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>")
def edit(id):
    statement = Statement.query.filter_by(id=id).first()
    return render_template("editForm.html", statement=statement)

@app.route("/update", methods=["POST"])
def update():
    id = request.form["id"]
    date = request.form["date"]
    description = request.form["description"]
    amount = request.form["amount"]
    type = request.form["type"]
    statement = Statement.query.filter_by(id=id).first()
    statement.date = date
    statement.description = description
    statement.amount = amount
    statement.type = type
    db.session.commit()
    return redirect("/")
    
if __name__ == "__main__":
    app.run()