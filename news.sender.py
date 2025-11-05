import os
import smtplib
import requests
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables from .env file
load_dotenv()

# --- 1. EMAIL CONFIGURATION & FUNCTION ---
# Get email credentials from .env file
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_newsletter(articles_list):
    """
    Connects to Gmail and sends the news articles as a formatted HTML email.
    """
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not RECEIVER_EMAIL:
        print("Email credentials (EMAIL_ADDRESS, EMAIL_PASSWORD, RECEIVER_EMAIL) are not set in .env file.")
        return
        
    print("Connecting to email server...")
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "Your AI-Powered News Summary"
    
    # --- START OF HTML BODY ---
    # Build the email body as an HTML string
    
    html_body = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 90%;
                max-width: 600px;
                margin: 20px auto;
                border: 1px solid #ddd;
                border-radius: 8px;
                overflow: hidden;
            }
            .header {
                background-color: #f4f4f4;
                color: #333;
                padding: 20px;
                text-align: center;
                border-bottom: 1px solid #ddd;
            }
            h1 {
                margin: 0;
                font-size: 24px;
            }
            .article {
                padding: 20px;
                border-bottom: 1px solid #eee;
            }
            .article:last-child {
                border-bottom: none;
            }
            h2 {
                font-size: 20px;
                margin-top: 0;
            }
            h2 a {
                text-decoration: none;
                color: #0056b3;
            }
            h2 a:hover {
                text-decoration: underline;
            }
            p {
                font-size: 16px;
                color: #555;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your AI-Powered News Summary</h1>
            </div>
    """
    
    # Loop through articles and add them to the HTML body
    # The 'summary' here is the raw 'content' from the API
    for i, (title, url, summary) in enumerate(articles_list, 1):
        html_body += f"""
            <div class="article">
                <h2><a href="{url}" target="_blank">{i}. {title}</a></h2>
                <p>{summary}</p>
            </div>
        """
        
    # Close the HTML tags
    html_body += """
        </div>
    </body>
    </html>
    """
    # --- END OF HTML BODY ---

    # Attach the HTML body to the email
    # We specify 'html' as the subtype so email clients render it
    msg.attach(MIMEText(html_body, 'html'))

    try:
        # Use smtplib.SMTP (not SSL) with port 587
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to secure
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        print("HINT: Make sure you are using a Google 'App Password' if you have 2FA enabled.")

# --- 2. NEWS FETCHING ---

# Get NewsAPI key from .env file
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news():
    """
    Uses the NewsAPI key to fetch top U.S. technology news.
    """
    if not NEWS_API_KEY:
        print("NEWS_API_KEY is not set in .env file.")
        return []
        
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',
        'category': 'technology',
        'pageSize': 5,
        'apiKey': NEWS_API_KEY
    }
    
    print("Fetching news from NewsAPI...")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Failed to fetch news: {response.status_code} {response.text}")
        return []
        
    articles = response.json().get('articles', [])
    
    formatted_articles = []
    for article in articles:
        # Get content, default to 'No content available' if null
        content = article.get('content', 'No content available')
        if not content:
            content = 'No content available'
            
        formatted_articles.append((article['title'], article['url'], content))
        
    print(f"Fetched {len(formatted_articles)} articles.")
    return formatted_articles

# --- 3. MAIN EXECUTION ---

if __name__ == "__main__":
    news_articles_list = fetch_news()
    
    if news_articles_list:
        # NOTE: This now sends the raw 'content' from the API.
        print("Sending email...")
        send_newsletter(news_articles_list)
    else:
        print("No articles found, email not sent.")
