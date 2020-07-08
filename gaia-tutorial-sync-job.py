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
# Submit the query as an asyn job
#
lang = 'PostgreSQL'
query = '''
-- Orbital elements of Solar System Objects

SELECT osc_epoch, orb_m, omega, node_omega, inclination, eccentricity, a
FROM gdr2.aux_sso_orbits;
'''
tap_results = tap_service.run_sync(query, language=lang)
print('...DONE\n')

#
# Convert to a pandas.DataFrame
#
results = tap_results.to_table().to_pandas()
print(results.head())
