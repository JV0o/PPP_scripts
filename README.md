This repository consists 3 python scripts that can be used to facilitate uploading data on benchling from AMBR fermentations. 

Additionnally to the .py files that require installation of python and the correct packages, .exe files for the two scripts AMBR_sampling_scheme and Make_sumary_excel can be found under the dist folder. They can just be open and should run without any necessary installation (it might take a few seconds to start it though, so be patient). 

Regarding the AMBR_sampling_scheme. This one helps to organize a sampling scheme. You can choose between "24 and 96 well plate". For now only 96 plate works in the workflow so only use that one. 
"Number of Reactors": just write the amount of reactors you run.
"Number of samples per reactor": Here you can choose the amount samples you take. It will include sample S0.
"Starting reactor number": Write the number of the first reactor. FOr example if you use reactor R20, R21, R22 write R20 as starting reactor.
"Take end batch Sample": Choose to take and end of batch sample if you want to do so. This sample will no be counted in the Number of samples it will add one more sample.
Generate the scheme and check if all the samples are there. They will be placed in a row way as in AMBR it is easier that way. A column way to sort is in developpment.

Regarding the Make_summary_excel script. This one will make a summary excel fille with all data needed to register the timepoint samples in benchling. To do so three files are needed in the following order:
- A sampling scheme excel file (which can be done with the first script). 
- A timepoints file that can be downloaded from the AMBR process as described in the workflow SOP.
- A ID stage run file that can be downloaded from benchling as described in the workflow SOP. 
At the end give the excel file a name like XXX_PD_0XX_AMBR_summary_excel and save it. It can now be used to upload on benchling as described in the workflow SOP. 
