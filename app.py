from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from net_calc import calc_dashboard


app = Flask(__name__)

app.debug = True
app.secret_key = 'super_secret_key'


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