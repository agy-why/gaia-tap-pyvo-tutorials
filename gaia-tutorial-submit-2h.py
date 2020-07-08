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

#
# Submit the query as an async job
#
query_name = "glob_clust"
lang = 'PostgreSQL'

query = '''
-- M4 globular cluster using PostgreSQL 

SELECT ra, dec, phot_g_mean_mag AS gmag
FROM gdr1.gaia_source
  WHERE pos @ scircle(spoint(RADIANS(245.8962), RADIANS(-26.5222)), RADIANS(0.5))
    AND phot_g_mean_mag < 15
'''

job = tap_service.submit_job(query, language=lang, runid=query_name, queue="2h")
job.run()

print('JOB {name}: SUBMITTED'.format(name=job.job.runid))
print('JOB {name}: {status}'.format(name=job.job.runid , status=job.phase))

#
# Save the job's url in a file to later retrieve results.
#
print('URL: {}'.format(job.url))

with open('job_url.txt', 'w') as fd:
    fd.write(job.url)
