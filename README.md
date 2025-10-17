
# Django search engine with custom algorithms


## Technologies 

- django
- python
- sqlite

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/tmy26/CoolBoxTest.git
cd CoolBoxTest
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. .ENV & .gitignore
usually it is DUMB(very bad practice) to add the .env file to repository, but i will add it, so it would be easier to set up. This same applies to the db.sqlite3, .gitignore files.

# THE TASK
Brief introduction to the whole app.
The task was to create search engine without using the already build in django .filters, .sort, and order. 

# General approach.
After researching the topic and evaluating different approaches like ElasticSearch, Generators and Websockets before i saw the restraint about that the whole app should be REST based, meaning it will run on the principle of request -> response and that it is manditory to implement sorting algorithm. I came to the conclusion that using inline SQL requests will definatly be the fastest and most optimazed way to achieve speed(That's how actually django's .filter, .sort functions work).

# Sorting Algos
After doing that, i had to build the sorting algorithms, i used ABC - abstractation for them. The two mentioned algos in the task were implemented ( MergeSort and QuickSort) Django actually uses timsort which is combination of MergeSort and InsertionSort, i could easly copied the algo from the internet but decided to proceed with the clean and simple merge and quicksort algorithms - The endpoint gives the opportunity to select which one to use.

# Custom CSV Parser
After all that i knew that i need to test the app with real data so i can see how it performs. For this i actually downloaded a generated data file, and created a custom .csv parser for it, so i can work with real data.

# Caching
After all the testing, i decided to cache the database, i started looking for ways to do it - Redis or in memory cache. I decided to proceed with in-memory caching, because the database isn't that big (10k records) to hit the limits. In THIS PARTICULLAR case i think this is the better solution, but it is definatly not scalable and not optimased for bigger databases.

# JSON and serializers
I have developed two serializers, one that actually returns all data from the company, and one that returns only the main data - name, country, industry and founded year. The second one is more compact and makes the responses faster, but it can't be used for testing the filtering and sorting because the data from FinancialData and CompanyDetails is actually needed to check if the everything actually works.

I thought about speeding up the whole response, and found a library called orjson. According to my research it is  5–10× faster than json.dumps, Handles datetime, UUID, etc. automatically , Produces smaller, more compact JSON. All the things i was looking for, in the end i decided to not implement it, because i may break the rule about that the responses should return pure JSON results.

### Testing of the app.
The testing was implemented using pytest. To run the tests, navigate to the root of the folder (where manage.py is located), activate your virtual enviroment and run:

I recommend using postman:

A example of a query:
url: /api/companies

And in postman a simple query like this can be send:
```bash
{
    "search input": "industry:Software OR revenue>100",
    "sort_by": "revenue",
    "sort order": "asc",
    "algorithm": "quicksort"
}
```

```bash
pytest -v
```

# Notes from the author.
The repo comes with preloaded database and with superuser :username: tmy26 and :password:0
I had the idea the preload the database when the app starts, but this could easily become a bottleneck, so i decided to not do it.

In the end of the day it was actually pretty fun experiance with a lot of new things learned. Pure pleasure.
