import os
import logging
from datetime import date as DATE
import weapon_db as db
from itertools import islice
from camera import VideoCamera
from flask import Flask, render_template, jsonify, request, Response
import logs

log = logs.createLogs("logs/weapon_api.log")

app = Flask(__name__)

def getErrorMsg(err_code, err_msg, err_type):
	error_msg = {
					"error": {
						"message": err_msg, 
				 		"type": err_type,
				 		"code": err_code
				 	}
	}
	return error_msg

def chunk(list_itr, size):
	list_itr = iter(list_itr)
	return list(iter(lambda: list(islice(list_itr, size)), []))

@app.route("/")
def index():
	log.info("inside INDEX route")
	return render_template("home.html")

@app.route("/api")
def api():
	log.info("inside API route")

	preview = request.args.get("preview")
	date = request.args.get("date")
	label = request.args.get("label")
	page = request.args.get("page")

	if preview == None or preview == "":	
		log.info("set PREVIEW parameter as default")
		preview = "False"

	if date == None or date == "":
		log.info("set DATE parameter as default")
		date = str(DATE.today())

	if label == None or label == "":
		log.info("set LABEL parameter as default")
		label = "pistols"

	if page == None or page == "":
		log.info("set PAGE parameter as default")
		page = 0

	page = int(page)

	preview = str(preview).capitalize()

	path = os.path.join("static", "predictions", date, label)

	chunk_size = 10
	try:
		list_images = os.listdir(path)
	except:
		return getErrorMsg(404, "Directory not found!", "directory")

	image_list = chunk(list_images, chunk_size)
	dict_list = []

	for chunks in image_list:
		dict_list.append({"images": chunks})

	if preview == "True":
		try:
			return render_template("gallery.html", photos=image_list[page], date=date, label=label.upper())
		except:
			if page == 0:
				return getErrorMsg(404, "No data found", "Data")
			else:
				return getErrorMsg(404, "Page Number not found!", "Page Number")

	else:
		if (page+1) == len(dict_list):
			try:
				log.warning("last page")
				return jsonify({"meta": {
										"label": label,
										"total_pages": len(dict_list),
										"page_no": page,
										"result_per_page": chunk_size,
										"images_found": len(dict_list[page]["images"])
										},
								"data": dict_list[page]})
			except:
				if page == 0:
					return getErrorMsg(404, "No data found", "Data")
				else:
					return getErrorMsg(404, "Page Number not found!", "Page Number")
		else:
			try:
				return jsonify({"meta": {
										"label": label,
										"total_pages": len(dict_list),
										"page_no": page,
										"next_page": page+1,
										"result_per_page": chunk_size,
										"images_found": len(dict_list[page]["images"])
										},
								"data": dict_list[page]})
			except:
				if page == 0:
					return getErrorMsg(404, "No data found", "Data")
				else:
					return getErrorMsg(404, "Page Number not found!", "Page Number")

@app.route("/predictions")
def predictions():
	date = request.args.get("date")
	if date != None and date != "":
		meta, pistols, not_pistols =  get_stats(date)
		return jsonify({"meta": meta,
						"pistols": pistols,
						"not-pistols": not_pistols
						})
	else:
		dates = get_all_dates()
		return dates

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b"--frame\r\n" b"Content-Type: image/png\r\n\r\n" + frame + b"\r\n\r\n")


@app.route("/video")
def video():
	log.info("getting predicted video")

	return Response(gen(VideoCamera()), mimetype="multipart/x-mixed-replace; boundary=frame")

def get_all_dates():
	log.info("getting all date folders")

	path = os.path.join("static", "predictions")

	dates = "<center><h1 style='font-family: arial;'>AI Weapon Detection API</h1></center> <center>"

	for date_folder in os.listdir(path):
		dates = dates + "<a style='border: 1px solid #e0e0e0; border-radius: 20px; font-family: arial; color: #000; text-decoration: none; background-color: #fff; padding: 10px;' href='predictions?date="+date_folder+"'>"+date_folder+"</a>   "

	dates = dates + "</center>"
	return dates

def get_stats(date):
	log.info("getting stats")

	pistol_path = os.path.join("static", "predictions", date, "pistols")
	not_pistol_path = os.path.join("static", "predictions", date, "not-pistols")

	log_pistols = os.listdir(pistol_path)
	log_not_pistols = os.listdir(not_pistol_path)

	meta = {"date": date,
			"pistols": len(log_pistols),
			"not-pistols": len(log_not_pistols)
	}

	pistols = {}
	not_pistols = {}

	for i, pistol in enumerate(log_pistols):
		pistols.update({i: pistol})

	for i, not_pistol in enumerate(log_not_pistols):
		not_pistols.update({i: not_pistol})

	log.info("PISTOLS: "+ str(len(log_pistols)))
	log.info("NOT-PISTOLS: "+ str(len(log_not_pistols)))

	return meta, pistols, not_pistols

if __name__ == "__main__":
	app.run(debug=True)