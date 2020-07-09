from pkg_resources import parse_version
import requests
import pyvo as vo
import pandas as pd
from pyvo.dal import TAPService

#
# Verify the version of pyvo 
#
if parse_version(vo.__version__) < parse_version('1.0'):
    raise ImportError('pyvo version must larger than 1.0')
    
print('\npyvo version {version} \n'.format(version=vo.__version__))

#
# Setup tap_service
#
service_name = 'Gaia@AIP'
url = "https://gaia.aip.de/tap"
token = 'Token <your-token>'

print('TAP service {} \n'.format(service_name))

# Setup authorization
tap_session = requests.Session()
tap_session.headers['Authorization'] = token

tap_service = TAPService(url, session=tap_session)

# list of failed jobs
failed = []

#
# Submit queries
#
base_name = 'gal_coord_{index}'
lang = 'PostgreSQL'

base_query = '''
SELECT source_id, 
       xgal, ygal, zgal, rgal, 
       ruwe, mg0, bprp0 
FROM gdr2_contrib.starhorse AS s 
  WHERE s.SH_OUTFLAG LIKE '00000' 
    AND s.SH_GAIAFLAG LIKE '000' 
  LIMIT {limit:d} OFFSET {offset:d}
'''

limit = 1000
total = 10000
index = 0

# open the file to store the jobs
fd = open('jobs_url.txt', 'w')

# header 
print('          {: ^{name_width}} -- limit : offset'.format('name', name_width=len(base_name)-6))

for offset in range(0, total, limit):

    query = base_query.format(limit=limit, offset=offset)
    name = base_name.format(index=index)

    print('> Query : {name} -- {limit}:{offset}'.format(name=name, limit=limit, offset=offset))

    # Create the async job
    try:
        job = tap_service.submit_job(query, language=lang, runid=name, queue="2h")
    except Exception as e:
        print('ERROR could not create the job.')
        print(e)
        failed.append(runid)
        continue

    # Run the run
    try:
        job.run()
    except Exception as e:
        print('Error: could not run the job. Are you sure about your SQL query? Wrong language?')
        print(e)
        failed.append(name)
        continue

    # Save the submitted jobs into a file
    fd.write(job.url + '\n')
    index = index + 1

# Verify that all jobs have been submitted
try:
    assert(failed == [])
except AssertionError:
    print("The following jobs had failed: {jobs}".format(failed))

fd.close()
