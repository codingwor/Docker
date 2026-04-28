# Docker notes

-> docker ps == lists all the running containers == ps- process state<br>
-> docker ps -a == lists all the running and stopped containers<br>
-> docker rm name/id == removes that container from the list<br>
-> docker stop name/id == stops the running container<br>
-> docker image prune == Remove unused images<br>
-> docker container prune == Removes all stopped containers<br>
-> docker history [NAME/ID] == Show the history of an image<br>
-> docker rename NAME-OLD NAME-NEW == Rename a container<br>
-> docker cp [NAME]:/PATH /local/path == container -> host == copy files/directories between host and container<br>
-> docker info<br>

@Flags are options you add to a command to change its behavior ex: -a,-d..<br>

-> docker images == lists all the images present<br>
-> docker rmi name == will remove the image from the list<br>

@before removing images you need to remove the dependent conatiners and then rm image<br>
// before removing u must remove all dependent containers of that image//<br>
-> docker run name == will pull and run the image directly<br>
-> docker run redis:4.0 == ':' called tag will run a specified version<br>
-> docker pull name == will only pull and store it in our host, it wont run the image<br>
-> docker stop name == will kill/force stop the running conatiner<br>

##Images:
Images are read-only templates containing instructions for creating a container. A Docker image creates containers to run on the Docker platform. Think of an image like a blueprint or snapshot of what will be in a container when it runs.<br>

** -a : List all images (parents & intermediates)<br>
** -q : Return only the ID of each image<br>
\*\* -l : Return the last container<br>

@Containers:
A container is an isolated place where an application runs without affecting the rest of the system and without the system impacting the application.<br>

--rm : Remove the container when it is stopped<br>
-i : Keep standard output stream open<br>
-t : Run the container in a pseudo-TTY [interactive mode]<br>
-d : Run the container in the background [detach mode]<br>
-p PORTS : Publish or expose ports<br>
-net : Connect a container to a network<br>
-ip : Assign a static IP to containers (you must specify subnet block for the network)<br>

