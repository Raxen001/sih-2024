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
            "course_duration": data[5],
            "course_details": "/course/" + str(data[6]),
        }

        json_data['results'].append(course)


    return json_data

def get_course_details(courseid):
    query = """ 
                SELECT * 
                FROM courses 
                WHERE id = %s;
            """
    query_data = (courseid, )
    cur.execute(query, query_data)
    data = cur.fetchone()
    json_data = {
        "course_name": data[0],
        "course_id": data[1],
        "course_img": data[2],
        "course_desc": data[3],
        "course_req": data[4],
        "course_duration": data[5],
        "colleges": []
    }

    query = """
                SELECT *
                FROM courseelgibility
                join college on courseelgibility.college_code = college.college_code
                join courses on courseelgibility.course_id = courses.course_id
                WHERE courses.id = %s
                ORDER BY nrif
                LIMIT %s 
                ;
            """
    limit = 3
    query_data = (courseid, limit,)
    cur.execute(query, query_data)
    datas = cur.fetchall()
    
    for data  in datas:
        college = {
            "college_name": data[11],
            "college_code": data[1],
            "college_image": data[2],
            "college_nrif": data[3],
            "college_url": data[4],
            "college_zipcode": data[5],
        }
        json_data['colleges'].append(college)
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
def get_careers(offset=0, no_of_ele=10):

    query = """
                SELECT career_name, career_desc, career_img, career_id
                FROM career
                ORDER BY career_name 
                LIMIT %s, %s;
            """

    query_data = (offset, no_of_ele, )
    cur.execute(query, query_data)

    datas = cur.fetchall()
    json_data = { "results": [] }
    for data in datas:
        career = {
            "career_name": data[0],
            "career_desc": data[1],
            "career_img": data[2],
            "career_details": "/career/" + str(data[3])
        }
        json_data['results'].append(career)
    return json_data
    
def get_career_details(careerid):
    query = """
                SELECT career_name, career_desc, career_img, career_id, career_video
                FROM career
                WHERE career_id = %s
            """

    query_data = (careerid, )
    cur.execute(query, query_data)
    data = cur.fetchone()
    json_data = {
        "career_name": data[0],
        "career_desc": data[1],
        "career_img": data[2],
        "career_id": data[3],
        "career_video": data[4],
        "courses": []
    }
    
    # courses for the career
    query = """
                SELECT courses.*
                FROM careereligibility
                JOIN career
                  ON career.career_id = careereligibility.career_id
                JOIN courses
                  ON careereligibility.course_id = courses.course_id
                WHERE careereligibility.career_id = %s;
                """
    query_data = (careerid, )
    cur.execute(query, query_data)
    datas = cur.fetchall()

    for data in datas:
        course = {
            "course_name": data[0],
            "course_id": data[1],
            "course_img": data[2],
            "course_desc": data[3],
            "course_req": data[4],
            "course_duration": data[5],
            "course_link": "/course/" + str(data[6]),
        }
        json_data['courses'].append(course)

    return json_data

###############################################################################
#mentor

def update_mentor(json_data):
    pass

###############################################################################
if __name__ == "__main__":
    # get_colleges()
    get_college_courses(2116)
    cnx.close()
