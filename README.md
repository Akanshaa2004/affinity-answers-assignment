# Affinity Answers — Full Stack Engineer Internship Assignment

A complete solution to the three-part technical assignment for the **Affinity Answers Full Stack Engineer Internship**.

This repository contains implementations covering **Python web scraping, SQL database querying, and Unix shell scripting**.

---

## 📌 Project Overview

The assignment consists of three independent technical tasks:

| Question | Technology | Objective |
|----------|------------|-----------|
| Question 1 | Python | Scrape and extract product information from MDComputers |
| Question 2 | SQL / MySQL | Execute analytical queries against the public Rfam database |
| Question 3 | Bash / Gawk | Download and process S&P 500 company data |

The project demonstrates practical knowledge of:

- Python programming
- Web scraping and HTML parsing
- Data processing
- SQL and relational databases
- MySQL command-line tools
- Bash shell scripting
- CSV processing
- Command-line utilities
- Error handling
- Data output in JSON and CSV formats

---

# 📂 Project Structure

```text
affinity-answers-assignment/
│
├── question1/
│   ├── main.py
│   ├── models.py
│   ├── parser.py
│   ├── scraper.py
│   ├── utils.py
│   ├── README.md
│   │
│   └── sample_data/
│       ├── sample_search_results.html
│       ├── sample_output.csv
│       └── sample_output.json
│
├── question2/
│   ├── answers.sql
│   └── README.md
│
├── question3/
│   ├── company_parser.sh
│   ├── README.md
│   └── sample_output.txt
│
├── requirements.txt
├── .gitignore
└── README.md

🐍 Question 1 — Python Web Scraping
Objective

The first task implements a Python-based product scraper.

The program accepts a search term and extracts product information from the provided search-result HTML.

The scraper extracts:

Product name
Product price
Product URL

The application supports both sample HTML input and a live search workflow.

Technologies Used
Python
Requests
Cloudscraper
BeautifulSoup
Pandas
JSON
CSV
Project Components
main.py

Acts as the main entry point of the application.

It handles command-line arguments and controls the overall scraping workflow.

scraper.py

Responsible for obtaining the search-result HTML.

It supports HTTP requests and Cloudflare-aware requests where required.

parser.py

Responsible for parsing the HTML and extracting the required product information.

models.py

Contains the data model used to represent product information.

utils.py

Contains supporting utility functionality used by the application.

Running Question 1

Navigate to the Question 1 directory:

cd question1
Using the provided sample HTML

The recommended way to test the project is:

python main.py --input-file sample_data/sample_search_results.html "external hard drive"

The program displays the extracted products in the terminal.

Example:

1. Product Name
   Price : Rs. ...
   URL   : https://...

2. Product Name
   Price : Rs. ...
   URL   : https://...

The program also saves the extracted results as:

output/products.json
output/products.csv
Live Search

The program can also be executed with a search term directly:

python main.py "external hard drive"

The search term can be changed according to the required product search.

Python Concepts Demonstrated
Command-line arguments
Functions and modules
HTTP requests
HTML parsing
Web scraping
CSS selectors
Data extraction
Data modelling
Exception handling
JSON serialization
CSV generation
File handling

Question 2 — SQL & MySQL
Objective

The second task contains SQL queries designed to run against the public Rfam MySQL database.

The queries retrieve and analyze biological sequence and taxonomy information from the Rfam database.

Database

Rfam

The queries are executed against the public Rfam MySQL server.

Connection details used by the assignment:

Host: mysql-rfam-public.ebi.ac.uk
Port: 4497
User: rfamro
Database: Rfam
SQL Concepts Demonstrated

The solution makes use of common SQL concepts including:

SELECT
FROM
WHERE
JOIN
GROUP BY
HAVING
ORDER BY
COUNT()
MAX()
LIMIT
OFFSET

These concepts are used to filter, join, aggregate, sort and paginate database results.

Running Question 2

Navigate to the Question 2 directory:

cd question2

The SQL queries are stored in:

answers.sql
MySQL command

The SQL file can be executed using:

mysql -h mysql-rfam-public.ebi.ac.uk -P 4497 -u rfamro -D Rfam < answers.sql

On Windows PowerShell, the following command can be used when MySQL is not configured in the system PATH:

Get-Content .\answers.sql | & "C:\Program Files\MySQL\MySQL Server 26.7\bin\mysql.exe" -h mysql-rfam-public.ebi.ac.uk -P 4497 -u rfamro -D Rfam

The query results are displayed directly in the terminal.

Example Output

Example results include information such as:

acacia_species_count
326

and sequence information such as:

species
rfamseq_acc
length

The remaining queries return the database information required by the assignment.

Question 3 — Unix Shell Scripting
Objective

The third task implements a shell script that downloads and processes an S&P 500 company dataset.

The script extracts:

Company name
Headquarters location
Founding year

and sorts the results by founding year from oldest to newest.

Technologies Used
Bash
curl
gawk
sort
How the Script Works

The script follows this pipeline:

CSV URL
   │
   ▼
  curl
   │
   ▼
Download CSV data
   │
   ▼
  gawk
   │
   ▼
Extract required columns
   │
   ▼
 sort
   │
   ▼
Terminal Output
Processing Steps
1. Accept CSV URL

The script accepts the CSV URL as a command-line argument.

2. Download data

curl downloads the CSV data and streams it to the next stage.

3. Parse CSV

gawk is used to correctly process CSV fields.

The script uses FPAT so that quoted fields containing commas are treated as a single field.

4. Extract required fields

The script extracts:

Company Name
Headquarters Location
Founded Year
5. Handle founding years

Some records contain values such as:

2013 (1888)

The script extracts the first four-digit year for sorting.

6. Sort results

The final data is sorted numerically by founding year.

Running Question 3

Navigate to the Question 3 directory:

cd question3

Make the script executable:

chmod +x company_parser.sh

Run the script:

./company_parser.sh "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"
Example Output
Company Name              Location                    Founded Year
BNY Mellon                New York City, New York    1784
State Street Corporation  Boston, Massachusetts      1792
Colgate-Palmolive         New York City, New York    1806
Hartford (The)            Hartford, Connecticut      1810

The complete output is sorted from the oldest founding year to the newest.

🛠️ Requirements
Python

Python 3.9+ is recommended.

Install the required Python dependencies using:

pip install -r requirements.txt
MySQL

A MySQL command-line client is required to execute Question 2.

Verify the installation with:

mysql --version

If MySQL is not available in the Windows PATH, use the full executable path.

Shell Environment

Question 3 requires:

Bash
curl
gawk
sort

The script can be executed using:

Git Bash
Linux
macOS


Design Considerations
Question 1

The scraper separates responsibilities between scraping, parsing, models and utility functions.

Sample HTML input is also provided so that the application can be tested without depending on a live website.

Question 2

The SQL queries are designed to work directly against the public Rfam database and demonstrate filtering, aggregation, joins and pagination.

Question 3

The shell script streams the downloaded CSV through the processing pipeline rather than creating an unnecessary intermediate file.

gawk with FPAT is used instead of a simple comma delimiter because CSV fields may contain commas inside quotation marks.


🧠 Key Technical Concepts
Python
Python modules
Functions
Command-line interfaces
HTTP requests
Web scraping
BeautifulSoup
HTML parsing
Data extraction
Exception handling
JSON
CSV
Object/data modelling
SQL
Relational databases
SELECT queries
Filtering
JOIN operations
Aggregation
GROUP BY
HAVING
Sorting
Pagination
Aggregate functions
Shell Scripting
Bash
Command-line arguments
Pipes
curl
gawk
AWK FPAT
CSV parsing
sort
Exit codes
Error handling
