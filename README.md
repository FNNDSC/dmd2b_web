# Website for dmd2b project
Advanced search tools for dmd2b project.

## Overview
Build a website for DICOM files thanks to Django

# Get started
You can access to my work by this path : /neuro/users/yves.verpillieux/DicomInfoExtraction/prg/dmd2b_web/

In the folder /dmd2b_web/polls/, the file "services.py" is a new version of "DicomInfoExtraction.py" which belongs to dmd2b project.
It extracts the values from DICOM files and then saves them in a Django database created with the models.

You will find the DICOM files in the path : ```/neuro/users/chris/data/```

# Prerequisite
Python3 needs to be installed

## Dependencies:
You need to install pydicom-0.9.9 and python3-dateutil:
```
sudo apt-get install python3-dateutil

cd pydicom-0.9.9
python setup.py install
pip install pydicom
```

# Development environment
## To add new data to DB
Edit the following lines in "services.py" to point to "dicom", "output" and "dmd2_web" project directories
```
sys.path.append("/neuro/users/.../")

os.chdir(/the/path/to/dicom/)

outputDir = (/the/path/to/output")
```

And then do : ```python3 services.py```

## Development database
To create the development database, do the followings:
```
mysql -u root -p
```

Now create a local database on MySQL's shell:
```
CREATE DATABASE dmd2b_web_db CHARACTER SET UTF8;
```
This ensures all tables and columns will use UTF-8 by default.

Next, we will create a database user which we will use to connect to and interact with the database. Set the password to something strong and secure:
```
CREATE USER user@localhost IDENTIFIED BY 'password';
```

Now, all we need to do is give our database user access rights to the database we created:
```
GRANT ALL PRIVILEGES ON dmd2b_web_db.* TO user@localhost;
```

Flush the changes so that they will be available during the current session:
```
FLUSH PRIVILEGES;
```

Then, you will need to change the database settings :
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dmd2b_web_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```
#To see the data
Connect to MySQL, then do: ```USE dmd2b_web_db;```

Finally do : ``` SELECT * FROM polls_seriesdetails;```

# To see the results on the web page
First create a system user to be able to do authenticated requests. We are going to create user "user" with password "password":
```
python manage.py createsuperuser
```
Start the Django development server:

Do : ```python manage.py runserver```

Then go to : ```127.0.0.1:8000/polls/```

## Or
Do : ```python manage.py runserver (Your IP adress):8000```

Then go to : ```(Your IP adress):8000/polls/```

# Results
Finally, you will see the webpage, then you just click on the webpage's head link to see the results in the other pages.
