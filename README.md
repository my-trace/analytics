# MyTrace Core API

## Setup

### Dependencies
Install these before getting started.

1. python
2. pip
3. virtualenv
4. foreman [https://github.com/ddollar/foreman](https://github.com/ddollar/foreman)

### Create virtual env
```
$ foreman run env
$ source env/bin/activate
```
### Install packages
```
$ foreman run install
```

### Create migration folder
```
$ foreman run python manage.py db init
```

### Run a migration
Repeat this every time the models change.
```
$ foreman run python manage.py db migrate
$ foreman run python manage.py db upgrade
```

## Development

### Run the app
```
$ foreman run web
```

### Run the tests
```
$ foreman run test
```

### Environment vars
Edit the `.env` file.

**WARNING:** The tests require a valid user oauth token in the environment. These expire every 2 months and need to be manually changed or else the tests will fail.

## Deployment

### Build the Docker image
```
$ foreman run build
```

### Run the Docker container
```
$ foreman run docker
```

### Environment vars
The `.env` is in the `.dockerignore` so don't use that. Use the command line `--env` option. See `bin/docker` for example.


## Routes

### GET /health
A health check endpoint.

### POST /users
Register a user from Facebook.
```yaml
headers:
  Authorization: <fb token>
  Content-Type: application/json

body:
  name: string
  email: string
```

### POST /points
Save a user's points.
```yaml
headers:
  Authorization: <fb token>
  Content-Type: application/json

body: json-array of the attributes for the Point (see model section)
```

```
[ { latitude: 37.78627132548483,
    floorLevel: null,
    horizontalAccuracy: 65,
    verticalAccuracy: 10,
    uuid: '3C332578-2A1F-40D5-9A16-EB9F7CE724DF',
    longitude: -122.3976185810548,
    timestamp: 1472717834.417828,
    altitude: 12.39452648162842 },
  { latitude: 37.78627132548483,
    floorLevel: null,
    horizontalAccuracy: 65,
    verticalAccuracy: 10,
    uuid: '4ABCE83B-4557-4556-9421-51E0238656A7',
    longitude: -122.3976185810548,
    timestamp: 1472717834.417852,
    altitude: 12.39452648162842 }]
```

### GET /points
Retrieve a user's points within a time interval (default the past week)
```yaml
headers:
  Authorization: <fb token>

querystring:
  from: unix timestamp milliseconds
  until: unix timestamp milliseconds
```

## Models

### Account
| attr | type |
| ---  | ---  |
| id   | BigInt |
| name | varchar |
| email | varchar |
| created_at | timestamptz |

### Point
| attr | type |
| ---  | ---  |
| id   | uuid |
| lat  | double |
| lng  | double |
| alt  | double |
| floor_level | int |
| vertical_accuracy | double |
| horizontal_accuracy | double |
| account_id | BigInt |
| created_at | timestamptz |
