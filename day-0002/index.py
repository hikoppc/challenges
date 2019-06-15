from flask import Flask,render_template,session,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import (StringField,BooleanField,DateTimeField,
                    RadioField,SelectField,TextField,
                    TextAreaField,SubmitField)
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config["SECRET_KEY"] = "mykey"

class InfoForm(FlaskForm):
    feedback = TextAreaField()
    submit = SubmitField("")

@app.route("/",methods=["GET","POST"])
def index():
    form = InfoForm()

    if form.validate_on_submit():
        words = form.feedback.data
        form.feedback.data = ex_calc(words)

        return render_template("home.html",form=form)

    return render_template("home.html",form=form)

def ex_calc(words):
    if "," in words:
        formulas = words.split(",")
    else:
        formulas = words.split("\n")

    if ";" in words:
        return "\n;;;;;;;;;;;;;;;error;;;;;;;;;;;;;;;\n" + \
                words + "\n;;;;;;;;;;;;;;;error;;;;;;;;;;;;;;;\n"

    if "=" in words:
        return "\n===============error===============\n" + \
                words + "\n===============error===============\n"

    if ":" in words:
        return "\n:::::::::::::::error:::::::::::::::\n" + \
                words + "\n:::::::::::::::error:::::::::::::::\n"

    formulas = [c.replace("\r","").replace("\n","").replace("=","").replace(" ","").replace(",","") for c in formulas]
    formulas = [c for c in formulas if len(c)>0]
    ans = [eval(c) for c in formulas]

    return "\n".join(["{0:} = {1:}".format(f,c) for f,c in zip(formulas,ans)])

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

if __name__=="__main__":
    app.run()
