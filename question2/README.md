# Question 2 - Rfam Database SQL Questions

Answers to three SQL questions against the public **Rfam** database.

## Files

| File | Purpose |
|---|---|
| `answers.sql` | All three SQL queries, with the question and result recorded as a comment above each |
| `explanation.md` | Plain-English explanation of every query - what it does, why each `JOIN`/`GROUP BY`/`HAVING`/`LIMIT` is needed, and how to talk through it in an interview |

## Connecting to the database

```bash
mysql -h mysql-rfam-public.ebi.ac.uk -P 4497 -u rfamro Rfam
```

No password is required (read-only public account). Run a query file with:

```bash
mysql -h mysql-rfam-public.ebi.ac.uk -P 4497 -u rfamro Rfam < answers.sql
```

## Questions answered

1. How many types of Acacia plants are in the `taxonomy` table? **-> 326**
2. Which type of wheat has the longest DNA sequence? **-> Triticum durum (durum wheat)**
3. A paginated query returning family accession, family name and longest
   sequence length (descending, length > 1,000,000), for page 9 at 15
   results per page.

See [`explanation.md`](explanation.md) for the full reasoning behind each
query.
