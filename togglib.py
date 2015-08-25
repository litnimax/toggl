import requests
import logging
import sys
import json
from datetime import date, timedelta
import re

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

re_date = re.compile('.+T([0-9]{2}:[0-9]{2}:[0-9]{2})\+.+')

api_token = '826a097c44ca2f00991c878c2500ef07'

WORKSPACE = '862594'
WORKSPACE_USERS = 'https://www.toggl.com/api/v8/workspaces/%s/users' % WORKSPACE
DASHBOARD = 'https://www.toggl.com/api/v8/dashboard/%s' % WORKSPACE
PROJECTS = 'https://www.toggl.com/api/v8/workspaces/%s/projects' % WORKSPACE
TASKS = 'https://www.toggl.com/api/v8/workspaces/%s/tasks' % WORKSPACE
TODAY_SUMMARY = 'https://toggl.com/reports/api/v2/summary?workspace_id=%(workspace)s&since=%(today)s&user_agent=test'\
                '&grouping=users&subgroupings=time_entries'


user_ids = {}
project_ids = {}

AUTH = (api_token, 'api_token')

def req(url):
    logger.debug(url)
    r = requests.get(url, auth=AUTH)    
    if r.status_code == 200:
        return r.json()
    else:
        return None

def get_dashboard():
    data = []
    dash = req(DASHBOARD)
    users = req(WORKSPACE_USERS)
    for user in users:
        user_ids[user['id']] = user['fullname']

    projects = req(PROJECTS)
    for proj in projects:
        project_ids[proj['id']] = proj['name']

    for a in dash['activity']:
        data.append({
            'user': user_ids[a['user_id']],
            'project': project_ids[a['project_id']] if a['project_id'] else '',
            'description': a['description'],
            'duration': str(timedelta(seconds=int(a['duration']))),
            'stop': re_date.search(a['stop']).group(1),
            })
    # We've got timeline from new to old, reverse it.
    data.reverse()
    return data


def get_summary(day):
    recs = req(TODAY_SUMMARY % {'workspace': WORKSPACE, 'today': day})
    #print json.dumps(recs, indent=4, sort_keys=True)
    data = []
    for rec in recs['data']:
        user = rec['title']['user']
        total_time = rec['time']
        user_data = {'user': user, 'total_time': str(timedelta(seconds=int(total_time)/1000)),
                      'time_entries': []}
        for line in  rec['items']:          
            user_data['time_entries'].append({
                'entry': line['title']['time_entry'],
                'time': str(timedelta(seconds=int(line['time'])/1000)),
                })
        data.append(user_data)
    return data


if __name__ == '__main__':
    d =  get_dashboard()
    for l in d:
        print l['duration'], l['stop']
