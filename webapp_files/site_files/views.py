from flask import render_template
from flask import request
from site_files import app
from site_files.model import Model 


@app.route('/')
@app.route('/index')
@app.route('/input')
def input():
    return render_template("input.html")

@app.route('/output')
def output():
    interest1 = request.args.get('interest1')
    interest2 = request.args.get('interest2')
    interest3 = request.args.get('interest3')
    zone = request.args.get('zone')
       
    hob0, hob1, hob2, hob3, hob4, events0, events1, events2, events3, events4\
    = Model(interest1, interest2, interest3, zone)
    return render_template("output.html", interest1=interest1, interest2=interest2, 
                           interest3=interest3, hob0=hob0, hob1=hob1, hob2=hob2, hob3=hob3, hob4=hob4,
                           event0=events0, event1=events1, event2=events2, 
                           event3=events3, event4=events4, zone=zone
                           )

@app.route('/demo')
def demo():
    return render_template("demo.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.errorhandler(KeyError)
def error(e):
    return render_template("error.html")