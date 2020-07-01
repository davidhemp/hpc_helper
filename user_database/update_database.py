
from datetime import datetime, timedelta
from requests import HTTPError
import mysql.connector

import soton_snow
from database_hashtables import get_department, projects_duration
import database_key

def format_row_data(user, supervisor, school, faculty):
    if user["u_type"] == "alumni" or user["u_type"] == "PGR":
        user["u_type"] = "Phd"
    row = (user["user_name"], "1", record["sys_created_on"].split(" ")[0], record["number"], \
            user["last_name"], user["first_name"], user["email"], user["u_type"], \
            " ".join([supervisor["title"], supervisor["first_name"], supervisor["last_name"]]), \
            supervisor["email"], supervisor["user_name"], "", get_department(school["name"]), \
            get_department(faculty["name"]), \
            record["form"]["iridis_funding_organisations"].replace("iridis_request_", ""), "", \
            record["form"]["iridis_research_area"].replace("research_area_", ""), "", \
            projects_duration[record["form"]["iridis_project_duration"]], \
            record["form"]["iridis_application_user_experience"].replace("experience_",""), \
            "", "", record["form"]["iridis_filestore_ownership"][0].lower(), \
            record["form"]["iridis_form_processing"][0].lower(), \
            "", "", record["form"]["iridis_project_title"], \
            record["form"]["iridis_project_outline"][:1000])
    return row

upper_limit = datetime.today()
lower_limit = upper_limit - timedelta(days=40)

# query for successful applications (state=3, closed complete)
# within the required time frame
query = soton_snow.application_query.AND(). \
        field("sys_updated_on").between(lower_limit, upper_limit).AND(). \
        field("state").equals("3")

columns = "`" + "`, `".join(["username","active","appl_date","ServiceNow", "surname","first_name", \
    "email","title","pi_name", "pi_email","pi_account","unix_group","school", \
    "faculty","funding","funding2","domain","domain2", "duration","linux_level", \
    "software","job_type", "filestore_yes","contact_yes","comments","web_page", \
    "proj_title","proj_descr"]) + "`"

records = soton_snow.get_iridis_applications(query, get_form_variables=True)
values = []
titles = []
for record in records:
    user = soton_snow.get_user_record(sys_id=record["u_owner"]["value"])
    try:
        supervisor = {"title": "Unknown", "first_name" : "Unknown", "last_name" : "Unknown", \
                        "email" : "Unknown", "user_name" : "Unknown"}
        supervisor = soton_snow.get_user_record(sys_id=record["form"]["iridis_supervisor_grant_holder"])
    except HTTPError:
        if type(user["manager"]) != str:
            try:
                supervisor = soton_snow.get_user_record(sys_id=user["manager"]["value"])
            except HTTPError:
                print("Failed to find supervisor for user: ".format(user["user_name"]))
                pass
    school = soton_snow.get_school(sys_id=user["department"]["value"])
    faculty = soton_snow.get_faculty(sys_id=school["u_faculty"]["value"])
    values.append(format_row_data(user, supervisor, school, faculty))
    titles.append(user["u_type"])

connection = mysql.connector.connect(host="mysql431.soton.ac.uk", \
                                    port=3306, \
                                    database="IridisUsers", \
                                    user=database_key.user, \
                                    password=database_key.password, \
                                    use_pure=True, charset='utf8')

if not connection.is_connected():
    raise exception("Failed to connect to mysql431.soton.ac.uk")

if len(values) > 0:
    query = "INSERT IGNORE INTO applicationsdev({}) VALUES(".format(columns) + "%s,"*27 +"%s)"
    cursor = connection.cursor()
    cursor.executemany(query, values)
    connection.commit()
connection.close()
