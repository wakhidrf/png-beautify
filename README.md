# PNG Beautify

[![Python](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple Python project to beautify PNG images using **Flask** and **Pillow**.

---

## Features

- Enhance and optimize PNG images
- Simple web interface using Flask
- Lightweight and easy to run

---

## Prerequisites

Make sure you have installed:

- Python 3.x
- Git
- Fish shell (for `.fish` virtual environment activation)

---

## Setup & Installation

Follow these steps to get started:

```bash
# Clone the repository
git clone https://github.com/png-beautify.git

# Create a virtual environment
python3 -m venv png-beautify

# Enter the project folder
cd png-beautify

# Activate the virtual environment (Fish shell)
. bin/activate.fish

# Install required packages
pip install pillow flask
```

---

## Running the Application

```bash
python3 app.py
```

Open your browser and go to: `http://127.0.0.1:5000` to start beautifying your PNG images.

---

## Project Structure

```
png-beautify/
├── app.py             # Main Flask application
├── static/            # CSS, JS, and image assets
├── templates/         # HTML templates
└── README.md          # Project documentation
```

---

## Contributing

Contributions are welcome! Feel free to:

- Open issues
- Submit pull requests
- Suggest new features

---

## License

This project is licensed under the MIT License.
