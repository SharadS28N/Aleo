# Aleo Voice Assistant Setup Guide

Aleo is a Python-based voice assistant project designed to run on Google Gemini. Follow this guide to set up and run Aleo.

## Project Structure
Here is a quick overview of the project files and folders:

```
|-- __pycache__      # Python cache folder (auto-generated)
|-- .venv            # Virtual environment for package management
|-- .gitignore       # Git ignore file for managing unnecessary file commits
|-- config.py        # Configuration file for setting up API keys and constants
|-- main.py          # Main script for running Aleo
|-- requirements.txt # List of required packages
```

## Prerequisites

Before starting, ensure you have the following:
- **Python 3.7+** installed on your system
- **Internet connection** (required for downloading dependencies)
- **Google Gemini API access** (if necessary for voice processing or NLP)

## Setup Instructions

1. **Clone the Repository**

   Clone this repository to your local machine or download the source code.

   ```bash
   git clone <repository_url>
   cd Aleo
   ```

2. **Set Up a Virtual Environment**

   Create a virtual environment to keep your dependencies isolated.

   ```bash
   python -m venv .venv
   ```

3. **Activate the Virtual Environment**

   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies**

   Use `requirements.txt` to install the necessary packages.

   ```bash
   pip install -r requirements.txt
   ```

5. **Configuration**

   Open `config.py` and enter any necessary API keys or constants. For example:

   ```python
   GOOGLE_GEMINI_API_KEY = "your_gemini_api_key_here"
   ```

6. **Run Aleo**

   To start the voice assistant, run `main.py`:

   ```bash
   python main.py
   ```

## Additional Notes

- **Updating Dependencies**: If new packages are added, update `requirements.txt` by running:
  
  ```bash
  pip freeze > requirements.txt
  ```

- **Deactivating the Virtual Environment**:
  
  When done, deactivate the virtual environment with:
  
  ```bash
  deactivate
  ```

## Troubleshooting

- **Module Not Found Error**: Ensure the virtual environment is activated and all packages are installed.
- **API Key Issues**: Double-check your API key in `config.py` and ensure it's correct and valid.

---

This guide should help you get started with Aleo, the voice assistant. Enjoy coding!

---
![image](https://raw.githubusercontent.com/SharadS28N/Aleo/main/aleo%202.png)
