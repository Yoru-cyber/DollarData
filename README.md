# Dollar_Data

<p align="center">
<img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExazdjNXd3enVmN294eTRmZjdzZDF4bjJjM3ljdm9pOHNqbnUwdGZqdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bMycGOQLESDCEnLNUz/giphy.gif">
<p/>

## Project Overview

This Python project automates the process of collecting, storing, and visualizing exchange rate data from the Banco Central de Venezuela (BCV) website. It utilizes web scraping to fetch the latest Excel file containing exchange rate information, extracts relevant data, stores it in a SQLite database, and presents it through a user-friendly web interface with a not so eye-bleeding chart.

## Features

  * **Automated Data Collection:**
      * Web scraping of the BCV website to identify and download the most recent Excel file containing exchange rate data.
      * Extraction of key information from the Excel file, specifically the exchange rate (price) and corresponding dates.
  * **Data Processing and Storage:**
      * Parsing of the downloaded Excel file using `xlrd` to read and extract data.
      * Data transformation and structuring using `Pandas` DataFrames for efficient manipulation and analysis.
      * Storage of processed data in a local `SQLite` database for persistence and easy querying.
  * **Web Visualization Interface:**
      * Web server built with `Flask` to provide a dynamic and interactive user interface.
      * Data retrieval from the `SQLite` database using `SQLAlchemy` ORM for seamless database interaction.
      * Displays an exchange rate visualization chart using `ChartJS` in the frontend.
      * Focus on Dollar exchange rate data for clarity and specific analysis.
  * **Monitoring and Observability:**
      * Comprehensive application monitoring implemented with `OpenTelemetry`, `Prometheus`, `Jaeger`, `Zipkin`, and `Grafana`.
      * Metrics collection and exposure via `Prometheus` for performance monitoring.
      * Distributed tracing with `Jaeger` and `Zipkin` to track requests and diagnose performance issues.
      * Visualization of monitoring data and creation of dashboards using `Grafana`.
  * **Scheduled Tasks:**
      * Automated background tasks managed by `APScheduler` for:
          * Regularly downloading the latest Excel file from BCV and updating the database with new exchange rate data.
          * Checking for data completeness by verifying the number of records from the latest entry to the current date, ensuring data integrity.
  * **Production-Ready Deployment:**
      * Configuration for deployment with `Gunicorn` as a WSGI server for robust web application serving.
      * Designed to be deployed behind a web server like `Nginx` (preferred) or `Apache` for enhanced performance and security.
      * Containerized with `Docker` and orchestrated with `Docker Compose` for easy setup and deployment.
  * **Documentation:**
      * Automatic documentation generation using `Sphinx` based on the project's codebase.

## Technologies Used

* **Python Libraries:**
    * **Web Scraping:** `requests`, `BeautifulSoup4`
    * **Excel Processing:** `xlrd`
    * **Data Manipulation and Analysis:** `pandas`
    * **Web Framework:** `Flask`
    * **ORM:** `SQLAlchemy`
    * **Database:** `sqlite3` 
    * **Task Scheduling:** `APScheduler`
    * **Web Server (WSGI):** `gunicorn`
    * **Monitoring & Observability:** `opentelemetry-api`, `opentelemetry-sdk`, `opentelemetry-exporter-prometheus`, `opentelemetry-exporter-jaeger`, `opentelemetry-exporter-zipkin`
    * **Documentation:** `Sphinx`
    * **Dependency Management:** `poetry`
* **Frontend Technologies:**
    * **JavaScript Charting Library:** `ChartJS`
* **Monitoring Infrastructure:**
    * `Prometheus`
    * `Grafana`
    * `Jaeger`
    * `Zipkin`
* **Deployment:**
    * **Containerization:** Docker, Docker Compose
    * **Web Server (WSGI):** `gunicorn`
    * **Web Server (Production):** `Nginx` (Recommended) or `Apache`

## Installation

If you have Docker and Docker compose installed go directly to the [usage](#Usage) section.

To set up the project locally, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Yoru-cyber/DollarData/tree/main/dollar_data
    cd dollar_data
    ```

2.  **Install Poetry:**

    If you don't have Poetry installed, follow the official installation instructions: [https://python-poetry.org/docs/basic-usage/\#installation](https://www.google.com/url?sa=E&source=gmail&q=https://python-poetry.org/docs/basic-usage/#installation)

3.  **Navigate to the project directory and install dependencies using Poetry:**

    ```bash
    poetry install
    ```

    This command will create a virtual environment and install all project dependencies as defined in `pyproject.toml` and `poetry.lock`.

## Usage

1.  **Run the Flask web application:**

    If locally:

    ```bash
    python dollar_data/web/app.py
    ```
    
    Otherwise make sure you have Docker and Docker Compose installed on your system.

    Run Docker Compose to build and start the application:

    ```bash
    docker-compose up --build
    ```

    The web application will be accessible at `http://localhost:8000/`.

2.  **Access the Web Interface:**

    Open your web browser and navigate to the address shown in the previous step. You should see the interactive chart displaying the BCV exchange rate data.

3.  **Background Tasks:**

    The project is configured with `APScheduler` to automatically run background tasks:

      * **Data Update Task:**  This task periodically scrapes the BCV website, downloads the latest Excel file, and updates the database. By default, this task is scheduled to run every 24 hours.
      * **Data Integrity Check Task:** This task runs to ensure data completeness by checking for missing records and alerting if there are gaps in the data. By default, this task is scheduled to run every 24 hours.

    These tasks run automatically in the background and do not require manual intervention once the application is running.

4.  **Monitoring Dashboards:**

    To access the monitoring dashboards, ensure you have `Prometheus`, `Grafana`, `Jaeger`, and `Zipkin` set up and running.

      * **Grafana:** Access Grafana in your browser (usually at `http://localhost:3000` or as configured). 
      * **Prometheus:** Access Prometheus to see raw metrics data (usually at `http://localhost:9090` or as configured).
      * **Jaeger:** Access Jaeger UI for distributed tracing visualization (usually at `http://localhost:16686` or as configured).
      * **Zipkin:** Access Zipkin UI for distributed tracing visualization (usually at `http://localhost:9411` or as configured).

## Documentation

The project documentation is built using `Sphinx`. To build the documentation locally:

1.  **Navigate to the `docs` directory:**

    ```bash
    cd docs
    ```

2.  **Build the documentation:**

    ```bash
    make html
    ```

3.  **Access the documentation:**

    Open the `docs/build/html/index.html` file in your web browser to view the project documentation.
    
    Or you can also run. 

    ```bash
    sphinx-autobuild docs/source docs/build
    ```


## License

This project is licensed under the IDC(I don't care) License. See the `LICENSE` file for the actual license which is BSD-3.


## Note

This is currently just a toy project and aims not to be for a professional project.

That's all.

<p align="center">
<img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWxxYnhrYTd3MWc3cXR5NGVxeXM4bGdlc2IxN2FoazJ4cDA2b2Y0cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/onOWJOc7U5GAE/giphy.gif">
<p/>

