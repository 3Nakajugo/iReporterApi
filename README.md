[![Build Status](https://travis-ci.org/3Nakajugo/iReporterApi.svg?branch=feature)](https://travis-ci.org/3Nakajugo/iReporterApi)
[![Coverage Status](https://coveralls.io/repos/github/3Nakajugo/iReporterApi/badge.svg?branch=feature)](https://coveralls.io/github/3Nakajugo/iReporterApi?branch=feature)
[![Maintainability](https://api.codeclimate.com/v1/badges/86138da571cb34d40a23/maintainability)](https://codeclimate.com/github/3Nakajugo/iReporterApi/maintainability)
# iReporterApi

iReporter enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention.

## Technologies
* flask
* Python 3.7

## Running App

* clone the repository

```$ git clone https://github.com/3Nakajugo/iReporterApi.git```

* Change directory

```$cd (folder name)```

* create virtualenv

```$ virtualenv (name of virtual enviroment)```

* activate virtualenv

``` $ .\(virtualenv name)\scripts\activate ```

* install requirements.txt file

``` $ pip install requirements.txt ```

* run the application

``` $ python run.py ```

* run tests 

``` $ pytest ```



## End points

| End points  	                |  Method	| Routes                                |
|---	                        |---	    |---                                    |
|Create a red-flag record       | POST      |/api/v1/incidents                      |
| Get all red-flag records      |GET        |/api/v1/incidents                      |
| Get a specific red-flag record|GET        |/api/v1/incidents/<int:incident_id>    |
|Edit a specific red-flag record|PUT        |/api/v1/incidents/<int:incident_id>    |
|Delete a red-flag record	    |  DELETE   | /api/v1/incidents/<int:incident_id>  	|

### Author
Edna Nakajugo Margaret