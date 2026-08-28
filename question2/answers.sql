-- ============================================================================
-- Question 2 - Rfam public database SQL answers
--
-- Connect with:
--   mysql -h mysql-rfam-public.ebi.ac.uk -P 4497 -u rfamro Rfam
--
-- Tables used (columns confirmed with `DESCRIBE <table>` on the live server):
--   taxonomy(ncbi_id, species, tax_string, tree_display_name, align_display_name)
--   rfamseq(rfamseq_acc, accession, version, ncbi_id, mol_type, length,
--           description, previous_acc, source)
--   family(rfam_acc, rfam_id, description, type, ...)
--   full_region(rfam_acc, rfamseq_acc, seq_start, seq_end, bit_score,
--               evalue_score, cm_start, cm_end, truncated, type, is_significant)
-- ============================================================================


-- ----------------------------------------------------------------------------
-- (a) How many types of Acacia plants can be found in the taxonomy table?
-- ----------------------------------------------------------------------------
-- "Acacia " (with a trailing space) restricts the match to the genus Acacia
-- itself, e.g. "Acacia aneura", and excludes unrelated names that merely
-- contain the substring "Acacia" elsewhere.
-- Result on the live database: 326

SELECT COUNT(*) AS acacia_species_count
FROM taxonomy
WHERE species LIKE 'Acacia %';


-- ----------------------------------------------------------------------------
-- (b) Which type of wheat has the longest DNA sequence?
-- ----------------------------------------------------------------------------
-- "Wheat" corresponds to the genus Triticum. taxonomy.species also contains a
-- few "Triticum ... virus" entries (viruses that infect wheat, not wheat
-- itself), so those are explicitly excluded.
-- Result on the live database: Triticum durum (durum wheat), 836,514,780 bp
-- (rfamseq_acc = LT934116.1)

SELECT tx.species, rf.rfamseq_acc, rf.length
FROM rfamseq rf
JOIN taxonomy tx ON rf.ncbi_id = tx.ncbi_id
WHERE tx.species LIKE 'Triticum%'
  AND tx.species NOT LIKE '%virus%'
ORDER BY rf.length DESC
LIMIT 1;


-- ----------------------------------------------------------------------------
-- (c) Paginated list of family name + longest DNA sequence length,
--     descending by length, only families with max length > 1,000,000,
--     page 9 of 15 results per page.
-- ----------------------------------------------------------------------------
-- Page size = 15  ->  page 9 means we skip the first 8 pages:
--   OFFSET = (page_number - 1) * page_size = (9 - 1) * 15 = 120
--   LIMIT  = 15
--
-- Result on the live database (page 9, rows 121-135 of the sorted list):
--   All 15 rows on this page share the same max_length (836,514,780 bp),
--   because that value comes from the same single wheat sequence
--   (LT934116.1, Triticum durum) which many different families all have
--   a significant hit on:
--     RF01284 snoR8a        836514780
--     RF01286 snoR26        836514780
--     RF01292 snoR2         836514780
--     RF01847 Plant_U3      836514780
--     RF01911 MIR2118       836514780
--     RF03160 twister-P1    836514780
--     RF03209 MIR9657       836514780
--     RF03674 MIR5387       836514780
--     RF03685 MIR9677       836514780
--     RF03896 MIR2275       836514780
--     RF03926 MIR1435       836514780
--     RF04110 MIR5084       836514780
--     RF04251 MIR5070       836514780
--     RF04331 Plastid-clpP  836514780
--     RF04335 Plastid-rpl20 836514780
--
-- Note: this query performs a large JOIN + GROUP BY over the full
-- `full_region` table (tens of millions of rows) and can take several
-- minutes to run against the public server - this is expected given the
-- table size, not a bug in the query.

SELECT f.rfam_acc, f.rfam_id, MAX(rf.length) AS max_length
FROM full_region fr
JOIN rfamseq rf ON fr.rfamseq_acc = rf.rfamseq_acc
JOIN family f   ON f.rfam_acc    = fr.rfam_acc
WHERE fr.is_significant = 1
GROUP BY f.rfam_acc, f.rfam_id
HAVING MAX(rf.length) > 1000000
ORDER BY max_length DESC
LIMIT 15 OFFSET 120;
