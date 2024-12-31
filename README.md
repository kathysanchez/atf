### Inspections by the Bureau of Alcohol, Tobacco, Firearms and Explosives 

This is a personal project examining changes in ATF inspections from 2021 through 2024. Please let me know if you want to use my work. The data are from [https://www.atf.gov/firearms/firearms-compliance-inspection-results](https://www.atf.gov/firearms/firearms-compliance-inspection-results) 

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

`requirements.txt`
  I used pip freeze to create this list of required libraries for this project.



<!-- 
  - It outputs 
    - A cleaned Excel spreadsheet (`.xlsx`) with: the panel, summary stats, descriptive stats
    - Time series in a short video (`.mp4`)
- `utils.py`
  A utility module containing plotting functions used in `atf.py`

-->