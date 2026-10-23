This README.txt file was generated on 20240105 by Luke Monroe

-------------------
GENERAL INFORMATION
-------------------

1. Title of Dataset: Conversion of HONO to Nitric Acid in supermicron aqueous droplets is accelerated in acidic conditions.

2. Author Information

First Author Contact Information
    Name: Luke Monroe
    Institution: Carnegie Mellon University
    Address: 5000 Forbes Ave Pittsburgh PA 15219
    Email: lukemonr@andrew.cmu.edu, luke.w.monroe@gmail.com
	Phone Number: 

Corresponding Author Contact Information
    Name: Ryan Sullivan
    Institution: Carnegie Mellon University
    Address: 5000 Forbes Ave Pittsburgh PA 15219
    Email: rsullivan@cmu.edu
	Phone Number: 

Author Contact Information
    Name: Jack Hall
    Institution: Carnegie Mellon University
    Address: 5000 Forbes Ave Pittsburgh PA 15219
    Email:jwhall@andrew.cmu.edu
	Phone Number:

Author Contact Information
    Name: Graham Thornhill
    Institution: Carnegie Mellon University 
    Address: 5000 Forbes Ave Pittsburgh PA 15219
    Email:gthornhi@andrew.cmu.edu
	Phone Number: 


---------------------
DATA & FILE OVERVIEW
---------------------


Directory of Files:


Each droplet is separated oxidation scheme > droplet matrix > date (Year_Month_Day_hr_min_sec). Each droplet folder contains the following:
 
   A. Filename: Rmatrix [data and time].mat 
      Short description: This is the Raman spectrum for the given droplet prior to any processing such as denoising, etc.  
        
   B. Filename: Processed_Raman_Spectra.mat
      Short description: This is the processed Raman spectrum for the given droplet that inclusing denoising, etc. This is the file that was used for further kinetics analysis
     
   C. Filename: Base spatial scale Corrected Raman Spectrum.fig
      Short description: This is the MATLAB figure of the Raman spectrum post initial data processing but prior to kinetic analysis

   D. Filename: Base spatial scale Corrected Raman Spectrum.png
      Short description: An exported form of C. in .png format that does not need MATLAB to view

   E. Filename: Denoised Raman Spectrum.fig
      Short description: A less processed version of the Raman spectrum that includes only denosing, but not baslining or other corrections

   F. Filename: Denoised Raman Spectrum.png
      Short description: An exported form of E. in .png format that does not need MATLAB to view

If applicable, droplet folders may include the following: 

   G. Filename: HomSimplePlot.png
      Short description: This is a summary of fitting statistics for a droplet that was fit with the WGM algorithm for homogenous (non-coreshell) droplets summarized in the paper. This data includes refractive index and droplet size. Fit error is also quantified. High fit error is indicative of the homogenous model not accurately describing the droplet either due to droplet not being homogenous or poor WGM identification. Error axis is on a log scale. Only frame with 3 or more WGMs were fit, so not all frames have data. Each point is a frame.

   H. Filename: kineticsarray.csv
      Short description: A .csv showing the peak area of the nitrate peak vs time used to derive the nitrate formation rate

   I. Filename: Nitrate concentration PA.fig
      Short description: A MATLAB figure plotting the kineticsarray.csv data in H. Data here is the total droplet run, excluding certain periods of every interference that may be at the start or end of the droplet experiment. 

   J. Filename: Nitrate Conc v time and fit.fig
      Short description: A linear fit of to determine nitrate formation rate in Mol/sec. Model fits do not include entire droplet time period shown in J. They focus on periods of change, and try to exclude periods of excessive WGM interference whereever possible. Time axis is start of model time, and does not correspond to start of droplet capture shown in  I. 

   K. Filename: RunParameters.csv
      Short description: Log file used to record kinetics model parameters, useful metrics for the reader will include frames that were removed due to external intereference or when the kinetics model starts and ends. Not all metrics are useful for every droplet as this kinetics model was built to accomodate other analysis beyond what is included in this dataset/paper. 

   I. Filename: Rate of NO3 change v time.fig
      Short description: Figure that shows the derivative of the fit in J. This derivative was use to ensure that the kinetics model fit did not capture stagnent periods before reaction conditions or after reaction completion that could interfere with rate calculations. 


-----------------------------------------
DATA DESCRIPTION FOR: Rmatrix_[date].mat
-----------------------------------------

1. Number of variables:5


2. Number of cases/rows: variable (experiment length dependent)


3. Missing data codes: NAN


4. Variable List


    A. Name: frame_index
       Description: numerical count of frame order (rows of rspectra)

    B. Name: rspectra
       Description: array listing intensity at each point in a Raman frame. Rows are frame and columns are wavelengths 

    B. Name: time_start
       Description: seconds since start of collection for each Raman frame start time

    B. Name: time_stop
       Description: seconds since start of collection for each Raman frame stop time. Difference between start and stop is frame integration time.

    B. Name: wavelength_index
       Description: wavelengths (nm) corresponding to each pixel on Raman spectrograph CCD. Column labels of rspectra 

