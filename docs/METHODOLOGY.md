# Methodology

## 1. Page-by-page extraction
`extract_jobvision.py` opens all 263 PDF pages, extracts text and table candidates, and writes one JSON file per page. `review_pdf.py` renders contact sheets for visual inspection.

## 2. Mapping
`map_jobvision.py` maps only explicit recognized table headers to canonical fields. It never shifts a value merely because a column appears plausible.

## 3. Normalization
Arabic/Persian variants, digits, spacing and punctuation are normalized. Original values remain available in page JSON.

## 4. Matching
Course and university names are matched separately. Exact/near-exact matches are accepted at a strict 96 score threshold. Scores from 88–95.99 are held for manual review.

## 5. Final dataset
Only records with verified course + university matches are joined to Sanjesh records. All ambiguous and unmatched records remain in audit outputs.

## 6. Missing data
Missing source values remain missing. The system never fills a missing salary, employment percentage, rank or satisfaction value with an estimate.

## 7. Geography
The project follows the reference project's rule: unresolved locations are not guessed to the nearest province.
