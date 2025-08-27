# Hotel Reservation System

A Django-based hotel room booking system with MySQL database support.

---

## 🚀 Features
- User authentication (Login/Register)
- Hotel/Room listing
- Room booking
- Admin dashboard for managing bookings

---

## 🛠️ Tech Stack
- Django (Python web framework)
- MySQL (Database)
- Crispy Forms + Bootstrap 5 (Frontend)
- PythonAnywhere (Deployment)

---

## 📦 Installation (Local Setup)

Follow these steps to set up the project locally:

### 1️⃣ Clone the Repository
bash
git clone https://github.com/your-username/hotel-reservation.git
cd hotel-reservation
2️⃣ Create a Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Configure MySQL Database
Make sure MySQL is running and create a database:

sql
Copy code
CREATE DATABASE hotel_reservation;
Update settings.py with your database credentials:

python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hotel_reservation',
        'USER': 'root',          # your MySQL username
        'PASSWORD': 'yourpassword',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
5️⃣ Apply Migrations
bash
Copy code
python manage.py migrate
6️⃣ Create Superuser (Admin)
bash
Copy code
python manage.py createsuperuser
Enter username, email, and password.

7️⃣ Run Development Server
bash
Copy code
python manage.py runserver
Now open http://127.0.0.1:8000/ in your browser.

🖥️ Access Admin Panel
Go to:

http://127.0.0.1:8000/admin/
Log in with the superuser credentials you created.
Copy code
http://127.0.0.1:8000/admin/
Log in with the superuser credentials you created.
