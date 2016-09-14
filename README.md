# Website for dmd2b project
Advanced search tools for dmd2b project.

## Overview
Build a website for DICOM files thanks to Django

# Get started
You can access to my work by this path : /neuro/users/yves.verpillieux/DicomInfoExtraction/prg/dmd2b_web/

In the folder /dmd2b_web/polls/, the file "services.py" is a new version of "DicomInfoExtraction.py" which belongs to dmd2b project.
It extracts the values from DICOM files and then saves them in a Django database created with the models.

# Development environment
## To run "services" program
Go to /dmd2b_web/polls/ :

WARNING : Edit the following lines in services.py to point to "dicom" and "output" directories
```
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
## Dependencies:
```
sudo apt-get install python3-dateutil
sudo apt-get install pydicom
```

# To see the results on the web page
Go to /dmd2b_web/

Then do : ```python manage.py runserver```

Then go to : ```127.0.0.1:8000/polls/```
## Or
Go to /dmd2b_web/

Then do : ```python manage.py runserver (Your IP adress):8000```

Then go to : ```(Your IP adress):8000/polls/```

# Results
Finally, you will see the webpage, then you just click on the webpage's head link to see the results in the other pages.
