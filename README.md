# AI-Powered News Newsletter

This is a Python script that fetches the top 5 technology headlines from the [NewsAPI](https://newsapi.org) and automatically sends them as a professionally formatted HTML email using a Gmail account.

## Features

* **Fetches Top News:** Grabs the 5 most recent top technology headlines from the US.
* **Professional HTML Formatting:** Generates a clean, readable HTML email with styled headers, article summaries, and clickable links.
* **Secure Credentials:** Uses a `.env` file to keep your API keys and email passwords safe and out of the script.
* **Gmail SMTP Integration:** Sends email using Google's SMTP server with a secure `starttls` connection.

## Setup & Installation

Follow these steps to get the script running.

### 1. Install Dependencies

You need two Python libraries for this script to work. You can install them using pip:

```bash
pip install python-dotenv requests
