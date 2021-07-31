from flask import Flask, render_template, request, redirect
from scrapper import scrap_hospital

app = Flask("hospitialScrapper")

db = {} # 같은 거 입력했을 땐 두번 크롤링 하지 않게 여기에 저장

@app.route("/") # homepage
def home():
    return render_template('home.html')

@app.route("/report") # resultpage
def report():
    location = request.args.get('location') # homepage에서 location 정보 가져오기
    word = request.args.get('word') # homepage에서 word 정보 가져오기
    inf = scrap_hospital(location, word)
    return render_template("report.html", searchingBy=word, inf =inf)              

app.run(host="0.0.0.0")



