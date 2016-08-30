##Url Resolver

####Notes:
- first django app. That was fun!
- lots of error handling is missing... :sadpanda:
- 4 hours time-boxed. (not including some django docs pre-reading.)

####Goals:
* [x] User should be able to submit any URL and get a standardized, shortened URL back
* [x] User should be able to configure a shortened URL to redirect to different targets based on the device type (mobile, tablet, desktop) of the user navigating to the shortened URL
* [x] Navigating to a shortened URL should redirect to the appropriate target URL
* [x] User should be able to retrieve a list of all existing shortened URLs, including time since creation and target URLs (each with number of redirects)
* [x] API requests and responses should be JSON formatted.
* [x] Write tests to prove functionality.

####Api Guide
All interactions are through /u/
- Post with body `{ 'desktop_url': 'test.com' }` creates. (mobile_url, tablet_url fields are optional)
- Get /u/ will return 'index' which will list all created with 'created_at', and 'redirect_count'
- Get /u/:slug where slug is the 10 char slug given within the create (or index) response will rediect according to mime-type

####Dev Setup Instructions
(assuming mac.)
- install virturalenv `pip install virtualenv`
- create virtural env `virtualenv venv`
- activate env - `source venv/bin/activate`
- install requirements `pip install -r requirements.txt`
- db migrations `python manage.py migrate`

####Test Instructions
- Follow dev-setup above.
- run `python manage.py test url_resolver`

####Server Instructions
- Follow dev-setup above.
- run `python manage.py runserver`
- server should be running on `http://127.0.0.1:8000/`
