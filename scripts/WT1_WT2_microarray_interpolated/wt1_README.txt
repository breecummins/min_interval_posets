Date of synchrony experiment: unknown
Person carrying out experiment: Steve Haase, Charles Lin


Strain: 15Da; bar1

STARTING CONDITIONS
Starting media: YEP 2% galactose 
Temperature of waterbath: 30 deg Celsius
Starting concentration: unknown
Synchrony method: Elutriation
Pre-incubation?: Yes, 20% dextrose for 45 min at 30 deg Celsius

AFTER SYNCHRONIZATION
Media used: YEP 2% dextrose + 1M Sorbitol
	Pre-warmed?: Yes
Concentration of cells at time 0 min: 1.0e7 cell/mL
Temperature of waterbath: 30 deg Celsius

Frequency of time points: Every 8 minutes
Length of time course following synchronization: 278 minutes

BUDDING INDEX
Clock	Lifeline	Total	Budded

CLOCCS PARAMETERS
recovery time: 95.8 min
period length: 77.1
How period length was determined: budding index in CLOCCS algorithm

RNA EXTRACTION AND SUBMISSION
Date of RNA extraction: Unknown
Date of RNA submission: Unknown
RNA was extracted using an acid phenol/chloroform protocol.
2ug were submitted to the Duke Microarray Core Facility.
The RNA was amplified once and labeled using the Affy 1-cycle IVT kit.
The labeled cDNA for each time point was applied to an Affymetrix Yeast 2.0 array.
Any issues in RNA extraction or submission: Only RNA from every other time point was extracted and submitted (16 min time points), starting with 30 minutes

NORMALIZATION
CEL files for this experiment were masked to remove any probes corresponding to S. pombe.  
The data was then normalized and summarized using a modified version of dChip method from the aft package in Bioconductor.  The modified code allows for the correct baseline array used for the normalization process.  The command used was expresso2(inputdata, normalize.method="invariantset", bgcorrect.method="none", pmcorrect.method="pmonly", summary.method="liwong")