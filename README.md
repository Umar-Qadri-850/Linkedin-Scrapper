🔎 LinkedIn Keyword Posts Scraper API

A FastAPI-based backend that fetches and filters public LinkedIn posts using the ScrapeCreators API.
You provide a keyword, and the API returns relevant LinkedIn posts with pagination, filtering, and clean structured output.

🚀 Features
🔍 Search LinkedIn posts by keyword
📄 Pagination support using cursor
🎯 Keyword-based filtering of post content
⚡ Async API calls using httpx
🛡️ Error handling for API/network failures
📦 Clean JSON response structure
🔐 Secure API key via environment variables
📦 Tech Stack
Python 3.10+
FastAPI
httpx (async HTTP client)
python-dotenv

⚙️ Installation
1. Clone the repository
git clone https://github.com/Umar-Qadri-850/linkedin-scraper-api.git
cd linkedin-scraper-api
  # Windows
3. Install dependencies
pip install fastapi uvicorn httpx python-dotenv 

▶️ Run the Server
uvicorn main:app --reload

Server will run at:

http://127.0.0.1:8000/docs
