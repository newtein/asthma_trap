## Main file

asthma_trap_init.py 
This is the standalone main file to reproduce the results. It depends on the following files: 

prepare_data_for_modeling_child_or.py
Reads the BRFSS and ACBS datasets to calculate PR and IR across the US. 

incidence_rate_logic.py
Describes the logic for imputing the missing values for nonparticipating states in BRFSS and ACBS. 

AF_calculations/calculate_AF.py
calculates the AF for each county and aggregates it to the state-level.The file uses the NO2 and population data for estimation.  

merge_with_ev_sales.py
Reads the light-duty vehicle data and merges with the original dataset. 

call_lme4_in_R.py
Describes the final model. This file calls for an R file, where the model is defined. 

# Files to reproduce the images
Figure 1: ev_sales_evadoption_evdaption_data_plot_2011_2022.ipynb
Figure 2: Flowchart created through Microsoft Visio
Figure 3: figure_3_v2_epa_ambient.ipynb
Figure S3: plotBasemap_v3_pollution.ipynb

# Data
Supplementary Tables S1-S13






