from flask import Flask,render_template,session,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import (StringField,BooleanField,DateTimeField,
                    RadioField,SelectField,TextField,
                    TextAreaField,SubmitField)
from wtforms.validators import DataRequired
import re

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

    if ":" in words:
        return "\n:::::::::::::::error:::::::::::::::\n" + \
                words + "\n:::::::::::::::error:::::::::::::::\n"

    if "import" in words or "read" in words or "write" in words or \
            "ssh" in words or "ssh" in words or "ftp" in words or \
            "sftp" in words or "exec" in words or "eval" in words:
        return "\nspellspellspellerrorspellspellspell\n" + \
                words + "\nspellspellspellerrorspellspellspell\n"

    formulas = [c.replace("\r","").replace("\n","").replace(" ","").replace(",","") for c in formulas]
    formulas = [c for c in formulas if len(c)>0]

    pre,post  = [c for c in formulas if "=" in c],[c for c in formulas if not "=" in c]

    useVariables = [c.split("=")[0] for c in pre]
    tmpVariables = ["tmpv{0}".format(i) for i in range(len(formulas))]
    tmpVariables = [c for c in tmpVariables if not c in useVariables][:len(post)]

    tmpv = {}
    exec(";".join(pre + ["{0}={1}".format(t,c) for c,t in zip(post,tmpVariables)]),{},tmpv)

    ans = [tmpv[t] for t in tmpVariables]

    pre  = ["{0} = {1}".format(*c.split("=")) for c in pre]
    post = ["{0} = {1}".format(c,t) for c,t in zip(post,ans)]

    return "\n".join(pre+post)

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

if __name__=="__main__":
    app.run()