-----------------------------------------
DATA DESCRIPTION FOR: Processed_Raman_Spectra.mat
-----------------------------------------

1. Number of variables: 10


2. Number of cases/rows: variable (experiment length dependent)


3. Missing data codes: NAN


4. Variable List

    A. Name: base_spectrum 
	 Description: not used

    B. Name: denoised_raman 
	 Description: Raman_spectrum that has been denoised, rows = frames, cols = wavelengths, values = intensity 

    C. Name: frame_index 
	 Description: frame number in sequential order, used to label rows in spectra

    D. Name: raman_base_corrected 
	 Description: Raman spectrum that has been baselined 

    E. Name: raman_base_corrected and denoised
	 Description: Raman spectrum that has been baselined and denoised

    F. Name: raw_raman_data
	 Description: Raman spectrum straight from spectrograph

    G. Name: settings
	 Description: parameters used in baselining, denoisng, and figure making 

    H. Name: temporal_change
	 Description: not used

    I. Name: time_series
	 Description: frame time start, in unix time 

    J. Name: wavelength_index
	 Description: Wavelength (nm) corresponding to each data point. Columns in spectra

-----------------------------------------
DATA DESCRIPTION FOR: Kineticsarray.csv
-----------------------------------------

1. Number of variables: 3


2. Number of cases/rows: variable (experiment length dependent)


3. Missing data codes: NAN


4. Variable List

    A. Name: 1
	 Description: seconds since start of experiment 

    B. Name: 2
	 Description: ratio of concentration of nitrate at time t over concentration of nitrate at time 0

    C. Name: 3
	 Description: Nitrate concentration at time t 

-----------------------------------------
DATA DESCRIPTION FOR: RunParameters.csv
-----------------------------------------

1. Number of variables: 21


2. Number of cases/rows: 1


3. Missing data codes: no missing data


4. Variable List

    A. Name: Lower Wavelength
	 Description: lower wavelength of peak of interest

    B. Name: Upper Wavelenght (misspelling persists in the code)
	 Description: upper wavelength of peak of interest

    C. Name: Frame Time Step
	 Description: Seconds of data collection for each frame 

    D. Name: WGM removal multiplyer
	 Description: multiplier for the standard deviation metric to identify and remove WGMs, based on the derivative of peak area. WGMs show rapid increase in peak area. 

    E. Name: Averaging Frame Window
	 Description: number of frames incorporated in the moving average of concentration 

    F. Name: Frames cut at beginning
	 Description: Number of frames cut at start of experiment to remove room light interfence when setting up experiment

    G. Name: Frames cut at end
	 Description: number of frames cut at the end of experiment to remove room light interference when ending experiment or period after droplet was lost

    H. Name: background peak center
	 Description: center wavelength of the peak used for background normalization to account for day-to-day variations in intensity. Background peak was generally obejective immersion oil.

    I. Name: calibration curve
	 Description: the numeric indicator of the calibration curved used for analysis 

    J. Name: peak intensity cal curve
	 Description: not used in this dataset

    K. Name: Area model cut point start (sec)
	 Description: experiment time at which the kinetics model starts the linear fit

    L. Name: Intensity model cut point start (sec)
	 Description: not used in this dataset

    M. Name: Area model cut point end (sec)
	 Description: experiment time at which the kinetics model stops the linear fit

    N. Name: Intensity model cut point end (sec)
	 Description: not used in this dataset

    O. Name: Frames to grow
	 Description: Number of frames that are used to expand the wavelengths used in the peak area calculation from the minium value to the specified value. NO3 peak increases in width and intensity and this setting and P are used to account for that growth in width. 

    P. Name: Minimum wavelength distance
	 Description: the minium distance between wavelength at start of run. 

    Q. Name: Approach used to find area
	 Description: a numeric value indicating if area remains constant throughout whole experiment (for calibration curves) or if it grows in width and intensity.

    R. Name: droplet radius
	 Description: not used in thsi dataset

    S. Name: initial NO2 (M)
	 Description: not used in this dataset

    T. Name: O2 (atm)
	 Description: not used in this dataset

    U. Name: O3 (atm)
	 Description: not used in this dataset

--------------------------
METHODOLOGICAL INFORMATION
--------------------------

1. Software-specific information:

Name: MATLAB 
Version: 2016b or later 
System Requirements: 
	CPU: 2 cores or higher
	RAM: 8 gig or higher
	Storage: more than 25 gig
Open Source? (Y/N): N

Executable URL:
Source Repository URL:
Developer: Mathworks
Product URL: https://www.mathworks.com/products/matlab.html
Software source components:

Additional Notes: Should run on windows or mac

2. Equipment-specific information:

Manufacturer: Teledyne Princeton Instruments
Model: ProEM: 16002 eXcelon™3 CCD

Manufacturer: Teledyne Princeton Instruments
Model: SP2500 Raman spectometer

Manufacturer: PARI TREK S
Model: medical nebulizer

Manufacturer: Azco industries
Model: HTU-500 ozone generator

Additional Notes:


3. Date of data collection: Jan 2023 to Sept 2023


