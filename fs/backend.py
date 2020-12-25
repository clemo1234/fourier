#%%
from flask import Flask,render_template, url_for,request
import socket
import parser
from math import sin, cos
from sympy import*
import numpy as np
init_printing()

t211 = str()
con = pi/180

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("FS.html")

@app.route('/', methods=['POST'])
def my_form_post():
    global eq
    eq = request.form['form']
    val2 = request.form['period']
    val=int(val2)
    if val < 1:
        render_template("FS.html", Error="Error: Cannot compute val < 1")
        val = abs(val) + 1
    #Define symbols
    x = Symbol("x")
    k = Symbol("k")
    T = Symbol("T")
    #Retrieve user input
    #code = input("Calculate >> ")
    #code2 = parser.expr(test).compile()

    #First coefficient
    code = eq
    an_0 = "(2/T)*cos((2*pi*k*x)/(T))"
    an = "integrate("+an_0+"*"+code+",(x,0,T),conds='none')"
    print(an)
    result = eval(an)
    a = result.subs(T,val)
    #Second coefficient
    bn_0 = "(2/T)*sin((2*pi*k*x)/(T))"
    bn = "integrate("+bn_0+"*"+code+",(x,0,T),conds='none')"
    print(bn)
    result2 = eval(bn)
    b = result2.subs(T,val)
    #Average amplitude
    a_0 = "integrate((2/T)*"+code+",(x,0,T),conds='none')"
    result3 = eval(a_0)
    ar = result3.subs(T,val)
    expr1 = sin((2*pi*k*x)/val)
    s2 = Mul(expr1,b)
    expr2 = cos((2*pi*k*x)/val)
    s1 = Mul(expr2,a)
    test1 = Sum(s1,(k,1,150)).doit()
    test2 = Sum(s2,(k,1,150)).doit()
    test3 = (ar/2) + test1 + test2 
    t21 = ar/2 +s1 +s2
    t211 = latex(t21)
    #print("test ", test3)

    p1 = plot(test3, show=True, ylim=(-2,2))
    print("inte a: ", a)
    print(b)
    print(ar)
    print("res ", s2)
    return render_template("FS.html", content=t211)

if __name__ == '__main__':
    app.run()
# %%
