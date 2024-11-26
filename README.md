# Inspections by Bureau of Alcohol, Tobacco, Firearms and Explosives 


- **`atf.py`**:  
  The primary script for cleaning and analyzing data. It handles:
  - Data preprocessing and merging
  - Summary statistics
  - Descriptive statistics
  - Generating plots and histograms
  - It outputs 
    - A cleaned Excel spreadsheet (`.xlsx`) with
      - The full data panel
      - Summary stats
      - Descriptive stats
    - Time series in a short video (`.mp4`)

- **`utils.py`**:  
  A utility module containing helper functions used in `atf.py`

- **`output_figures.qmd`**:  
  A Quarto Markdown file for rendering a Word document (`.docx`) for easily viewing figures.

- **`ATF_Inspection_Figures.docx`**:  
  The rendered output from `output_figures.qmd` containing additional plots for easy viewing.
