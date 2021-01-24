from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from net_calc import calc_dashboard


app = Flask(__name__)

app.debug = True
app.secret_key = 'super_secret_key'

test_1 = [{"data":{"id":"n0","node_type":"feed","pressure":"100"},"position":{"x":100,"y":300},"group":"nodes","removed":False,"selected":False,"selectable":True,\
"locked":False,"grabbable":True,"classes":""},{"data":{"id":"n1","node_type":"cont","pressure":""},"position":{"x":300,"y":300},"group":"nodes","removed":False,\
"selected":False,"selectable":True,"locked":False,"grabbable":True,"classes":""},{"data":{"id":"n2","node_type":"feed","pressure":"50"},"position":{"x":500,"y":200},\
"group":"nodes","removed":False,"selected":False,"selectable":True,"locked":False,"grabbable":True,"classes":""},{"data":{"id":"n3","node_type":"feed","pressure":"50"},\
"position":{"x":500,"y":400},"group":"nodes","removed":False,"selected":False,"selectable":True,"locked":False,"grabbable":True,"classes":""},\
{"data":{"id":"e0","source":"n0","target":"n1","density":"32.2","length":"100","viscosity":"1","diameter":"4","roughness":"0.00015"},"position":{},"group":"edges",\
"removed":False,"selected":False,"selectable":True,"locked":False,"grabbable":True,"classes":""},{"data":{"id":"e1","source":"n1","target":"n2","density":"32.2",\
"length":"100","viscosity":"0.1","diameter":"4","roughness":"0.00015"},"position":{},"group":"edges","removed":False,"selected":False,"selectable":True,\
"locked":False,"grabbable":True,"classes":""},{"data":{"id":"e2","source":"n1","target":"n3","density":"32.2","length":"50","viscosity":"1","diameter":"4",\
"roughness":"0.00015"},"position":{},"group":"edges","removed":False,"selected":False,"selectable":True,"locked":False,"grabbable":True,"classes":""}]


@app.route('/' , methods=['GET', 'POST'])

def set_project():
	return render_template('hydra.html')

@app.route('/calc' , methods=['GET', 'POST'])

def set_calc():
	input_data = request.get_json()
	output_data = calc_dashboard.get_result(input_data)
	return jsonify(result= output_data)


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
	app.run(port= 13000)