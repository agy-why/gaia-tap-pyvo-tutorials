from pkg_resources import parse_version
import requests
import pyvo as vo
import pandas as pd

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

tap_service = vo.dal.TAPService(url, session=tap_session)

#
# Submit the query as an async job
#
query_name = "tgas_stars"
lang = 'PostgreSQL'

query = '''
-- Number of TGAS stars with parallax / parallax_error > 10

SELECT COUNT(*)
FROM gdr1.tgas_source
  WHERE parallax / parallax_error > 10;
'''

job = tap_service.submit_job(query, language=lang, runid=query_name, queue="30s")
job.run()

#
# Wait to be completed (or an error occurs)
#
job.wait(phases=["COMPLETED", "ERROR", "ABORTED"], timeout=30.)
print('JOB {name}: {status}'.format(name=job.job.runid , status=job.phase))

#
# Fetch the results
#
job.raise_if_error()
print('\nfetching the results...')
tap_results = job.fetch_result()
print('...DONE\n')

#
# Convert to a pandas.DataFrame
#
results = tap_results.to_table().to_pandas()
print(results.head())
