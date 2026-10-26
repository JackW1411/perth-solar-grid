# Gotchas

Anything that wasted more than 15 minutes. One entry each: what happened, why, and the fix.

- **Postcode type mismatch.** pandas reads CER postcodes as integers (800), ABS stores them as text ("0800"). A join silently matches nothing. Fix: `.astype(str).str.zfill(4)` in `load_cer.py`.
- **Western Power catchments leave gaps.** Matching postal areas to NCMT catchments by interior point left Leederville, Roleystone and Pinjarra unmatched. Fix: match on largest area overlap (D14).
- **CARTO basemap tiles now need an API key.** The web map showed "API KEY REQUIRED" watermarks. Fix: OpenStreetMap tiles.
- **AEMO site blocks automated fetches** (403 on policy pages, binary PDFs). Fix: download the PDF and extract text with `pdftotext -layout`.
