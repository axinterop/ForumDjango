# Django Forum

Django Forum is a simple project that I created to practice the Django Web Framework.

## Features
- Ready Bootstrap-themed pages
- User password reset
- User Sign up/Log in
- Gravatars

## Installation

1. Install **Python 3.6, 3.7, 3.8** or **3.9**: [link](https://www.python.org/downloads/)
2. Clone the repository:
   ```git
   git clone https://github.com/axinterop/ForumDjango.git
   ```
3. Create and activate the virtual enviroment.
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

## Screenshots
### Home page
![127 0 0 1_8000_](https://user-images.githubusercontent.com/40664776/135628988-c034c30a-7320-4fd9-bcf2-ef347bb6b139.png)
---
### Topics
![127 0 0 1_8000_boards_1_](https://user-images.githubusercontent.com/40664776/135629035-b0334590-90da-4802-aec6-9887ecf765ca.png)
---
### Posts
![127 0 0 1_8000_boards_1_topics_1](https://user-images.githubusercontent.com/40664776/135631760-ee020fe5-7cce-4fd9-961a-b03d27a2726f.png)
---
### Log in
![127 0 0 1_8000_login_](https://user-images.githubusercontent.com/40664776/135629067-c2704300-fa15-44c2-ae1e-1ccee77969ff.png)
---
### Password reset
![127 0 0 1_8000_reset_](https://user-images.githubusercontent.com/40664776/135629072-d52e5dd4-9c5b-4a66-a2ad-6a191c887317.png)