-> docker run ubuntu sleep 10 == keep this process alive without doing anything(ubuntu is just image it doesn't have any process in it to run) -> used to check logs, delay execution, keeps container alive temp -> without this sleep cmd as the image wont have anything to run it will exit immediately.<br>

-> docker exec <container_id> <command> == Uses an existing running container and Runs an additional command inside it<br>

-> docker run -d //name -> start machine and walk away (detach) //runs in the background
-> docker attach //first few no's -> come back and sit again (attach)//connects to running container<br>

-> docker run -it centos bash == "Start a Centos container and give me a terminal inside it"<br>

- This is actually two flags combined:<br>
- -i -> interactive
  - Keeps standard input open (so you can type)
- -t -> terminal
  - Gives you a proper terminal interface<br>

@port mapping
-> docker run -p 80:5000 webapp == <host_port>:<container_port> (port on ur computer):(post inside the container)
a webapp running on port 5000 inside container which cant be used by the user, now user can see it on localhost:80

# left(your sys) : right(inside conatiner)

@volume mapping
-> docker run -v /opt/datadir:/var/lib/MySQL MySQL == the data present in /var/lib/MySQL from MySQL image is now mapped to opt/datadir so that if you delete the data from var the data is still present in opt/datadir

-> docker inspect conatiner_name == will return all the details of the container in json format
-> docker logs conatiner_name == will return all the logs of that container which ran in the bg
L>> docker logs -f --since=10m TEST == Show the logs for the container "TEST" for the past 10 minutes
#since/details/follow or -f/tail or -n/timestamps/until

#dockerfile is needed

$$
Dockerfile -> docker build -> Image -> docker run -> Container -> Flask app runs
-> docker file path & -t -> image tag
-> docker build -f Dockerfile -t my-app == will build the dockerfile with image name as my-app
   # . : The PATH specifies where to find the files for the context of the build on the Docker daemon.
   # -t NAME : The name of the image to build, , a tag of the image can be specified image:tag.
   # -f : Specify the Dockerfile name from which to build the image. by default if no dockerfile is specified , docker daemon will search for a file name Dockerfile in the build context (Default is PATH/Dockerfile)

#do docker login before pushing
-> docker push image_name == will push the image to public docker hub registry & check path correctly like rand/web-app not just web-app

@DockerFile
-> it is built in a layered architecture
-> everything is in instruction and argument format
-> FROM Ubuntu == from/RUN/COPY/ENTRYPOINT is instr and Ubuntu is arg
-> step1: every Dockerfile should start with base os cmd or another image i.e From OS
-> step2: then install all dependencies i.e RUN pip install...
-> step3: then copy instruction files from our local system onto docker image i.e COPY ./opt/...
-> step4: specify the entry point to run the flask app and it will always run the cmd when the container starts i.e ENTRYPOINT FLASK_APP=/opt/source-code/app.py flask run

@Env vars
-> in app.py color=red; instead of directly specifying in code we can say color = os.environ.get('APP_COLOR') then then image it, it will take some random color.
-> if you want to pass var then use docker run -e APP_COLOR=blue simple-webapp-color
-> docker inspect image_name == you can see the env vars present under env keyword

@command
-> docker run ubuntu sleep 5 == so here sleep 5 is the command
-> so cmd could be like this CMD['command','param'] i.e CMD['sleep','5']
-> we have docker run ubuntu-sleeper -> sleeps but there is no seconds mentioned so u need to mention 5 after sleeper or else : entrypoint['sleep'] cmd['5'], it will directly take 5 and if u mention after -sleeper 10 it will simply override 5 to 10
-> so if you want to override entrypoint then u can say : docker run --entrypoint sleep2.0 ubuntu-sleeper 10

@docker-compose
# tool to define and run multiple containers using a single YAML file
================docker-compose.yml================
version: '3'

services:

vote:
  image: voting-app        || build : ./vote == it will first build the image and give temp name and use it
  ports:
    - "5000:80"
  depends_on:
    - redis

redis:
  image: redis

worker:
  image: worker            || build: ./worker
  depends_on:
    - redis
    - db

db:
  image: postgres
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
    POSTGRES_DB: votes

result:
  image: result-app        || build: ./result-app
  ports:
    - "5001:80"
  depends_on:
    - db

===========================
-> docker-compose up == will create all the containers with the prefix dir i.e root_worker...

@docker registry
# A registry is a place where Docker images are stored
-> docker.io/library/images/repo == docker.io is the registry, lib is user/account
#for private registry u need to first login other it will show couldn't found the image
-> docker login private-registry.io
-> docker run private-registry.io/apps/internal-app

# what if your running ur appli on premise and don't have private registry, how do you deploy your own private registry within ur org?
-> Docker registry is itself another application , it is available as docker image -- name is registry and exposes the API on port 5000
$$ Build + Tag (username/app) -> Push -> Store in Registry(Docker Hub) -> Pull anywhere ===== public registry
$$ Build + Tag (ip:5000/app) -> Push -> Local Registry -> Pull inside network ===== private registry
-> docker run -d -p 5000:5000 --name registry registry:2   # 2 is version
-> docker image tag my-image localhost:5000/my-image == tagging is required so that the docker will know now where to push the image i.e localhost:5000/my-image
-> docker push localhost:5000/my-image
-> docker pull localhost/ip_addr:5000/my-image

@docker engine
# host with docker installed on it
# it contains Docker Daemon (dockerd), RestAPI these both are backend and we have docker CLI which is frontend and its is client side means using out laptop, here we type our cmds
$$ Docker CLI -> REST API -> Docker Daemon -> Container runs
# ex:
   docker -H=10.123.2.1:2375 run nginx == run this in ur lapi
   10.123.2.1:2375 == sends request to remote docker engine
   REST API receives the request and passes request to docker daemon
   docker daemon pull the images and starts container on remote server(our sys)
   -H : Host == Tells docker to Use this remote engine instead of local one

@how docker containerize its application?
# docker uses namespaces to isolate workspace, it could be process id,network, interprocess, mount, unix time sharing
@namespace:
# to create isolation
# don't interfere with each other
# don't see host system
# behave like separate systems
# ex: consider process id namespace, in our (linux sys)host sys we have pid1 under this we have pid2,3,4,5,6 but inside this host system we have a container(child sys) which has pid1,2 which represents originally pid5,6. So, we can see that it gives each container its own process numbering system and it will act as a separate sys. Host = whole company(school), container = one department(class)
✓ Process isolation
✓ Containers don't interfere
✓ Cleaner environment

-> docker run --cpus=.5 ubuntu == will ensure that container doesnt take up more that 50% of the host
-> docker run --memory=100m ubuntu == max 100mb

@Docker storage
# for ex i have a built a dockerfile1 and ran it and want to build another dockerfile2 which has same first 3 steps as of first file, now it will not again build those 3 steps again, in this way it will save disk space.
# and while building each step taking some mb or b for storage.
-> Copy on write mechanism: (container layer == read-write layer && image layer == read only layer)
   # Once we build an image then it will be read only we cant write onto it, for that we again have to run that image in which we can read-write in container layer and once that container layer is deleted then the changes made will also get deleted.
   # suppose we have app.py in image built and if we want to make changes then docker will automatically make a copy of app.py onto container layer and we can make changes there, this is called copy on write mechanism
   # u cant modify image layer if u want to do any changes you can simply rebuild that image again using docker cmd

@volume: v is old mount is new
-> docker volume create data_volume == this will create a folder under /var/lib/docker < volumes < data_volume
-> docker run -v data_volume:/var/lib/MySQL MySQL == i could mount this volume inside the docker containers read write layer using -v option.
@mounting - 2types:
-> docker run --mount type=bind,source=/host/path,target=/container/path nginx
   1) volume mounting : mounts the volume from the volume directory.
   2) bind mounting : links a folder/file from your host machine directly into a container, complete folder path is given
