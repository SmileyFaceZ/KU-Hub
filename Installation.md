# 🚀 Run and Install

### Steps to install and run the project.
#### [Step 1](#step-1-Setup-the-environment): Setup the environment
#### [Step 2](#step-2-clone-the-repository-1): Clone the Repository
- [Step 2.1](#Django-Configuration): Django Configuration
- [Step 2.2](#Neon-Configuration): Neon Configuration
- [Step 2.3](#Google-OAuth-Configuration): Google OAuth Configuration
#### [Step 3](#step-3-install-the-required-modules-1) Install the Required Modules
#### [Step 4](#step-4-database-migrations-1): Database Migrations
#### [Step 5](#step-5-run-server-1): Run Server

---

## Step 1: Setup the Environment

### Get Environment Variables
Get the environment variables from the project owner and put it in the `.env` file.

#### Django Configuration

| Variable                               | Description                                                                        |
|:---------------------------------------|------------------------------------------------------------------------------------|
| `SECRET_KEY`                           | Used for cryptographic signing [Generate Secret Key](https://djecrety.ir/)         |
| `DEBUG`                                | Set `True` for development, `False` for actual use                                 |
| `ALLOWED_HOSTS`                        | List of strings representing the host/domain names that this Django site can serve |
| `TIME_ZONE`                            | Time zone for this installation                                                    |

#### Neon Configuration

To get neon database url follow these steps.
1. Go to [NEON](https://neon.tech/) (Read [Documentation](https://neon.tech/docs/introduction))
2. Create a new project
3. Create a Database
4. Go to Dashboard and copy psql url and put it in .env file in the root directory of the project

| Variable                               | Description                |
|:---------------------------------------|----------------------------|
| `DATABASE_URL`                         | Postgres Database NEON url |

#### Google OAuth Configuration
To get google oauth client id and secret key follow these steps.
1. Go to [Google Cloud Platform](https://console.cloud.google.com/)
2. Create a new project
3. Go to Credentials (On the left side bar under APIs & Services)
4. Create Credentials
5. Select OAuth Client ID
6. Select Web Application
7. Put your credentials in .env file in the root directory of the project
8. Go to OAuth consent screen
9. Add your domain to Authorized domains
10. Add your email to Test users

| Variable                               | Description                                                                        |
|:---------------------------------------|------------------------------------------------------------------------------------|
| `GOOGLE_OAUTH_CLIENT_ID`               | Google OAuth Client ID                                                             |
| `GOOGLE_OAUTH_SECRET_KEY`              | Google OAuth Secret Key                                                            |

#### Firebase Configuration 🛠️
To get firebase private key follow these steps.
1. Go to [Firebase Website](https://console.firebase.google.com/)
2. Select your project
3. Go to Project Settings
4. Go to Service Accounts
5. Click Generate New Private Key
6. Put your credentials in .env file in the root directory of the project

| Variable                               | Description                                                                        |
|:---------------------------------------|------------------------------------------------------------------------------------|
| `FIREBASE_TYPE`                        | Firebase Type                                                                      |
| `FIREBASE_PROJECT_ID`                  | Firebase Project ID                                                                |
| `FIREBASE_PRIVATE_KEY_ID`              | Firebase Private Key ID                                                            |
| `FIREBASE_PRIVATE_KEY`                 | Firebase Private Key                                                               |
| `FIREBASE_CLIENT_EMAIL`                | Firebase Client Email                                                              |
| `FIREBASE_CLIENT_ID`                   | Firebase Client ID                                                                 |
| `FIREBASE_AUTH_URI`                    | OAuth2 URI                                                                         |
| `FIREBASE_TOKEN_URI`                   | OAuth2 Token URI with Firebase Project ID                                          |
| `FIREBASE_AUTH_PROVIDER_X509_CERT_URL` | Firebase Auth Provider X509 Cert URL                                               |
| `FIREBASE_CLIENT_X509_CERT_URL`        | Firebase Client X509 Cert URL                                                      |
| `FIREBASE_UNIVERSE_DOMAIN`             | Firebase Universe Domain                                                           |

### Create a virtual environment and activate it
To create a virtual environment, run the following command:

```commandline
python -m venv venv
```

To activate the virtual environment, use one of the following commands:

Windows
```commandline
venv\Scripts\activate
```

macOS / Linux:
```commandline
source venv/bin/activate
```
---

## Step 2: Clone the repository
Clone the repository and using this command on terminal:
```commandline
git clone https://github.com/SmileyFaceZ/ku-polls.git
```
---

## Step 3: Install the required modules

Installing the required `Python` modules by executing the following command:
```commandline
pip install -r requirements.txt
```

---

To verify that all modules are installed, run the following command:
```commandline
pip list
```

---

## Step 4: Database migrations

To create a new database, run the following command:
```commandline
python manage.py migrate
```
---

## Step 5: Run server

Launch the server, running the following command:
```commandline
python manage.py runserver
```
