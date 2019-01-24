# Movie Journal

This is a flask web app for the Item Catalog project for Udacity's fullstack nanodegree program. It's called "Movie Journal" a website where you can add and edit your own movies in different genres.

## Getting Started

To get this web app up and running on your local machine, first you need: 

* Terminal (Linux, Mac) or Git Bash (Windows) - if you don't have git installed you can get it [here](git-scm.com).
* Virtual machine (VirtualBox, Vagrant).


## Installing

 Install VirtualBox:

VirtualBox is the software that actually runs the virtual machine, [download it here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).

 Install Vagrant:

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [download it here](https://www.vagrantup.com/downloads.html). Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

Download the VM configuration:

You can clone or download the repository https://github.com/udacity/fullstack-nanodegree-vm. This will give you a directory called FSND-Virtual-Machine.

open terminal and change into the directory FSND-Virtual-Machine/vagrant then startup the virtual machine:

```
cd Downloads/FSND-Virtual-Machine/vagrant
vagrant up
vagrant ssh
```

place the files in the "Movie Journal" folder inside the catalog directory.

in your terminal app change into the catalog directory inside the virtual machine:

```
cd /vagrant/catalog

```


## Running The Web Application Locally

To run this web application first you need to start up the "movies" database:

```
python movies_database.py
```

then to add movies to the database:

```
python listofmovies.py
```


after you setup the database you can startup the web app:

```
python Movie_Journal.py

```


ENJOY and let me know what movies you added :) !


### Coding Style Tests

pycodestyle is a tool to check your Python code against some of the style conventions

```
Pycodestyle --first ReportTool.py
```


## Authors

* **Yara Alotaibi** - *Initial work* - [Yaraotaibii](https://github.com/yaraotaibii)

## Acknowledgments

* This project is part of Udacity full stack nanodegree program

