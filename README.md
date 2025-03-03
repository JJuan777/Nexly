# 🚀 Nexly - Social Network

![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite3-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![AJAX](https://img.shields.io/badge/AJAX-Enabled-orange.svg)

## 📌 Description
**Nexly** is a social network built as a practice project using **Django 5.0.6** and **SQLite3**. It includes features such as authentication, user posts, profiles, messaging, stories, comment interactions, post sharing, media uploads, and friend requests. The frontend is styled with **Bootstrap v5.3**, and AJAX is used for dynamic interactions.

## 🎯 Features
✅ **User Authentication** (Login, Registration, Logout).<br>
✅ **Create and Manage Posts** (Text, Images, Videos).<br>
✅ **User Profiles** (Profile Pictures, Bios, Personal Information).<br>
✅ **Messaging System** (Private Messages Between Users).<br>
✅ **Stories Feature** (Temporary Posts Visible to Friends).<br>
✅ **Comment Interactions** (Likes, Replies, AJAX Integration).<br>
✅ **Share Posts** (Reposting and Sharing With Friends).<br>
✅ **Friend Requests** (Send, Accept, Decline Requests).<br>
✅ **AJAX-Powered UI** (Seamless Dynamic Interactions).<br>
✅ **Bootstrap 5.3 Styling** (Responsive and Modern UI).<br>

## 🏗️ Project Structure
```
Nexly/              # Main Django App
SocialNetwork/      # Django Project Settings and Configuration
media/              # User-Uploaded Images and Videos
static/             # CSS, JavaScript, and Other Static Files
templates/          # HTML Templates for Rendering Pages
db.sqlite3          # SQLite Database File
```

## 🔑 Admin Panel Access
To access the Django **admin panel**, go to:
```
http://127.0.0.1:8000/admin/
```
**Admin Credentials:**  
✉️ Email: `juanbalderramasan@gmail.com`  
🔑 Password: `Carnada01`

## 🛠️ How to Clone and Run
1. **Clone the repository**
   ```sh
   git clone https://github.com/JJuan777/Nexly.git
   cd Nexly
   ```
2. **Create a Virtual Environment** (Recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```
3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run Database Migrations**
   ```sh
   python manage.py migrate
   ```
5. **Start the Django Development Server**
   ```sh
   python manage.py runserver
   ```
6. **Open the Application in Browser**
   ```
   http://127.0.0.1:8000/
   ```

## 📧 Contact
For any questions or suggestions, visit my profile on **[GitHub](https://github.com/JJuan777)**.

---
**© 2025 - Nexly Social Network** 🚀
