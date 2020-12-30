from App.SMS_Send import SMS_Send
from App.MMS_Send import MMS_Send


from App.Controller_Configuration import Controller_Configuration
import App.Config

import os

from flask import Flask, request, render_template


app = Flask(__name__, template_folder='../Assets/Templates')

@app.route('/')
def index():
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	return render_template('index.html')

@app.route('/LoadingApplicationStatus')
def LoadingApplicationStatus():
	return str(App.Config.LoadingApplication)

@app.route('/send_sms', methods = ['GET', 'POST'])
def send_sms():
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	if request.method == 'POST':
		SMS_Send.add_to_queue(request.form['number'], request.form['text'])
		return render_template('blank.html', text="Your SMS has been added to the queue")
	else:
		return render_template('send_sms.html')



@app.route('/send_mms', methods = ['GET', 'POST'])
def send_mms():
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	if request.method == 'POST':
		#SMS_Send.add_to_queue(request.form['number'], request.form['text'])
		if request.files:
			image = request.files["image"]
			print(image)
			image.save(os.path.join("Assets/Images/Tmp", image.filename))
			MMS_Send.add_to_queue(request.form['number'], ["Tmp/" + image.filename])
		else:
			print("no image")
		return render_template('blank.html', text=request.form['number'])
	else:
		return render_template('send_mms.html')



@app.route('/configure_controller', methods = ['GET', 'POST'])
def configure_controller():
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	if request.method == 'POST':
		#App.Config.Controller = Controller_Configuration()
		App.Config.Controller.SetNewData(request.form["address"], request.form["email"], request.form["password"])
		return render_template('configuration_controller.html')
	else:
		return render_template('configure_controller.html')



@app.route('/main.js')
def main_js():
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	return render_template('main.js')


@app.route('/set_controller_configuration')
def set_controller_configuration():
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	return App.Config.Controller.Login()


@app.route('/get_controller_status')
def get_controller_status():
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	return App.Config.Controller.UpdateStatus()


@app.route('/serial_logs')
def serial_logs():
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	return render_template('serial_logs.html')

@app.route('/serial_logs_file/<sub>')
def serial_logs_file(sub):
	#if App.Config.LoadingApplication: return ""

	try:
		sub = int(sub)
		with open('Logs/Serial.txt') as f:
			data = f.read()
			l = len(data)

			if l < sub:
				sub = 0


			return str(l) + ">>>" + data[sub:l]

	except:
	  	return "0>>>[!] Read File Error...\n\r"
