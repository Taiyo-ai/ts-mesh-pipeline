from setuptools import setup, find_packages

setup(
	name='gdacs_timeseries',
	version='0.0.1',
	description='Time-series event store for disaster events that occurred in India Using GDACS Disaster Alerts.',
	author='Julio Cojom',
	author_email='jul.alejandro5@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True
	# install_requires=install_requires
	# dependency_links=[str(ir._link) for ir in requirements if ir._link]
)

print('Execute "docker exec -it <image name> python3 client.py --step (1, 2, 3, 4, 5, clean)')