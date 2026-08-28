#!/usr/bin/env bash
#
# company_parser.sh - Download the S&P 500 constituents CSV and print
#                      company name, headquarters location and founding
#                      year, sorted by founding year (oldest first).
#
# Usage:
#   ./company_parser.sh <csv-url>
#
# Example:
#   ./company_parser.sh \
#     "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"
#
# Requires: curl, gawk (GNU awk, for the FPAT CSV-parsing feature), sort.

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <csv-url>" >&2
    exit 1
fi

CSV_URL="$1"

# --fail        : make curl exit non-zero on an HTTP error (e.g. 404)
# --silent      : hide the progress bar
# --show-error  : still print the error message if --fail triggers
curl --fail --silent --show-error "$CSV_URL" |
    gawk '
        BEGIN {
            # FPAT tells (g)awk what a "field" looks like, instead of what
            # separates fields. This is what lets us split on commas while
            # still treating a quoted "Saint Paul, Minnesota" as ONE field.
            
            FPAT = "([^,]+)|(\"[^\"]*\")"
            OFS = "\t"
        }

        # Row 1 is the header (Symbol, Security, GICS Sector, ...) - skip it.

        NR == 1 { next }

        {
            company_name = $2   # "Security" column
            location     = $5   # "Headquarters Location" column
            founded_raw  = $8   # "Founded" column, e.g. 1902 or "2013 (1888)"

            # Strip the surrounding double quotes CSV puts around fields
            # that themselves contain a comma, e.g. "Saint Paul, Minnesota".

            gsub(/^"|"$/, "", company_name)
            gsub(/^"|"$/, "", location)
            gsub(/^"|"$/, "", founded_raw)

            # A few rows show two years, e.g. "2013 (1888)" meaning the
            # current company was formed in 2013 from a predecessor
            # founded in 1888. We take the first 4-digit number as the
            # founding year to keep the sort key simple and consistent.

            match(founded_raw, /[0-9]{4}/)
            founding_year = substr(founded_raw, RSTART, RLENGTH)

            print company_name, location, founding_year
        }
    ' |
    sort -t $'\t' -k3,3n



