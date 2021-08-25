# capstoneproject-comp3900-w18a-default
capstoneproject-comp3900-w18a-default created by GitHub Classroom

## Set up instructions

After pulling the project from Github, please follow the following steps:

For database:

step0: Install MySQL(https://dev.mysql.com/downloads/mysql/) in your local environment

step1: Initialize the database and set password **12345678** for the user **root**

step2: Open a terminal, go into the 'capstoneproject-comp3900-w18a-default' folder, run 

```
chmod +x create_db.sh
```

step3: then, run 

```
./create_db.sh
```

 and enter the password **12345678**

For Backend server:

step0: Download python 3.7 or python 3.8 in order to run the project.

step1: Open a terminal, go into the 'capstoneproject-comp3900-w18a-default' folder,  create a virtual environment by 

```
python3 -m venv env
```

step2: In the same terminal,  activate the virtual environment.

```
 source env/bin/activate
```

step3:  install all packages we need.

```
pip install -r requirement.txt
```

Step4: run the project

```
python3 app.py
```

You can deactivate the virtual environment by typing **deactivate** in the terminal.

 

The website in now running on **http://127.0.0.1:5000/ ,** please copy and paste it into your web browser to use our website.
