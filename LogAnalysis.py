import re
import csv
import codecs
from flask_cors import CORS
from flask import Flask,render_template,request,jsonify

app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

fail_list = []
select_list = []
all_list = []
test_list = []
log_map = {}

def analyse_csv(csv_file):
    fail_list.clear()
    select_list.clear()
    all_list.clear()
    test_list.clear()
    reader = csv.DictReader(codecs.iterdecode(csv_file,"utf-8"))
    for item in reader:
        Dict = {}
        Dict['Year'] = 2019
        Dict['Month'] = item['month']
        Dict['Day'] = item['day']
        Dict['Hour'] = item['hour']
        Dict['Minute'] = item['minute']
        Dict['Second'] = item['second']
        all_list.append(Dict)
        test_list.append("2019-{}-{} {}:{}:{}.{}".format(item['month'],item['day'],item['hour'],item['minute'],item['second'],item['microsec']))
        if item['result'] == 'Fail':
            select_list.append(Dict)
            fail_list.append("2019-{}-{} {}:{}:{}.{}".format(item['month'],item['day'],item['hour'],item['minute'],item['second'],item['microsec']))
    return jsonify({
        "code":1,
        "fail":fail_list,
        "select":select_list,
        "all":all_list,
        "test":test_list
    })

def analyse_log(log_file):
    log_map.clear()
    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d+'
    log = codecs.iterdecode(log_file, "utf-8")
    item = ""
    for line in log:
        m = re.match(pattern, line)
        if m:
            item += line
            log_map[m.group()] = item
            item = ""
        else:
            item += line
@app.route('/card')
def card():
    return render_template("card1.html")


@app.route('/',methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        csv_file = request.files.get("csv")
        #log_file = request.files.get("log")
        if csv_file.filename.endswith("csv"): #and log_file.filename.endswith("log"):
            #analyse_log(log_file)
            return analyse_csv(csv_file)
        return jsonify({
            "code": 0,
            "fail":[],
            "select":[],
            "all":[],
            "test":[]
    })

if __name__ == '__main__':
    app.run(debug=True)
