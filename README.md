# Django Forum

Django Forum is a simple project that I created to practice the Django Web Framework.

## Features
- Ready Bootstrap-themed pages
- User Sign up/Log in
- Gravatars

## Installation

1. Install **Python 3.6, 3.7, 3.8** or **3.9**: [link](https://www.python.org/downloads/)
2. Clone the repository:
   ```git
   git clone https://github.com/axinterop/ForumDjango.git
   ```
3. Create and active the virtual enviroment.
4. Install all the dependencies from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
5. Migrate:
   ```bash
   py manage.py migrate
   ```

### Database auto-population (optional)
If you want to look at a project with a populated database, follow these steps:

6. Install additional packages:
   ```bash
   pip install lorem nickname-generator
   ```
7. Run the script (highly recommended to use only for populating an **empty** DB):
   ```bash
   py populate_db.py
   ```
   All information related to the script **will be written to the console** after it is finished.
8. Run the server:
   ```bash
   py manage.py runserver
   ```
In case if you want to empty the database, enter the next command:
```bash
py manage.py flush --noinput
```