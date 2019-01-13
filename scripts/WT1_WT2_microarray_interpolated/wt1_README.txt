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
Clock	Lifeline	Total	Budded30	14.62686567	200	038	25.00973394	200	046	35.39260221	200	154	45.77547047	207	162	56.15833874	209	270	66.54120701	217	478	76.92407528	203	486	87.30694354	217	1094	97.68981181	205	56102	108.6893431	200	85110	119.5034327	217	129118	129.7528762	213	156126	140.0023198	237	196134	150.2517633	212	196142	160.5012069	232	219150	170.7506504	208	189158	181.000094	223	167166	191.2495376	224	138174	201.6344906	201	86182	212.8104946	234	96190	223.282915	203	102198	233.5323585	242	132206	243.7818021	218	124214	254.0312456	203	130222	264.2806892	280	180230	274.5301328	262	173238	284.7795763	216	145246	295.0290199	207	129254	305.7556421	224	134262	316.8129537	245	144270	327.0623973	201	116278	337.3118408	215	125

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
