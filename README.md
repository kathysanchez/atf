### Inspections by the Bureau of Alcohol, Tobacco, Firearms and Explosives 

This is a personal project examining ATF inspections from 2021 through 2024. Please give credit if you use any part of this work. The data are from [https://www.atf.gov/firearms/firearms-compliance-inspection-results](https://www.atf.gov/firearms/firearms-compliance-inspection-results) 

`atf.py`  
  The primary script for cleaning and analyzing data. It handles: data preprocessing, summary stats, descriptive stats, generating plots.

`ATF_Inspection_Figures.qmd`  
  A Quarto Markdown file for rendering a pdf (`.pdf`) for easily viewing figures.

`ATF_Inspection_Figures.pdf`  
  The rendered output from `ATF_Inspection_Figures.pdf` containing friendly select plots. 

`outputs/`
  A folder where I save my working output. 
  - `plots/`  
      A subfolder for select plot files.



<!-- 
  - It outputs 
    - A cleaned Excel spreadsheet (`.xlsx`) with: the panel, summary stats, descriptive stats
    - Time series in a short video (`.mp4`)
- `utils.py`
  A utility module containing plotting functions used in `atf.py`

-->