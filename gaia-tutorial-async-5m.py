from pkg_resources import parse_version
import requests
import pyvo as vo
import pandas as pd
import time

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
query_name = "glob_clust"
lang = 'ADQL'

query = '''
-- M4 globular cluster with geometric distances using ADQL

SELECT gaia.source_id, gaia.ra, gaia.dec, gd.r_est
FROM gdr2.gaia_source gaia, gdr2_contrib.geometric_distance gd
  WHERE 1 = CONTAINS(POINT('ICRS', gaia.ra, gaia.dec), 
                   CIRCLE('ICRS',245.8962, -26.5222, 0.5))
    AND gaia.phot_g_mean_mag < 15
    AND gd.r_est BETWEEN 1500 AND 2300
    AND gaia.source_id = gd.source_id
'''

job = tap_service.submit_job(query, language=lang, runid=query_name, queue="5m")
job.run()

print('JOB {name}: SUBMITTED'.format(name=job.job.runid))

#
# Sleep for 2 minutes.
#
while job.phase not in ("COMPLETED", "ERROR", "ABORTED"):
    print('WAITING...')
    time.sleep(2. * 60.) # do nothing for 2 minutes

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
