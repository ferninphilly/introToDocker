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
For this next step we're going to be doing an install utilizing the repository. This will become more important in modules 5 & 6 but for now let's start here: `sudo yum install -y yum-utils`

Now we're going to add our repo: 
```
sudo yum-config-manager \
     --add-repo \
     https://download.docker.com/linux/centos/docker-ce.repo
```     
Now let's enable the edge repository (it's included in the docker.repo file) but it's not enabled by default. Let's enable it here: `sudo yum-config-manager --enable docker-ce-edge`

Now we're going to update the yum package index: `sudo yum makecache fast`

And now (finally) we're ready to install the latest *non-enterprise* version of docker. When you want to go enterprise you can have your own personalized repo which is awesome for managing images: `sudo yum -y install docker-ce`

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

Let's start with the working directory flag "-w" which is how we set the working directory within the container. If it does not exist then it is created. So we would do that with: `docker run -w /main/directory/ -it ubuntu bash` and as you can see- we are in the newly created "wortking directory" that we just set within our container. 
For mounted volumes- which are essential because in docker *this is how we create persistence* we have the **-v** (volume) command which will mount a volume from the host to the container. Write code in mounted volume, it persists, build container. 
First let's make a directory to work from: `mkdir docker_practice`
Then:
`cd docker_practice`
Okay- now let's mount our current directory:
```
docker  run  -v `pwd`:`pwd` -w `pwd` -i -t  ubuntu bash

```
and run a quick `pwd` from inside this container and you can see that we have a mounted working directory. 
*If the host directory does not exist* then docker will create it for you on the host before starting the container* which is kind of cool. 
Containers come and go. Files that go in containers need to be mounted on the host.
Now let's create a quick little file in here that we can run.
Let's do a quick little python app...  
You will find a copy of "requirements.txt" in the lab_02 directory. We'll use this to build our little app. We want that in our mounted directory so copy it into our mounted directory: */vagrant_mounted*
Let's also grab the *actual* code that goes along with this- so make a copy of fernapp.py into */vagrant_mounted/*
Now let's get all of the packages we need in our little docker container:
```
apt-get update && apt-get upgrade
apt-get install -y python-dev python-pip
pip install uwsgi
pip install -r requirements.txt
python fernapp.py
```
DARN that was a lot of work! And the worst part! When you `exit` from the program....all gone! 






 In order to mount the file we utilize the "-v" option. SO- if we wanted to mount our current working directory into our bright, shiny new ubuntu container we would do this:
docker run -v 


#### Challenge time:
Okay- for each of you please download and run a ubuntu image and then get into that image and install python 3.4. 








