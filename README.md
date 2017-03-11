#Docker

## Module 1: Introduction to Docker
### Installation

#### Step one is to download our git repo:

```bash
git clone https://github.com/ferninphilly/introToDocker.git ~/introToDocker
```
Navigate to the IntroToDocker folder. Here you will find the CentOS box:

```bash
cd IntroToDocker
ls
```
You should see a file that looks like this: CentOS-7-x86_64-Vagrant-1701_01.VirtualBox.box. If I have been unsuccessful in uploading that
then please go to [this site](http://cloud.centos.org/centos/7/vagrant/x86_64/images/) to get the appropriate image. 
Please pick up CentOS-7-x86_64-Vagrant-1701_01.VirtualBox.box

#### Step Two is to set up our environment:
Now let's set up our environment! If you have vagrant installed, excellent!
If not you will need to navigate to [this](https://www.vagrantup.com/downloads.html) page and download Vagrant 1.9.2:

What I have set up here is just a base image- no frills- nothing added
We will be using this to install and configure DOCKER. Please run the 
following to set up the environment:

```bash
vagrant box add intro2docker CentOS-7-x86_64-Vagrant-1701_01.VirtualBox.box
vagrant init intro2docker
vagrant up
vagrant status 
vagrant global-status
```
Finally please add in vagrant-vbguest to allow us to mount folders (necessary for some future labs)

```vagrant plugin install vagrant-vbguest```

*Note: You may need to alter your vagrantfile when mounting! If this is the case please note that we will need to look at the config.vm.synced_folder in the vagrantfile and updating it accordingly!*

Now let's go in there and look around: `vagrant ssh` and just to make sure that we are on the right version: `cat /etc/redhat-release`

Should be CentOS 7

And, of course, let's: `sudo yum update && sudo yum upgrade` because we want to make sure that we are always on the latest versions

Okay! We're good to go now with our (basic) environment. 

#### Step Three- install utilizing docker repository	
For this next step we're going to be doing an install utilizing the repository. This will become more important in modules 4 & 5 but for now let's start here: `sudo yum install -y yum-utils`

Now we're going to add our repo: 
```
sudo yum-config-manager \
     --add-repo \
     https://download.docker.com/linux/centos/docker-ce.repo
```     
Now let's enable the edge repository (it's included in the docker.repo file) but it's not enabled by default. Let's enable it here: `sudo yum-config-manager --enable docker-ce-edge`

Now we're going to update the yum package index: `sudo yum makecache fast`

And now (finally) we're ready to install the latest *non-enterprise* version of docker. When you want to go enterprise you can have your own personalized repo which is awesome for managing images: `sudo yum -y install docker-ce`
We will also want to run the following:
```
sudo yum install epel-release
sudo yum install -y python-pip
sudo pip install docker-compose
sudo yum upgrade python*
```
Please note that what we've done here only installs the LATEST versions of docker. If you want to go version specific you can add the <VERSION> to the end of the sudo yum install docker-ce-<VERSION>

Okay-let's start her up: `sudo systemctl start docker`
Now let's go and make sure that everything is running by pulling an image and running it: `sudo docker run hello-world`
This is a basic docker image that will be downloaded and run. If docker is running correctly you should see a message that verifies that your installation appears to be running correctly. Congrats! Let's go on to configuration

#### Step Four: Configuration:
So here's the issue- the docker daemon binds to the Unix socket- which means that only root can access it using SUDO. As it becomes tiresome sudo-ing every command we want to create a unix group called docker and add users to it. When the docker daemon starts it switches ownership to this group and anyone in that group does not need to sudo everything.
So let's first create that group: `sudo groupadd docker`
And add our user (probably "vagrant" unless you have altered it): 
```
sudo usermod -aG docker $USER
```
Now logout of the system: `logout` and log back in:`vagrant ssh` and run your test again (but without SUDO this time!)
`docker run hello-world`

Now let's configure Docker to start on boot:`sudo systemctl enable docker`
Okay- so now let's go through some of the options you have around configuration of your docker daemon. 
The following command shows your default path in docker for 
the .service file
```
systemctl show --property=FragmentPath docker
```
From here you should get an idea of where your docker.service file
is located. You can make alterations to this file to control things
like limiting the disk space used by docker by moving it to a 
separate partition. You can do that by altering the [Service]
section of the file (don't do this now):

>ExecStart=
>ExecStart=/usr/bin/dockerd --graph=/mnt/docker-data --storage->driver=overlay
This will allow you to start docker from a partitioned drive. ALSO note the first blank line- this is necessary to avoid an error on startup.
You can also alter environment variables (useful if you are using an http proxy) by adding them as such (again- do not do this!):

>Environment="HTTP_PROXY=http://proxy.whatevs.com:80/"

If you'd like you can create a directory called:
>sudo mkdir /etc/systemd/system/docker.service.d
and create a .conf file called:
>/etc/systemd/system/docker.service.d/docker.conf

We're not going to touch this file yet but, as with any other config changes to any other program we will need to flush changes
`sudo systemctl daemon-reload`
And we will need to restart docker: `sudo systemctl restart docker` any time we make changes. 

Finally the key question- where are the logs? Well: `sudo journalctl -u docker`
Note: You might need to sudo this one.

## Module 2: Images
### Step One: download an image:
Now that we're ready let's start downloading base images. 
This works a lot like any other repo we know how to use. 
First let's see which images we already have: `docker images`
You probably see "hello-world" on there. This is fine- that's the only image that we've gotten so far. Let's add to that. 
We are on CentOS so let's get an Ubuntu image. First, we'll search for it (just as with yum, brew, apt-get, etc): `docker search ubuntu`
Lots of options here. Let's take a look at just doing the latest (though as you can see- tons of options to be had). To get the "latest" version of an image simply append ":latest" to the end of your pull request: `docker pull ubuntu:latest`

Okay- image is pulled. Let's execute it and see all of the awesome things it
has in store for us! `docker run ubuntu`

Well....that was...disappointing. 
Let's get another image that does something! `docker search whalesay`
And now let's pull it and run it...in a single command!
```
docker run docker/whalesay cowsay hello-government!
```

Obviously you have gotten the most advanced return ever seen by the eyes of man here! Not just some poorly drawn image of a whale....

What I want you to take away from this is the "docker run" command. 
Initially it searched for the image locally, couldn't find it, and immediately searched the repo, then pulled it, then ran it. Kind of a neat trick, right? Three steps in one...
If you have the time or inclination you can get the whale to say other things by (obviously) changing the parameter.
>Challenge: Take ten minutes and run and/or pull some other images from the repo


###Step Two: Managing images locally
Run this again: `docker images` and you should see the whalesay has been added.
The first thing we want to do here is go from image->container
(remember from the lecture that a container is an instantiated image)
SO- to do this we need to "docker run" the image and simultaneously access
the container (when you docker run something you are basically creating and tearing down the container). Let's start by seeing if there are any containers currenly running. The command to do this is:
docker ps
Now- let's say that you are annoyed by the buildup of containers (already) and you want to get rid of the pesky "hello world" image there. Seems simple enough: `docker rmi hello-world` where "rmi" is shorthand for "remove images".

BUT WAIT- there's been an error- it's alerting you that there is a stopped
container built from that image! So this would be the equivalent of deleting the CLASS whilean instantiated object is currently in existence. Could cause issues... What we want to do is get rid of any stopped containers when we remove this image. Let's take a quick look at what images we already have for docker with our `docker ps` command. 

Nothing. Hmm. Well let's look at **stopped** containers with 
```
docker ps -f "status=exited"
```
where -f is shorthand for filter...and there it is. 
So what is the takeaway here? After a run a container is *stopped* but it isn't *deleted*. As of docker 1.1.2 there is a handy command called `docker container prune` which will remove all stopped containers (used to be we had to use `docker rm $(docker ps -f "status=exited")` to do this but this is a useful little trick!).
Anyways- let's run:
```
docker container prune
```
and we can hit "y". Now let's look at our images with `docker images` and run `docker rmi` to get rid of our **hello-world** image.

A quick side note before we leave this step- save this command because occasionally you will become angry and frustrated with docker and just want to nuke everything: `docker rm $(docker ps -a -q)`
Where '-a' is for "show all containers" and '-q' is for "show just the numeric ids on these things!"
Following that- to nuke all of your images: `docker rmi $(docker images -q)`

### Step Three: 
So now let's get into a container to see what is going on under the hood. This is how you would utilize a running container normally- but since we've nuked all of our containers we need a running one, so...
```
docker run -it docker/whalesay bash
```
Where the **i** is for **interactive**- which means "keep stdin open" and the **t** is for allocating a psuedo-TTY.
So what we can see here is what is happening under the hood. We are currently *in* the whalesay container and free to poke around. We can look at the cowsay file with vi or just explore the README or whatever. 
One thing to note- run a quick `ps` from in this container and note what the top PID is. This will be important later...

### Step Four: 
So now let's explore some other options with our image. [Here](https://docs.docker.com/v1.13/engine/reference/commandline/run/) is a complete list of options for docker run. There are some extremely common options here that are worth exploring in depth as they are commonly used at the dev level. 

First thing to do is to look at fixing those complex image ids. Let's tag our image. Please run this command `docker tag ubuntu:latest uspto:practice`
Now let's see if it's there with `docker images`
Tagging is one of those really useful things that you should do up front- will save you agony down the road when you're dealing with a hundred or more containers!

Let's start with the working directory flag "-w" which is how we set the working directory within the container. If it does not exist then it is created. So we would do that with: `docker run -w /main/directory/ -it ubuntu bash` and as you can see- we are in the newly created "working directory" that we just set within our container. 
For mounted volumes- which are essential because in docker *this is how we create persistence* we have the **-v** (volume) command which will mount a volume from the host to the container. Write code in mounted volume, it persists, build container. 
First let's make a directory to work from: `mkdir docker_practice`
Then:
`cd docker_practice`
Okay- now let's mount our current directory:
```
docker  run  -v `pwd`:`pwd` -w `pwd` -i -t uspto:practice bash

```
and run a quick `pwd` from inside this container and you can see that we have a mounted working directory. 
*If the host directory does not exist* then docker will create it for you on the host before starting the container* which is kind of cool. 
Containers come and go. Files that go in containers need to be mounted on the host.
Type `exit` and leave the container for a minute. 
Now that we are back in our vagrant box (type "pwd" to make sure!) let's take a look at the container we just created! 
*Remember that **docker run** will take an image and create a container*
On the command line type `docker ps`
Okay- nothing, right?
Type `docker ps -a` ("a" is for "all")
You should now see your container. The reason it did not work under "docker ps" is because the container was *not running at the time*
This does not mean that we cannot run our docker container- and that is where another important command comes in: `docker exec`
`docker exec` basically means "execute this container". It's a way to pass a command line command into a container and have it executed. Let's give it a shot:
```
docker ps -a
<copy your docker container id>
docker exec <docker container id> echo "Hello I am a container!"
```
And....wait a second! STILL not running! Let's get it running with `docker run` BUT- we'll want it running in "detached" mode so that it will *not shut down* when we exit it! 
We do that with the "-d" tag as follows:
`docker run -i -t -d uspto:practice`
Now go back up and try our previous command again (you created a new container so you will need to get the new container id. You are creating a new container **every time** you type out `docker run`)
So what is the takeaway here? 
First off- docker containers are built and die in one command. They are *microservices* (as we went over in the lecture) and they are thus intended to do a single thing and die. They are not really built for **persistence**. 
That being said- you can **absolutely** have them persist by putting them into the "detached" mode utilizing the "-d" option in run. This means that they will continue to live

Now let's create a quick little file in here that we can run.
Let's do a quick little python app...  
You will find a copy of "requirements.txt" in the lab_02 directory. We'll use this to build our little app. We want that in our mounted directory so copy it into our mounted directory: */vagrant_mounted*
Let's also grab the *actual* code that goes along with this- so make a copy of fernapp.py into */vagrant_mounted/*
Now let's get all of the packages we need in our little docker container:
```
apt-get update && apt-get upgrade -y
apt-get install -y python-dev python-pip
pip install uwsgi
pip install -r requirements.txt
python fernapp.py
```
DARN that was a lot of work! And the worst part! When you `exit` from the program....all gone! 
Well...not so fast! 
Exit from the program (either with `CTRL P` and then `CTRL Q` or by typing *exit* on the command line)
Now that we're out run a `docker ps` and grab your container name
Let's commit that:
`docker commmit <container name> uspto/practice`

And let's try running it:
#### Challenge time:
Here's what we need to do to run this. You *have* the necessary tools! 
Step one: make a running, *detached* container (so that it keeps running)
Step two: execute a simple command on the command line into the container
Step three: write a simple "sh" file in the container that you can execute from outside the container by typing "sh <yourfile>". 

So how do we build our docker container "around" our application?

## Module 3: Dockerfile
Okay- so we've decided to build a single application using docker!
Remembering that docker is built around a "microservices" philosophy- let's do this using our old "MVC framework" methodology and break our application into two basic parts:
	1. Model: our server (we'll do POSTGRESQL)
	3. Controller: our code (python)
Let's set everything up so that we have a persistent "blueprint"


###Step One: Build out our model:
So now we'll need all of the requirements for a good postgresql database and place them in our Dockerfile. 
I have a dockerfile in the lab03 subfolder. Go in there and take a look at it keeping in mind what we learned from the previous lecture about what each of the commands means. 
We will need to copy this file into your mounted directory to allow vagrant to pick it up. 
Once it is in your mounted directory ssh into vagrant and cd into the folder where it exists. 
Now run this command: 
```
docker build -t postgres_container .
```
Now your postgres container will be build *and* tagged with a name!
Just to show you another capability- if you run that same command again it will rebuild the postgres_container from the cache. You have an option to completely rebuild from the ground up from your *Dockerfile* by using the
*--no-cache* option. 
It's a good one to know if you build the container and then want to make changes to your dockerfile and rebuild the container from the ground up. 
As we learned from the last lab- just because we have built the container doesn't mean it's running, though. At this point we have two options to run the new postgres container- through container linking (which is the next lab so don't want to spoil it) or directly from the host. 
Let's run it from the host:

Run a `docker images` and you should see your image that you just built. From here we need to run it. 

```
docker run --rm -P -d --name pg_test postgres_container
```
And now run a `docker ps` to make sure that it is installed successfully.
Please note the port forwarding when you docker ps here- you are forwarding into port 5432 of your main host. If you don't have postgresql installed on your virtual machine yet you can run `sudo yum install -y postgresql` and get it. Please do that now. 
Once postgres is installed let's forward into our docker container. In my example the port forwarding was from port 32769 so I will use this command to access postgresql in my docker container:
`psql -h localhost -p 32769 -d docker -U docker --password`
Spoiler alert- the password is *docker*

So now we have command line access to PSQL! Put in an entry if you'd like (don't forget to create a table first). 

Obviously the next issue is that we will need to persist this data somehow, right? I mean- a database is only good if the data lasts. 
This is where the MOUNTED VOLUMES becomes essential.
Use *\q* to back out of the psql command line and vi into your dockerfile (if you don't have vim installed yet run a `sudo yum install vim`)
You see where we are mounting the files there? This is essential. 

###Step Two: Build out our controller:
Now that we have our model built out (sort of)- let's build out our controller. Let's use *python* for this exercise. 
First thing we'll want to do (as we'll be using different Dockerfiles for this) is minimize confusion. Please alter the name of the existing dockerfile to *Dockerfile_postgres*: `mv Dockerfile Dockerfile_postgres`
Now let's grab another Dockerfile. This one will be relatively simple- you can find it in the root directory as *Dockerfile_python*
Vim into it and take a look at it.
You can probably see what it does in pretty plain language. Let's try building it! 
```
docker build -t controller:latest -f Dockerfile_python .
```
In this case you see us using the "-f" which is for "file". 
The "." means "build it right here". 
NOW- before we *run* this container let's make a quick alteration and take advantage of port forwarding again! 
```
docker run -p 5000:5000 controller
```
So what we're saying is *"take this flask app, point it at port 5000 (which
we are forwarding to) and run it "*

No open another tab and run `curl 127.0.0.1:5000`
You should get a message there. 
And this is how we build a basic container!
Going back to our original tab you should see the log from where we hit! 
Obviously if we *had* a browser here you would see this as a web page.

So now what if we wanted to connect these two containers? 
That will be the subject of our next lab. 

##Challenge: 
Create a Dockerfile and an app that outputs the square of a number given in the "run" command. (you may need to google some of this but you have all the tools!)

##Module 4: The Docker yaml files
The docker yaml file is how we link together numerous containers to create an app. It basically creates multiple containers, creates a network for them, and then links them. 
In this exercise we will be utilizing the docker-compose command on our yamls. To review where we are thus far: 
`docker build` -- builds the image
`docker run ` -- builds the container (instantiates the image)
*Dockerfile* is the blueprint for the image. 
Now let's talk about `docker-compose` which utilizes a yaml to merge multiple containers together into an app (thus allowing us to keep our "microservices philosophy" intact).
To demonstrate how this works we'll build a simple redis/python flask app counter that will run on localhost. 

This application will require *two* containers to run: a *web app* that will basically run the web section and then a *redis* image to act as our back end (to ensure persistence)
The first thing we want to do (obviously) is copy the files over to our mounted system from the lab_04 directory...so let's do that. 

Once everything is over we will engage in our first "docker-compose" command- which will be very similar to our "docker build" command:
```
docker-compose -f docker-compose.yml --project-name redis_and_python build
```
Where the -f points to a file and (notice the change here!) you will change from --name to --project-name to tag the image appropriately
Now let's run a `docker images` to make sure that everything has been built correctly and you should see your image there. 
Now let's launch this thing using another command (docker-compose up):
```
docker-compose -f docker-compose.yml --project-name redis_and_python up -d
```

Now let's see if this is running in our containers with a `docker ps`
And you should see that you have created two containers- a _web and a _redis container. This is how we will end up maintaining the count. 
Now- as this is a more public deployment we will need to grab the assigned IP address to our docker container- so let's look at something like this:
```
docker inspect redisandpython_web_1 
```
And as you can see there is a ton of data about that container. Let's see about *just* grabbing the IP address:
```
WEB_APP_IP=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' redisandpython_web_1)

``` 
Now let's see if this worked:

```
curl http://${WEB_APP_IP}:80
```

And you should see your hit counter app up and running using both REDIS and PYTHON (flask)
This is (hopefully) a brief taste of the awesomeness that you can create with linked containers! 
What I want you to think about here is how these containers can be used to create simple things like ETLs and basic micro-apps that do-a-thing and then die. Are there places in your organization where you can use stuff like this? 

##Challenge three:
Create your own yaml that combines a back end (lightweight- something like REDIS or sqlite) that does it's own hit counter and outputs to the command line!























