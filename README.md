## Site Link Keyword Dashboard

This project extracts links from a website and then uses an LLM to extract keywords and keyword scores. 
It includes features to set a score for each link and to view them through a Web UI.


## Features

- **Link Data Collection**: Collects links (A tags) from websites by setting specific conditions.
- **Keyword Extraction**: Passes link titles to an LLM to get important keywords and their corresponding scores.
- **Link Scoring**: Sets an individual score for each link based on the keyword scores.
- **Web UI**: A web application that allows you to check collected links and keywords by date.


## Getting Started

### 1\. Prerequisites

- Python 3.12+

### 2\. Installation

Clone the repository and install the required Python packages.

Bash

```
pip install -r requirements.txt
```

### 3\. Environment Configuration

#### Sqlite

Specify the name of the SQLite file to use in the `SITE_LINK_SQLITE` environment variable. If not specified, a file named *site\_link.db* will be created in the current directory.

#### ollama

To use ollama, change `enable: false` to `enable: true` in the ollama configuration section of `config/llm_config.yaml` and set the desired `model` name.

#### gemini

To use gemini, you must set the `GEMINI_API_KEY` environment variable with your *API\_KEY*, and then change `enable: false` to `enable: true` in the gemini configuration section of `config/llm_conf.yaml` and set the desired `model` name.


### 4\. Running the Application

#### Run the Collector

```
python run_all_collector.py
```

#### Run the UI

To start the development server, run `app.py`:

Bash

```
python app.py
```

The application will be accessible at `http://127.0.0.1:5000`.