from flask import Flask, request, render_template
import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer

disease_names = pickle.load(open('disease_list.pkl', 'rb'))
feature_names = pickle.load(open('feature_list.pkl', 'rb'))
model = pickle.load(open('new_model.pkl', 'rb'))

number = LabelEncoder()
number.classes_ = disease_names



def Disease_Predictor(model, inputarray):
    vtr = CountVectorizer(vocabulary = feature_names)
    test_pred = vtr.fit_transform(inputarray)
    result_ans = model.predict(test_pred.toarray())
    result_disease = number.inverse_transform([int(result_ans[0])])
    return result_disease[0]



app = Flask(__name__)

@app.route("/")
def hello():
    print('===')
    return render_template('homepage.html')

@app.route("/diagnosis")
def diagnosis():
    print('===')
    return render_template('diagnosisform.html')

@app.route("/form", methods = ["GET", "POST"])
def form():
    if request.method == "POST":
        fn = request.form.get("fname")
        ln = request.form.get("lname")
        return fn + ln
    return render_template("form.html")


@app.route("/result", methods = ["GET", "POST"])
def results():
    if request.method == "POST":
        form_data = request.form
        vals = "symp"
        symps_str = ""
        for i in range(1,18):
            d = vals + str(i)
            if len(request.form.get(d)) > 0:
                symps_str+=request.form.get(d)
                symps_str+=" "

        symps_str = symps_str.strip()
        print(symps_str)
        dis_res = Disease_Predictor(model, [symps_str])    
        return render_template("results.html", data=dis_res)
    return render_template("results.html")

if __name__ == "__main__":
    app.run()
