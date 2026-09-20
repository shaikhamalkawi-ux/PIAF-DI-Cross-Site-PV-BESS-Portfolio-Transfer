# Manuscript support

`make_figures.py` rebuilds the three R6R8 figure PDFs from the public-safe
admitted CSV values under `reproducibility/reference/derived/`.
It pins Matplotlib PDF and PostScript font output to Type 42 so the resulting
manuscript contains embedded CID TrueType/Type 1 fonts and no Type 3 fonts.

The unpublished manuscript, supplement, editable source archive, and author
metadata are not committed to this public repository. They are returned only
through the controlled Google Drive workspace.
