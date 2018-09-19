from  setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    README = fh.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-weeklycalendar',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='GPL License',  
    description='Weekly Calendar for Django',
    long_description=README,
    url='https://github.com/yvznvr/WeeklyCalendar',
    author='Yavuz Unver',
    author_email='yvzunver@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
