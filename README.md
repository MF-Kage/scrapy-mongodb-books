# Books Scraper (Scrapy + MongoDB)

A production-style web scraping project built with Scrapy that extracts structured book data and persists it to MongoDB using an idempotent upsert pipeline.

This project demonstrates backend data processing, deterministic ID generation, structured transformation, and unit-tested parsing logic.




## Overview:
The scraper collects book listings from Books to Scrape, extracting:
- Title
- Price
- Relative URL



Results are processed through a MongoDB pipeline that ensures:
- No duplicate records
- Deterministic document IDs using SHA-256 hashing
- Clean separation of scraping and persistence concerns



## Features:
- Paginated crawling
- Structured item definitions
- MongoDB upsert pipeline
- Deterministic ID hashing
- Logging configuration
- Unit tests using mocked HtmlResponse
- Clean, modular Scrapy project layout



## Tech Stack:
- Python 3
- Scrapy
- MongoDB (pymongo)
- unittest

## Project Structure:
```
books/
├── books/
│   ├── spiders/
│   ├── tests/
│   ├── items.py
│   ├── pipelines.py
│   └── settings.py
├── scrapy.cfg
├── requirements.txt
└── README.md
```


# Setup:
## Create a virtual environment and install dependencies:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Running the Spider
```bash
scrapy crawl book
```

## Export output to JSON:
```bash
scrapy crawl book -O sample_output.json
```

## Running Tests
```bash
python -m unittest discover
```



## Tests validate:
- Correct item extraction
- Accurate pagination handling
- Expected field values



## Design Notes:
- Item processing is decoupled from persistence via Scrapy pipelines.
- MongoDB upsert ensures idempotent writes.
- Document IDs are generated deterministically using SHA-256 of the URL.
- Parsing logic is unit-tested using controlled HTML fixtures.



## Future Improvements:
- Environment variable configuration for database credentials
- Expanded test coverage
- CLI-based runtime configuration
- CI integration