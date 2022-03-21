# Traffic-speed-prediction
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![GitHub branch status check](https://img.shields.io/github/checks-status/denizisik58/traffic-speed-prediction/main?logo=GitHub&style=for-the-badge)
![GitHub](https://img.shields.io/github/license/denizisik58/traffic-speed-prediction?style=for-the-badge)

Currently under development. The following information given is used to boot up the application.

## Prerequisites
Make sure to have the following software installed before running the application:
- [Docker](https://www.docker.com/)

## Manual installation

In order to run the application in development, use the following command:

```docker-compose up -d```

Please keep in mind that docker doesn't provide docker-compose binary in some operating systems and could therefore be a reason for the command to fail.

## Installation via scripts

A BASH and PowerShell script has been written to start up docker. The scripts will automatically start postgres and the application. 

**Unix:** StartApplication.sh 

**Windows:** StartApplication.ps1

## .ENV
A .env file can be found in the source code in the following format:
```
POSTGRES_USER="<username>"
POSTGRES_PASSWORD="<password>"
POSTGRES_DB="<dbname>"
POSTGRES_HOST="db"
ConnectionString_TSP:"Server=db;Database=<dbname>;UserId=<username>;Password=<password>"
```

## Contributors
- Adrian Bay Dorph
- Anton Marius Breinholt
- Casper Skourup
- Deniz Isik
- Jack Kryger Sørensen
- Mads Piriwe Risom Andersen
- Villum Niels Robert Sonne

## License
- [MIT](https://github.com/denizisik58/traffic-speed-prediction/blob/main/LICENSE)

