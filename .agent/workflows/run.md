---
description: How to start the UniFlow LMS application
---

To start the application, follow these steps in your terminal:

0. **Ensure Pip is Installed** (Only if `pip` is missing):
   ```bash
   python -m ensurepip --default-pip
   python -m pip install --upgrade pip
   ```

1. **Set Up Virtual Environment**:
   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   venv\Scripts\activate
   ```

1. **Install Dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Initialize the Database**:
   ```bash
   python manage.py makemigrations core
   python manage.py migrate
   ```

2. **Create a Lecturer/Admin Account**:
   ```bash
   python manage.py createsuperuser
   ```
   *Note: After creating the user, log in to the admin panel at `/admin/` to manage group assignments and content.*

3. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

4. **Access the Dashboards**:
   - Student Portal: [http://127.0.0.1:8000/portal/](http://127.0.0.1:8000/portal/)
   - Staff Portal: [http://127.0.0.1:8000/staff/](http://127.0.0.1:8000/staff/)
   - Admin Panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

// turbo
5. **(Optional) Run Verification Tests**:
   ```bash
   python manage.py test core
   ```
