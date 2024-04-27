
# CiteFair

  

CiteFair is a tool designed to detect potential gender and race biases from citations. By analysing the authors of scholarly articles through automated requests to CrossRef and NamSor APIs, CiteFair aims to highlight disparities in citation practices that could influence academic and professional recognition.

  

## Features

  

- Fetches author data from CrossRef using DOI.

- Determines the likely gender and race/ethnicity of the authors using NamSor API.

- Analyzes potential biases based on gender and race.

- Provides a simple interface for querying by DOI and displays bias analysis results.

  

## Prerequisites

  

Before you begin, ensure you have the following:

- Python 3.6 or higher

-  `requests` library installed

  

## Installation

  

Clone the repository to your local machine:

```bash
git  clone  https://github.com/yourusername/CiteFair.git

cd  CiteFair
```
Install the required libraries:

```bash
pip install requests
```
## Usage
Run the script from the command line:

```bash
python main.py
```
Enter the DOI when prompted to receive the bias analysis for the given DOI.

## API Keys
You will need to obtain an API key from [Namsor](https://namsor.app/).
Replace `api_key_here` in the code with your actual NamSor API key.
You will also need API keys from [genderize.io](https://genderize.io/) and [nationalize.io](https://nationalize.io/) if you plan on doing your own data collection.