# If you:
   create file on host -> visible in container
   create file in container -> visible on host

@storage drivers
# Storage drivers control how Docker stores and manages image and container data on disk
   Storage driver handles this merging:
   Read-only layers (image)
   +
   Writable layer (container)
   ↓
   Final container filesystem
# docker uses storage drives to enable layered architecture. AUFS, ZFS, BTRFS, Device mapper, Overlay, Overlay2

@Docker networking
# how containers communicate with each other, the host, and the outside world
# by default 3 n/ws are created
~ Bridge || docker run ubuntu
   - default n/w that container gets attached to, its internal private network created by docker on host
   - all containers attached to this n/w by default and they get internal IP addr 172.17.0.2/3/4/5.. series
   - to access any of these from outside world then map the ports of these containers to host port i.e 172.17.0.2:2375

~ None || docker run ubuntu --network=none
   - containers are not attached to any n/w and doesn't have access to external world or other containers they run in isolated n/w

~ Host || docker run ubuntu --network=host
   - running a container on a particular host, but we cant run containers parallelly we can only run one container in one host
   - if you are running a web server on port 5000 in a web container then its is automatically accessible on the same port without requiring any port mapping as the web container uses host network

~ User-defined Bridge Network || docker network create --driver bridge --subnet 182.18.0.0/16 custom-isolated-network
   - to isolate containers within docker host
   - by default docker can only create on internal bridge but if we want to create we need to run this cmd

#Embedded DNS == Docker's built-in DNS server that lets containers find each other using names instead of IP addresses

@Container orchestration
# automated management of multiple containers
# automatically run, manage, scale, and monitor containers
# popular ones are Kubernetes, docker swarm, mesos

@Docker swarm
# Run and manage multiple containers across multiple machines
-> docker swarm init
-> docker swarm join --token <token> <manager-ip>:2377 == add workers now we have a cluster
-> docker service create --name web -p 8080:80 nginx == creates a service
-> docker service create --replicas=3 my-web-app == it will create replicas
$$
