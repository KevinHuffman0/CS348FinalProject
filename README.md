# CS348FinalProject
# Music Manager Interactive Database
Allows users to add/edit/delete bands and associated albums.
Based on these added band and albums, user can view reports that sort the database, and can see interesting info about the inputted data.

# Project Requirements
This project was created as a final project in my information systems class.
The app was a way to practice relational database modeling, indexing, transactions and concurrency, etc.
The project required a way for users to add information to a database, and see reports based on the data in the database.

# Tools
This project was made in Python with Flask, SQLAlchemy and SQLite.

# Files
app.py -> Main file to run program. You can see the different routes for the project features.  
database.py -> Create the database and indexes.  
models.py -> See the actual schema of the database. Uses object relational mapping.  
index.html -> Visual elements of application for the add/edit/delete page (user can add/edit/delete bands and albums)  
reports.html -> Visual elements of application for the reports page (where user can sort database)  
aggregation.html -> Visual elements of app for aggregation page (see # bands per country, albums per band)   
