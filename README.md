### Inspections by Bureau of Alcohol, Tobacco, Firearms and Explosives 
- Data source [https://www.atf.gov/firearms/firearms-compliance-inspection-results](https://www.atf.gov/firearms/firearms-compliance-inspection-results)

- `atf.py` 
  The primary script for cleaning and analyzing data. I am just working on the numerator for now, not the lists of federal firearms licensees.
  - It handles: data preprocessing, summary stats, descriptive stats, generating plots and histograms
  
- `outputs/`
  A folder where output files are saved.
    - `plots/`
      A subfolder for plot files.

<!-- 

  - It outputs 
    - A cleaned Excel spreadsheet (`.xlsx`) with: the panel, summary stats, descriptive stats
    - Time series in a short video (`.mp4`)
- `utils.py`
  A utility module containing plotting functions used in `atf.py`

- `output_figures.qmd` 
  A Quarto Markdown file for rendering a Word document (`.docx`) for easily viewing figures.

- `ATF_Inspection_Figures.docx`  
  The rendered output from `output_figures.qmd` containing additional plots for easy viewing.
-->