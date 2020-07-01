import pysnow

#Password and user are kept seperate.
from hpc_key import *

client = pysnow.client.Client(host='sotonproduction.service-now.com',
                              user=user, password=password)

request_resource = client.resource(api_path='/v1/table/sc_req_item')
user_resource = client.resource(api_path='/v1/table/sys_user')
department_resource = client.resource(api_path='/v1/table/cmn_department')
application_resource = client.resource(api_path='/uno49/ritm_iridis_api', base_path='/api')

application_query = pysnow.QueryBuilder().field('short_description'). \
                    contains('Iridis Account Application')


def get_application_form_variables(ritm):
    return application_resource.request(
        'GET', headers={"ritm": ritm}).one()[ritm]


def get_iridis_applications(query, get_form_variables=False):
    """Return a list of dictionaries containing data for service now
    records matching query (a pysnow.QueryBuilder object). If
    get_form_variables is True then a second API request is made for
    each matching record to populate user responses of the full
    application form. This is accessible under the 'form' key of each
    record and may differ depending on the version of the form.
    """
    response = request_resource.get(query=query, stream=True)

    records = list(response.all())
    if get_form_variables:
        for record in records:
            record['form'] = get_application_form_variables(record['number'])

    return records


def get_school(sys_id=None):
    if sys_id is None:
        raise ValueError("Missing department sys_id")
    else:
        query = {'sys_id': sys_id}
    return department_resource.get(query=query, stream=True).one()

def get_faculty(sys_id=None):
    if sys_id is None:
        raise ValueError("Missing Faculty sys_id")
    else:
        query = {'sys_id': sys_id}
    return department_resource.get(query=query, stream=True).one()

def get_user_record(user_name=None, sys_id=None):
    if user_name is None and sys_id is None:
        raise ValueError('Must provide either user_name or sys_id')

    if user_name is not None:
        query = {'user_name': user_name}
    else:
        query = {'sys_id': sys_id}

    return user_resource.get(query=query, stream=True).one()



def sc_lookup(value, item="sys_id", ticket_type="user"):
    """Get requested item from service now. Used to find a single
        item. Can look for an incident, user or request. A more
        flexible interface for getting records.

        Input:
            value - string
                What service now should be looking for.
            item - string
                What parameter it should look against, e.g ticket id
            ticket_type -
                One of the following "request", "user", "incident"
                or "department"
        Return:
            Dictionary

    """
    tables = {"request": "/table/sc_req_item",
              "user": "/table/sys_user",
              "incident": "/table/incident",
              "department": "/table/cmn_department"}
    table = client.resource(api_path=tables[ticket_type])
    data = table.get(query={item: value})
    return data.one()



### Some basic tests below

# record = get_iridis_application('RITM0166238', get_form_variables=True)

# import datetime
# today = datetime.datetime.today()
# lower_limit = today - datetime.timedelta(days=7)
# query = application_query.AND().field('sys_created_on'). \
#         between(lower_limit, today)
# records = get_iridis_applications(query, get_form_variables=True)

# user = get_user_record('cica1d14')
# user = get_user_record(sys_id='33c1365d6fc1fd0004c9ff554b3ee45a')
