from App.SMS_Send import SMS_Send
from App.MMS_Send import MMS_Send


from App.Controller_Configuration import Controller_Configuration
import App.Config

import os

from flask import Flask, request, render_template, url_for

import App.serial_ports

import json
from io import StringIO

import threading

import sys


def get_system_configuration_tpl():
	MMS_APN_Configurations=[x.split(";") for x in (open("Assets/apn_mms.txt", "r").read() if os.path.exists("Assets/apn_mms.txt") else "").split("\n")]

	return render_template('system_configuration.html', 
		ATInitProblem=str(App.Config.ATInitProblem), 
		SerialPorts=App.serial_ports.serial_ports(),
		MMS_APN_Configurations=MMS_APN_Configurations,
		System_Configuration=App.Config.System_Configuration
	)

app = Flask(__name__, template_folder='../Assets/Templates')
#app.logger.disabled = True



#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

#@app.route('/favicon.ico')
#def favicon():
	#return send_from_directory(os.path.join(app.root_path, 'static'), 'Assets/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
	if App.Config.ATInitProblem: return get_system_configuration_tpl()
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	return render_template('index.html', version=App.Config.Version)

@app.route('/LoadingApplicationStatus')
def LoadingApplicationStatus():
	return str(App.Config.LoadingApplication)

@app.route('/ATInitCheck')
def ATInitCheck():
	return str(App.Config.ATInitProblem)

@app.route('/system_configuration', methods = ['GET', 'POST'])
def configure_sim():
	if App.Config.ATInitProblem == False and App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	if request.method == 'POST':
		print(request.form)

		serial_port = request.form['other_serial_port'] if request.form['serial_port'] == "other" else request.form['serial_port']
		friendly_apn_name = request.form['friendly_apn_name']
		url_mms_center = request.form['url_mms_center']
		ip_mms_proxy = request.form['ip_mms_proxy']
		port_mms_proxy = request.form['port_mms_proxy']
		apn_name = request.form['apn_name']

		data = {
			"serial_port": serial_port,
			"friendly_apn_name":friendly_apn_name,
			"url_mms_center":url_mms_center,
			"ip_mms_proxy":ip_mms_proxy,
			"port_mms_proxy":port_mms_proxy,
			"apn_name":apn_name
		}

		print(data)

		d = json.dumps(data)
		f = open("Config/System_Configuration.json", "w")
		f.write(d)
		f.close()

		def reboot_os():
			os.execl(sys.executable, sys.executable, *sys.argv)

		t = threading.Timer(3.0, reboot_os)
		t.start()

		return render_template('blank.html', text=render_template('ul.html', vars=[
			["Serial Port",serial_port],
			["APN Name",friendly_apn_name],
			["APN URL",url_mms_center],
			["APN IP",ip_mms_proxy],
			["APN PORT",port_mms_proxy],
			["APN NAME",apn_name]
		]) + "<br><br><br><h1>In a few seconds the application should start again. Follow the logs in the console. Otherwise, run the program manually.</h1><script>setTimeout(function(){location.href='/';},3000)</script>")
	else:
		return get_system_configuration_tpl()


@app.route('/send_sms', methods = ['GET', 'POST'])
def send_sms():
	if App.Config.ATInitProblem: return get_system_configuration_tpl()
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	if request.method == 'POST':
		SMS_Send.add_to_queue(request.form['number'], request.form['text'])
		return render_template('blank.html', text="Your SMS has been added to the queue")
	else:
		return render_template('send_sms.html')



@app.route('/send_mms', methods = ['GET', 'POST'])
def send_mms():
	if App.Config.ATInitProblem: return get_system_configuration_tpl()
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
	if App.Config.ATInitProblem: return get_system_configuration_tpl()
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	if request.method == 'POST':
		#App.Config.Controller = Controller_Configuration()
		App.Config.Controller.SetNewData(request.form["address"], request.form["email"], request.form["password"])
		return render_template('configuration_controller.html')
	else:
		return render_template('configure_controller.html', controller_input=( "text" if App.Arguments.args.showcontroller else "hidden") )



@app.route('/main.js')
def main_js():
	#if App.Config.LoadingApplication: return render_template('LoadingApplication.html')
	return render_template('main.js')


@app.route('/set_controller_configuration')
def set_controller_configuration():
	if App.Config.ATInitProblem: return get_system_configuration_tpl()
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	return App.Config.Controller.Login()


@app.route('/get_controller_status')
def get_controller_status():
	if App.Config.ATInitProblem: return get_system_configuration_tpl()
	if App.Config.LoadingApplication: return render_template('LoadingApplication.html')

	return App.Config.Controller.UpdateStatus()


@app.route('/serial_logs')
def serial_logs():
	if App.Config.ATInitProblem: return get_system_configuration_tpl()
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
