Date of synchrony experiment: unknown
Person carrying out experiment: Steve Haase, Charles Lin


Strain: 15Da; bar1

STARTING CONDITIONS
Starting media:YEP 2% galactose
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
Length of time course following synchronization: 278

BUDDING INDEX
Clock	Lifeline	Total	Budded30	17.37238297	224	038	26.78193366	243	346	36.19148436	286	454	45.60103505	245	362	55.01058574	256	270	64.42013644	265	578	73.82968713	209	386	83.23923783	229	1594	92.64878852	214	20102	101.8127419	205	51110	110.0995621	206	79118	118.8609676	218	128126	128.5103248	205	142134	138.159682	217	171142	147.8090392	233	197150	157.4583964	245	221158	167.1077536	237	203166	176.7571108	233	167174	186.406468	246	144182	196.0558252	217	111190	204.8995825	228	97198	213.1864027	203	100206	222.4553532	219	115214	232.1047104	329	182222	241.7540676	211	127230	251.4034248	232	149238	261.052782	214	141246	270.7021392	224	158254	280.3514964	207	143262	290.0008536	203	133270	299.6502108	210	133278	307.986423	222	134

CLOCCS PARAMETERS
recovery time: 100.3 min
period length: 85.0 min
How period length was determined: budding index in CLOCCS algorithm

RNA EXTRACTION AND SUBMISSION
Date of RNA extraction: Unknown
Date of RNA submission: Unknown
RNA was extracted using an acid phenol/chloroform protocol.
2ug were submitted to the Duke Microarray Core Facility.
The RNA was amplified once and labeled using the Affy 1-cycle IVT kit.
The labeled cDNA for each time point was applied to an Affymetrix Yeast 2.0 array.
Any issues in RNA extraction or submission: Only RNA from every other time point was extracted and submitted (16 min time points), starting with 38 minutes


NORMALIZATION
CEL files for this experiment were masked to remove any probes corresponding to S. pombe.  
The data was then normalized and summarized using a modified version of dChip method from the aft package in Bioconductor.  The modified code allows for the correct baseline array used for the normalization process.  The command used was expresso2(inputdata, normalize.method="invariantset", bgcorrect.method="none", pmcorrect.method="pmonly", summary.method="liwong")
