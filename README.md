# Traffic-speed-prediction
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![GitHub branch status check](https://img.shields.io/github/checks-status/denizisik58/traffic-speed-prediction/main?logo=GitHub&style=for-the-badge)
![GitHub](https://img.shields.io/github/license/denizisik58/traffic-speed-prediction?style=for-the-badge)

Everything in this repository is currently under development and is being developed for the company <u>[Solita](https://www.solita.fi/en/?utm_campaign=EST:+Brand&utm_term=solita&utm_source=adwords&utm_medium=ppc&hsa_kw=solita&hsa_acc=2178929025&hsa_mt=e&hsa_grp=123766618555&hsa_tgt=kwd-334844187&hsa_src=g&hsa_cam=13334249436&hsa_net=adwords&hsa_ad=525097120039&hsa_ver=3&gclid=CjwKCAjw9-KTBhBcEiwAr19igyzTDgaTbxDB4OXuDHPWwFqxYIEXXrlGfyWRza2-p1sCwaj-uH7nPBoCzR4QAvD_BwE) </u>. The following information provided is used to boot up the application for development purposes or deploying the docker stack to production.


This repository is managed by dependabot in order to keep all packages up to date and be alerted if there are any vulnerabilities in the source code.
## Development

### Prerequisites
Make sure to have the following software installed before running the application:
- [Docker](https://www.docker.com/)


Also, it is important to import 2 .env files. One for the `Frontend` and one for the `App`:

**App:**
```
NODE_ENV=<production/development>
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<dbname>
POSTGRES_HOST=db
SECRET_KEY=<a strong auto generated key (should be 100+ characters long)>
```

**Frontend:**

```
NODE_ENV=<production/development>
REACT_APP_MAPBOX_SECRET_KEY=<MapBoxSecretKey>
REACT_APP_BACKEND_PRODUCTION_URL=https://tsp.hostanything.org
REACT_APP_BACKEND_DEVELOPMENT_URL=http://localhost:8000
```

Both .env files contains a variable called NODE_ENV representing the current state of the project. It's very <u>IMPORTANT</u> to update these as it can expose harmful information, if it ends out in production. 

Change the value to `development` when you are in development or `production` when you are going to deploy.


### Manual installation

#### App:
In order to run the application manually, make sure to navigate to the `App` folder and run the following command:

```docker-compose up -d```

Please keep in mind that docker doesn't provide docker-compose binary for some operating systems, and could therefore be a reason for the command to fail. In that case, you'll need to manually install it.

#### Frontend in development:

In order to run the frontend in development all you need to do is to navigate to the `Frontend/reactjs` folder and run the following command:

`npm start`

You should now be able to visit http://localhost:3000

The page will reload when you make changes.
You may also see any lint errors in the console.

#### Frontend in production:
If you want to see how it looks and functions in production you first need to build the react application and then you can serve it for the public:

```
1. npm run build
2. serve -s build
```



## Continuous deployment

Every time the development team publishes a release, a new docker image for the application and frontend will be built and pushed to **GitHub package registry** using GitHub actions. All files for GitHub actions can be found in the `.github` folder.

Make sure to add your GitHub access token into your repository. [Follow this tutorial to add secrets to your repository.](https://github.com/Azure/actions-workflow-samples/blob/master/assets/create-secrets-for-GitHub-workflows.md)

The docker stack is managed by **shepherd**, which will check for new package version every 5 minutes and update the services on the host machine if there are any changes.

[Shepherd](https://github.com/djmaze/shepherd) is a utility to automatically update your services whenever their image is updated (Upon making a release).


### Deploying the stack

Docker swarm has been used for the deployment stack as it allows the development team to manage multiple containers across multiple hosts. It is also very beneficial as it gives high availability and makes it easy to scale.

`sudo docker swarm init` - This will initialize a new cluster for the services. It generates two random tokens, a worker token and a manager token. When you join a new node to the swarm, the node joins as a worker or manager node based upon the token you pass to swarm join.

`sudo docker stack deploy -c deployment.yml tsp` - This will deploy the complete application stack to the swarm by using the *deployment.yml* file.


Note that the deployment.yml file contains our own images (App & Frontend) as services together with some other services. Our own images are as described above pushed into our personal GitHub Container Registry. 

If you do not have your images on GitHub Registry yet, please make sure to do so:
```
1. docker build . --tag ghcr.io/<YourGitHubName>/<ImageName>:latest
2. docker run ghcr.io/<YourGitHubName>/<ImageName>:latest
3. docker push ghcr.io/<YourGitHubName>/<ImageName>:latest
```


Run step 1 for all the services you serve. In this case we are serving the backend (App) & the Frontend. Therefore, we need to build both images and push them to our repository.

Run step 2 for all the services to make sure that the services serves as intended before pushing them into production.

Run step 3 to push the final images to production. Remember, if you already have a docker swarm running with the deployment file, and you update an image by pushing it to your repository, shepherd will see a new version and immediately adjust changes into production.


In order to see how it's functioning in production, and before you initialize a docker swarm, you can simply run the deployment.yml file by running the 2 commands at the beginning of this section. But make sure that the images exists in your GitHub repository beforehand.

## Additional information

The cloud host of choice for this project is Linode, and the database is postgres. You can use whatever
provider you want to use to host the application on and the same goes with the database. 


Keep in mind that the machine learning part can be a heavy process and therefore needs a strong host machine to train itself
(We are currently using a Linux machine with 2GB RAM and are having difficulties).

All you need to do to get started with the project is:

```
1. Find a provider you want to host your application on e.g AWS EC2
2. Find a database provider you want to store your data on e.g AWS DynamoDB
3. Put the information into the .ENV files
4. Scrape the data by using our scraper and load your database up with road information.
5. Train the model.
6. Set up the services with docker swarm by using the guide above.
7. Host the service to the public and enjoy your predictions!
```



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

