# DATACOR_codes
Codes to calculate adsorption energies in DATACOR project 

A part of the project (DATACOR) is based on the adsorption energy of certain molecules over Aluminum.
The working scheme consists of a screening of molecule position on a surface of Al (111). Therefore, we use the code from Combination.py that combine the SLAB and POSCAR files. Where the files are in VASP format, the SLAB has the surface of Al (111) and POSCAR has the geometry of the molecule. The geometry of the molecule will be rotated on the X, Y, and Z axes and centered in the center of the SLAB file. Finally, the output is generated in gen format, a format of DFTBplus. This code generate the different adsorption geometries to perform adsorption screening. The optimization of each geometry we use the XTB package (https://github.com/grimme-lab/xtb) to reduce the computational cost.

The next step use the geometry with the lowest adsorption energy to start the DFT calculation with VASP package. To automatize the change from XTB to VASP calculation use the script_make, a bashscript that use makeDIR file that contain the the number of calculation and the number of rotations to generate the POSCAR and POTCAR file.

This code was developed in the frame of project DataCor (POCI-01-0145-FEDER-030256 and PTDC/QUI-QFI/30256/2017, https://datacoproject.wixsite.com/datacor)
