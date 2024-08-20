
# CRD-Controller

Welcome to the CRD-Controller project! This repository contains code for a Django web application and Raspberry Pi scripts to facilitate two-way communication between AWS, a Raspberry Pi, and an ESP32 microcontroller. This project is designed to manage and control remote devices through a web interface, leveraging the power of AWS services for robust and scalable communication.

## Table of Contents

- [Introduction](#introduction)
- [Architecture](#architecture)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

CRD-Controller is a comprehensive solution for remote device management. It integrates a Django-based web application for user interaction, a Raspberry Pi for on-site control, and an ESP32 microcontroller for device communication. The system utilizes AWS EC2 for hosting and MQTT for message brokering.

## Architecture

![image](https://github.com/annjan777/CRD-Controller/assets/133907685/a354c934-b727-4d73-ad36-33717e910866)


1. **Django Web Application**: Provides a user-friendly interface to monitor and control devices.
2. **Raspberry Pi**: Acts as a bridge between the web application and ESP32, handling data transmission.
3. **ESP32**: Connected devices that receive commands and send back data.
4. **AWS EC2**: Hosts the Django application and MQTT broker for reliable communication.

## Features

- Real-time device monitoring and control
- Two-way communication between Raspberry Pi, ESP32, and AWS
- Secure and scalable architecture
- User-friendly web interface
- User authentication and authorization (admin and regular user roles)
- View logs and debug information

## Technologies Used

- Python 3.7
- Django 3.1.2
- SQLite
- Bootstrap 5
- jQuery
- AWS EC2
- AWS IoT
- Mosquitto MQTT broker
- NodeRed
- Paho-MQTT

## Installation

### Prerequisites

- AWS Account
- Raspberry Pi with Raspbian OS
- ESP32 microcontroller
- Python 3.8+
- Django
- Mosquitto MQTT broker
- NodeRed
- Paho-MQTT
- AWS IoT
- AWS EC2 Instance

### Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/CRD-Controller.git
cd CRD-Controller
```

#### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scriptsctivate`
```

#### 3. Install the Required Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

#### 6. Run the Development Server

```bash
python manage.py runserver
```

#### 7. Access the Application

Open your web browser and navigate to `http://127.0.0.1:8000/`

## Usage

1. **Login:**
   - Admin users can log in at `http://127.0.0.1:8000/admin/`
   - Regular users can log in at `http://127.0.0.1:8000/user_login/`

2. **Admin Dashboard:**
   Admin users have access to the admin dashboard where they can manage users, view logs, and perform other administrative tasks.

3. **User Dashboard:**
   Regular users can view and update the status of the CRD system from the user dashboard.

4. **Status and Update:**
   - View the current status of various CRD parameters.
   - Update parameters as needed.

5. **Logs:**
   - View system logs to monitor activities and troubleshoot issues.

6. **Debug:**
   - Access debugging tools to diagnose and fix problems with the CRD system.

## Configuration

Ensure that you properly configure your AWS services and Raspberry Pi scripts to enable smooth communication between the web application, Raspberry Pi, and ESP32. Refer to the provided scripts and documentation within the repository for detailed setup instructions.

## Project Structure

```
CRD-Controller/
│
├── iot_app/
│   ├── migrations/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── images/
│   │       └── logo.jpg
│   ├── templates/
│   │   └── base.html
│   │   └── home.html
│   │   └── status_update.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── CRD-Controller/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
