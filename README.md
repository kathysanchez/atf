### Inspections by Bureau of Alcohol, Tobacco, Firearms and Explosives 

Data source: [https://www.atf.gov/firearms/firearms-compliance-inspection-results](https://www.atf.gov/firearms/firearms-compliance-inspection-results)

`atf.py` 
  The primary script for cleaning and analyzing data. I am just working on inspections for now, not the lists of federal firearms licensees.
  - It handles: data preprocessing, summary stats, descriptive stats, generating plots and histograms

`ATF_Inspection_Figures.qmd` 
  A Quarto Markdown file for rendering a pdf (`.pdf`) for easily viewing figures.

`ATF_Inspection_Figures.pdf`  
  The rendered output from `ATF_Inspection_Figures.pdf` containing additional plots for easy viewing.

`outputs/`
A folder where I save my working output.
    `plots/`
    A subfolder for plot files.



<!-- 
  - It outputs 
    - A cleaned Excel spreadsheet (`.xlsx`) with: the panel, summary stats, descriptive stats
    - Time series in a short video (`.mp4`)
- `utils.py`
  A utility module containing plotting functions used in `atf.py`

-->