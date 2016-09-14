# Website for dmd2b project
Advanced search tools for dmd2b project.

## Overview
Build a website for DICOM files thanks to Django

# Get started
You can access to my work by this path : /neuro/users/yves.verpillieux/DicomInfoExtraction/prg/dmd2b_web/

In the folder /dmd2b_web/polls/, the file "services.py" is a new version of "DicomInfoExtraction.py" which belongs to dmd2b project.
It extracts the values from DICOM files and then saves them in a Django database created with the models.

# To run "services" program
Go to /dmd2b_web/polls/ :

WARNING : Edit the following lines in services.py to point to "dicom" and "output" directories
```
os.chdir(/the/path/to/dicom/)

outputDir = (/the/path/to/output")
```

And then do : ```python3 services.py```

# Development database
To create the development database, do the followings:
```
mysql -u root -p
```

Now create a local database on MySQL's shell:
```
CREATE DATABASE dmd2b_web_db CHARACTER SET utf8;
```

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
        'USER': 'isen',
        'PASSWORD': 'yves',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

# To see the results on the web page
Go to 127.0.0.1:8000/polls/
And then, you just click on the webpage header to see the results in the other pages.
