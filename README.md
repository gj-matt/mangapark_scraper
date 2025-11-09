# Mangapark Scraper

Scrape the latest chapters and save them as a .csv file.

## Requirements
- Python 3.8+
- pandas
- requests
- beautifulsoup4

Install required packages:
pip install pandas requests beautifulsoup4

## Installation
1. Clone the repository:
git clone https://github.com/gj-matt/mangapark_scraper.git
cd mangapark_scraper

2. (Optional) Create and activate a virtual environment:
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

3. Install dependencies:
If the repo has requirements.txt:
pip install -r requirements.txt
Otherwise:
pip install pandas requests beautifulsoup4

## Usage
- Scrape the latest chapters:
python mangapark.py latest

This creates a CSV file named like:
scraped_manga-YYYY-MM-DD HH:MM:SS.csv

- Search for a manga and save results:
python mangapark.py search "manga name"

This creates a CSV file named like:
searched_manga-YYYY-MM-DD HH:MM:SS.csv

CSV columns:
- title
- url
- chapter_url
- latest_chapter
- cover
- id

Run these commands from the repository directory or provide the full path to mangapark.py.
