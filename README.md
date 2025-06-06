# Enigma Machine

A Django-based web application that simulates the historical Enigma machine encryption system. This project provides an interactive interface for encrypting and decrypting messages using the principles of the famous World War II-era encryption device.

## Features

- Interactive web interface for encryption/decryption
- Historical Enigma machine simulation
- Message encryption and decryption capabilities
- User-friendly Django-based interface
- Secure message handling

## Tech Stack

- Python 3.x
- Django 4.2.21
- Django Widget Tweaks 1.5.0
- SQLite Database

## Installation

1. Clone the repository:
```bash
git clone https://github.com/artem-commits/enigma-machine.git
cd enigma-machine
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Project Structure

- `core/` - Core application components
- `encrypting/` - Encryption-related functionality
- `manage.py` - Django management script
- `requirements.txt` - Project dependencies
## Usage

1. Access the web interface through your browser
2. Enter your message in the input field
3. Configure encryption settings (if applicable)
4. Click encrypt/decrypt to process your message
5. View the encrypted/decrypted result

## Author

- Artem Commits - [GitHub Profile](https://github.com/artem-commits)
