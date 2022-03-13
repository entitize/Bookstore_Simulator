# Bookstore

Setup Instructions

Generate initial data
Our data comes from a custom random data generator under `generate_data.py`
Data is written to `./data` on the user's machine

Generate initial data
```
mkdir data
python3 generate_data.py
```

Users can add their own data by interacting with the command line app

Run the following commands in mysql command line
```
CREATE SCHEMA `cs121_final_project`;
USE cs121_final_project;
source setup.sql;
source load-data.sql;
source setup-routines.sql;
source setup-passwords.sql;
source grant-permissions.sql
```

Running the app
Run `python3 app.py`