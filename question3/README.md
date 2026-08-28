# Question 3 - Shell Script: S&P 500 Company Data

A shell script that downloads a CSV of S&P 500 companies and prints each
company's **name**, **headquarters location** and **founding year**, sorted
by founding year (oldest first).

## Files

| File | Purpose |
|---|---|
| `company_parser.sh` | The script itself |
| `sample_output.txt` | Example output (first 20 rows) |

## Usage

```bash
chmod +x company_parser.sh
./company_parser.sh "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"
```

Pipe through `column -t -s$'\t'` for aligned, human-readable columns:

```bash
./company_parser.sh "<url>" | column -t -s$'\t'
```

## How it works

1. **`curl --fail --silent --show-error "$CSV_URL"`** downloads the CSV and
   streams it straight to `awk` (no temporary file needed). `--fail` makes
   curl exit with an error code if the server returns a 4xx/5xx response,
   instead of silently printing an HTML error page as if it were data.

2. **`awk` with `FPAT`** parses the CSV and picks out three columns:
   - column 2 - `Security` (company name)
   - column 5 - `Headquarters Location`
   - column 8 - `Founded`

   A plain `awk -F,` (split on every comma) would break on this dataset,
   because fields like `"Saint Paul, Minnesota"` are quoted specifically
   *because* they contain a comma. Splitting on every comma would wrongly
   cut that field into `"Saint Paul` and `Minnesota"`.

   `FPAT` flips the logic: instead of describing what separates fields, it
   describes what a field *looks like*:

   ```awk
   FPAT = "([^,]+)|(\"[^\"]*\")"
   ```

   This matches either "a run of characters with no comma" or "a whole
   quoted string", so a quoted field with an internal comma is correctly
   treated as a single field.

3. A few rows in the `Founded` column look like `2013 (1888)` - the current
   corporate entity was formed in 2013 from a predecessor founded in 1888.
   `match(founded_raw, /[0-9]{4}/)` grabs the **first** 4-digit year found,
   so the sort key stays a single, simple number.

4. **`sort -t $'\t' -k3,3n`** sorts the tab-separated output numerically
   (`n`) by the 3rd field (the founding year).

## Design decisions

- **`gawk` instead of `cut`/plain `awk -F,`**: correctness beats simplicity
  here - a naive comma split silently produces wrong data on this exact
  file, and getting that wrong would not be visibly obvious.
- **Streamed, not saved to disk**: `curl | awk | sort` avoids writing an
  intermediate file, which is unnecessary for a one-off transformation of
  this size.
- **`set -euo pipefail`**: the script stops immediately if the download
  fails or an undefined variable is used, rather than silently continuing
  with empty/partial data.

## Example output

See [`sample_output.txt`](sample_output.txt). First few rows:

```
Company Name              Location                   Founded Year
BNY Mellon                New York City, New York     1784
State Street Corporation  Boston, Massachusetts        1792
Colgate-Palmolive         New York City, New York      1806
Hartford (The)            Hartford, Connecticut        1810
```
