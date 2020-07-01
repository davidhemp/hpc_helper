import datetime

def get_department(key):
    departments = {
        "Aeronautical and Astronautical Engineeri" : "Aero and Astronautical",
        "School of Electronics & Computer Science" : "ECS",
        "School of Ocean and Earth Science" : "Ocean and Earth Science",
        "School of Mathematical Sciences" : "Mathematics",
        "School of Physics & Astronomy" : "Physics and Astro",
        "School of Chemistry" : "Chemistry",
        "Engineering Education - Central" : "Engineering Education",
        "School of Engineering" : "Engineering",
        "Human Development and Health" : "HumanDevelopmentHeal",
        "Geography & Environmental Science" : "Geography & Environm",
        "Cancer Sciences" : "Cancer Sciences",
        "School of Biological Sciences" : "Biological Sciences",
        "Faculty of Engineering & Phys Sciences" : "Physical Sciences and Engineering",
        "Faculty of Environmental & Life Sciences" : "Environmental and Life Sciences",
        "Faculty of Social Sciences" : "Social Sciences",
        "Faculty of Medicine" : "Medicine",
        "Faculty of Engineering & Phys Sciences" : "Physical Sciences and Engineering",
        'Clinical and Experimental Sciences' : 'Clinical and Experimental Sciences',
        'Economics' : 'Economics',
        "Faculty Central (FEPS)" : "FEPS",
        "iSolutions" : "iSolutions",
        "Professional Services" : "Professional Services",
        "Institute of Sound & Vibration Research" : "ISVR",
        "Zepler Inst. for Photonics & Nanoelectro" : "Zepler Institute",
        "Social Statistics & Demography" : "Social Sciences",
        "Mechanical Engineering" : "Mechanical Engineering" ,
        "Southampton Business School" : "Business",
        "Southampton Education School" : "Education",
        "Engineering Education - Aerospace Engineering" : "Aerospace Engineering",
        "Enterprise" : "Enterprise"
    }
    try:
        return departments[key]
    except KeyError:
        return key[:20]

projects_duration = {
    'iridis_request_project_duration_1_2' : str(datetime.datetime.now().year + 2),
    'iridis_request_project_duration_3_5' : str(datetime.datetime.now().year + 5),
    'iridis_request_project_duration_over_5' : str(datetime.datetime.now().year + 10)
}
