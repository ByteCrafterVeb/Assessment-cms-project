# Assessment-cms-project
Content Management System (CMS) using Python DjangoREST framework 

### Prerequisites
- Python 3.x
- Node.js and npm
- MySQL




# Here's how to begin with this project 
1. Installing Django and DjangoRESTframework
    create and activate virtual environment :
    ```command promt(cmd)
    python -m venv myenv
    source myenv/bin/activte   #On Windows: myenv\Scripts\activate
    ```
    Installing Django and DjangoREST framework
   ```cmd
   pip install django djangorestframework djangorestframework-simplejwt mysqlclient
   ```
2. Create new Django project and app:
  ```cmd
  django-admin startproject cms_project
  cd cms_project
  django-admin startapp cms
  ```
3. Configure MySQL database
   Edit 'cms_project/settings.py'
4. define Models
   Edit 'cms/models.py' to define User, Profile, Content, and Category
5. Create Serializers
   Edit 'cms/serializers.py'
6. Setup Views and URLs
   'cms/views.py' and 'cms/urls.py'
7. JWTAuthentication
   'cms_project/settings.py'
8. Migrations
    ```cmd
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
9. Test APIs using Postman API

# Here's how to clone and use it 
1. Installation
    ```cmd
    git clone https://ByteCrafterVeb/Assessment-cms-project
    cd cms_project
    ```
    
2. Backend Setup
   ```cmd
   python -m venv myenv
   myenv\Scripts\activate
   ```
   ```cmd
   pip install -r requirements.txt
   ```
   ```cmd
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```
4. API Endpoints


Additional Notes
This project uses MySQL as the database. Make sure MySQL server is installed and running before setup.



