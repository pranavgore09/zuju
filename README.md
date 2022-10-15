# APIs for listing Fixtures

## Pre-requisite
This application uses containerized setup.
Please make sure you have installed docker, docker-compose and make.

Makefile is used to fire repetitive commands in fewer words.

Type `make --version` to make sure that you have make command working.
Alternatively, entire project can be run using an virtual environment and psql database but I have not tested it, hence focus is only on docker setup.

Make sure that port 8000 is available and no other services are running. It is best to stop+remove all running containers before going ahead.

### This setup is verified under
1. Host OS is `Ubuntu 20.04.5 LTS`
2. Docker version `20.10.17, build 100c701`
3. docker-compose version `1.29.2, build 5becea4c`

## Please follow the steps in given order

First, we will initialize the current directory. This action will create required directories in the local folder. For production system this should not be required.
> `make init`

We will build the image locally, it requires internet connection as it pulls varies images like python3.8, postgres and few pip install, it might ask to enter the password
> `make build`

Once build is ready, proceed to run the server using
> `make dev`

Now, run migration so that we can start using Django Admin.
> `make migrate`

Let's create a super user to log into Djagno Admin (Hint: use admin:admin as username:password when asked on terminal - easy to remember.)

>`make createsuperuser`


Visit http://localhost:8000/admin/ and login using newly created credentials.

Let's feed some data to the system
>`make loaddata`


If you have not changed any of the project configurations, then it will create about ~240 fixtures for one tournament. This helps in testing the application from openapi doc.


Visit [fixtures-link](http://localhost:8000/admin/fixtures/fixture/) to verify all fixtures are created as expected.

Visit [teams-link](http://localhost:8000/admin/teams/team/) to verify all teams data.

Visit [tournaments-link](http://localhost:8000/admin/tournaments/tournament/) to verify the tournament record.

## Testing APIs via documentation
#####  Fixtures Listing
- Open http://localhost:8000/schema/
- Click on `/fixtures` API (first in the list)
- Click on `Try out` on right top of that section. (Text field is now accessible)
- Copy a valid tournament UUID from [tournaments-link](http://localhost:8000/admin/tournaments/tournament/) and paste it in "tournament_uuid" field
- Click on `Execute`
- Verify the result
- For further testing you can copy the `next` URL and paste in a new tab
- Then use "prev" and "next" buttons to navigate the API responses on that new tab
- FE will call next and prev URLs when user scrolls up or down the page.


#####  Fixtures Calendar
- Open http://localhost:8000/schema/
- Click on `/fixtures/calendar/{month}` API
- Click on `Try out` on right top of that section. (Text field is now accessible)
- Enter a valid month from 1-12
- Copy a valid tournament UUID from [tournaments-link](http://localhost:8000/admin/tournaments/tournaments/) and paste it in "tournament_uuid" field
- Click on `Execute`
- Verify the response. Each record contains "date <> match_count"
- FE can use this API to show clickable-buttons on calendar view

#### Constants that will change fixture count (Open local_settings.py and change if required)
```
FIXTURES_PER_DAY : How many matches per day (default=2)
FIXTURES_ON_WEEKDAY : Which days to schedule matches on (default=Fri, Sat, Sun)
SUPPORTED_TOURNAMENT_TITLES : Default Tournament Titles used are (EPL, Serie A). One of these will be used
DEFAULT_MONTHS_IN_PAST: Schedule matches in past
DEFAULT_TOURNAMENT_DURATION_IN_MONTHS: How many months a tournament should run
DEFAULT_FIXTURE_PAGE_SIZE: Page size for cursor paginated API (default=3)
DEFAULT_TEAM_COUNT: How many teams should be enrolled in system (default=2)
DEFAULT_TOURNAMENT_COUNT: How many tournaments should be created (default=1)
```

If you change the settings, you need to call `make loaddata` again to make that effect in database. This action will not remove any existing data but it will add more data to the database.


Visit http://localhost:8000/schema/ for documentation.

All Fixtures
http://localhost:8000/fixtures/

Calendar view
http://localhost:8000/calendar/10/


### Project Structure
- Using Python-Djnago-PostgreSQL setup for the assignment purpose. I understand that, In actual work, technology/tool will be different and I will be able to adapt to that in the future.
- "z_common" is an app folder that contains all common work. Base classes, Abstract classes and generic code which will be used across the app will go into "z_common".
- requirements file is broken down into multiple as per environment requirement.
- "zuju" is the main entry-point django app for the project.
    - This app holds the settings file and local_settings file.
    - Many parameters can be changed from settings file and programs behavior will change.
- Teams / Tournaments / Fixtures are other django apps
    - Each app contains a models.py. It describes all database tables schemas
    - Each app contains serializer.py. It describes how the object will be transformed into an dictionary in the API response
    - Each app contains api.py. This is data-layer of each model. All CRUD should happen through this layer only. (Acts as a Factory)
    - Each app contains admin.py. It describes how admin panel will be shown to user. It is highly customized by adding custom-search feature. I have followed [HakiBenita's blog](https://hakibenita.com/how-to-add-a-text-filter-to-django-admin) for the same. I hope that is okay. It is very helpful to debug the system.
- load_data is a command line tool/script that helps me build sample dataset for demo purposes
- I am using `Faker` to create random team names, please enjoy those funny names :)

### Acceptance Criteria (as mentioned in assignment)
####  Fixtures Listing
- API should return all fixtures under one tournament
- API should return details of each fixture
    - Home Team
    - Away Team
    - Current state of the fixture (Live/Confirmed/Full-Time)
    - Date Time of the match
- I am using Cursor Pagination (AKA Keyset pagination) because ->
    - UI does not need to show page numbers 1,2,3,4
    - UI does not need jumping to specific page
    - User is not selecting page size
- CursorPagination suits this use case and performs better because ->
    - It will not scan the database until last record
    - It will just return records from last known record using its PK<>Created_at composite key.
    - I am using PostgreSQL hence underline query will use row comparison using `> (created_at,pk)` query.

#### Fixtures Calendar
- As shown in the picture, user can change the month only. Hence API takes month as input
- API should return days on which fixtures are confirmed
- API will not return days where fixtures are not available
- UI can render the calendar view and allow user to click only when the "count" of fixtures on that day is greater than zero.
- Pagination is NOT used here, this API works on input month input. Only given month's records will be returned

### Expectations (as mentioned in assignment)
- Code repository is accessible and has a detailed README.md
- APIs are documented and available to test at http://localhost:8000/schema/ (Only after running the application)
- With permission, I am using Python stack for the assignment.
- Few tests are added in the code, more can be done.

### Improvements I would like to make
- Logging can be added across the application, easy to debugging
- Sentry like systems can be integrated for better overview of errors and exceptions
- Caching can be used for API responses.
    - Cache will get invalidated when we load new fixtures
- Authorization is not considered while working on the assignment, it can be added and then each API will need JWT like some authorization to get valid response
- Tournament and Team can have Many-to_many relationship but it is not considered for the scope of the assignment
- Application can be extended to include Players and more entities



### Applicaion tear down
To stop the service and remove containers
> `make clean`

> `sudo chown -R $USER postgres-data/`

> `rm -rf postgres-data/` (removes all application's data)

### Re-running the application without build
> Make sure that you did the teardown steps completely
> `make dev`

### Re-running the application with build
> `make build`
> `make dev`


## FAQ
#### How to monitor server logs?

To follow application logs for dev purposes (uses "follow", you will have to use ctrl+c to come back to shell)
> `make logs`
#### How to access the django application inside container?
> `make bash`

Alternatively run `make shellplus` or `make shell` to enter Django shell.

