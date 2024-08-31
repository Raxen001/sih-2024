from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
import db

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


################################################################################
# Courses
"""
the courses section
"""
@app.route("/listcourses")
@cross_origin()
def list_courses():

    offset = request.args.get("offset", default=0, type=int)
    json_data = db.get_courses(offset=offset)
    return json_data

@app.route("/course/<courseid>")
@cross_origin()
def course_details(courseid):
    json_data = db.get_course_details(courseid)
    return json_data

################################################################################
# Colleges
@app.route("/listcolleges")
@cross_origin()
def list_of_colleges():

    offset = request.args.get("offset", default=0, type=int)
    json_data = db.get_colleges(offset=offset)
    return json_data

@app.route("/college/<int:collegeid>")
@cross_origin()
def list_courses_college(collegeid):
    # print(collegeid)
    json_data = db.get_college_courses(collegeid)
    return json_data


################################################################################
# career
@app.route("/listcareers")
@cross_origin()
def list_of_careers():

    offset = request.args.get("offset", default=0, type=int)
    json_data = db.get_careers(offset=offset)
    return json_data

################################################################################
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
