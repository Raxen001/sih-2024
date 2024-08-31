import mysql.connector
from pprint import pprint

cnx = mysql.connector.connect(user='root', password='my-secret-pw',
                              host='127.0.0.1',
                              database='mydatabase')
cur = cnx.cursor()

###############################################################################
# courses
def get_courses(offset=0, no_of_ele=10):
    query = """ SELECT * 
                FROM courses 
                ORDER BY course_id 
                LIMIT %s, %s;
            """
    data = (offset, no_of_ele, )
    cur.execute(query, data)
    datas = cur.fetchall()
    json_data = { "results" : [] }
    for data in datas:
        course = {
            "course_name": data[0],
            "course_id": data[1],
            "course_img": data[2],
            "course_desc": data[3],
            "course_req": data[4],
            "course_duration": data[5]
        }

        json_data['results'].append(course)


    return json_data


###############################################################################
# colleges
"""
from this point all the college query db whatever idc
"""
def get_colleges(offset=0, no_of_ele=10):
    query = """ SELECT * 
                FROM college 
                ORDER BY nrif 
                LIMIT %s,%s;
            """
    data = (offset, no_of_ele, )
    cur.execute(query, data)
    datas = cur.fetchall()

    json_data = { 'results' : [] }
    for data in datas:
        college = {
            "name": data[0],
            "nrif": data[1],
            "url": data[2],
            "image": data[3],
            "zipcode": data[4],
            "coursesn_link": "/college/"+ str(data[5]),
        }
        json_data['results'].append(college)

    return json_data

def get_college_name(college_id):
    query = """
                SELECT college_name
                FROM college
                WHERE college_code = %s
            """
    data = (college_id,)
    cur.execute(query, data)
    data = cur.fetchone()
    return data


def get_college_courses(college_id):
    query = """
                SELECT courses.course_name, courses.course_id, courses.course_desc, courses.req, courseelgibility.cutoff, college.college_name, courses.course_image
                FROM college
                JOIN courseelgibility ON courseelgibility.college_code = college.college_code
                JOIN courses ON courses.course_id = courseelgibility.course_id
                WHERE college.college_code = %s
            """
    data = (college_id,)
    cur.execute(query, data)
    datas = cur.fetchall()
    json_data = { "college_name": get_college_name(college_id),
                 'results' : [] }
    for data in datas:
        college = {
            "course_name": data[0],
            "course_id": data[1],
            "course_desc": data[2],
            "course_requirements": data[3],
            "cutoff": data[4],
            "course_img": data[6],
        }
        json_data['results'].append(college)
    return json_data

###############################################################################
# career

###############################################################################
if __name__ == "__main__":
    # get_colleges()
    get_college_courses(2116)
    cnx.close()
