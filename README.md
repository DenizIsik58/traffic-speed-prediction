# Traffic-speed-prediction
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![GitHub branch status check](https://img.shields.io/github/checks-status/denizisik58/traffic-speed-prediction/main?logo=GitHub&style=for-the-badge)
![GitHub](https://img.shields.io/github/license/denizisik58/traffic-speed-prediction?style=for-the-badge)

Everything in this repository is currently under development. The following information provided is used to boot up the application for development purposes or deploying the docker stack.
##Development

### Prerequisites
Make sure to have the following software installed before running the application:
- [Docker](https://www.docker.com/)

### Manual installation

In order to run the application manually, use the following command:

```docker-compose up -d```

Please keep in mind that docker doesn't provide docker-compose binary in some operating systems and could therefore be a reason for the command to fail. In that case you need to manually install it.

### Installation via scripts

A BASH and PowerShell script has been written to start up docker. The scripts will automatically start 2 containers - a postgres container for the database and one for the application.

**Unix:** `./StartApplication.sh`

**Windows:** `StartApplication.ps1`

You should now be able to visit https://localhost:8000

### .ENV
A .env file can be found in the source code in the following format:
```
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<dbname>
POSTGRES_HOST=db
```

## Continuous deployment

Everytime the development team has published a released, a new docker image for the application will be built and pushed to GitHub package registry using GitHub actions. The docker stack is managed by shepherd which will check for new package version every 5 minutes. 


###Deploying the stack

`sudo docker swarm init`

`sudo docker stack deploy -c deployment.yml tsp`

## Contributors
- Adrian Bay Dorph
- Anton Marius Breinholt
- Casper Wasser Skourup
- Deniz Isik
- Jack Kryger Sørensen
- Mads Piriwe Risom Andersen
- Villum Nils Robert Sonne

## License
- [MIT](https://github.com/denizisik58/traffic-speed-prediction/blob/main/LICENSE)

