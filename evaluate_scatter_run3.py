# -*- coding: utf-8 -*-
"""
Example script to serve as starting point for evaluating scatter results
of run3 (with incorrect CTAC/mu-map)

The current script reads results from run0 and run3 and displays them.

In this exercise, a wrong mu-map (here called CTAC) is used, where bone mu-values are approximately 
set to lung mu-values, maybe like in PET-MR.

run_scatter_3.sh runs both the scatter estimation and the attenuation correction
with this wrong CTAC. With this exercise you can check the influence of the wrong
mu-map on the scatter estimate, and on the reconstructed image.

Prerequisite:
You should have executed the following on your command prompt
    ./run_simulations_thorax.sh
    ./run_scatter_0.sh
    ./run_scatter_3.sh

Author: Kris Thielemans
"""
#%% Initial imports
import matplotlib.pyplot as plt
import stir
from stirextra import *
import os
#%% go to directory with input files
# adapt this path to your situation (or start everything in the exercises directory)
os.chdir(os.getenv('STIR_exercises_PATH'))
os.chdir('STIR-exercises')
#%% change directory to where the output files are
os.chdir('working_folder/GATE1')
#%% read in data from GATE2
# original scatter as generated by the simulation
org_scatter=to_numpy(stir.ProjData.read_from_file('my_scatter_g1.hs'));
# estimated scatter
estimated_scatter_run0=to_numpy(stir.ProjData.read_from_file('scatter_estimate_run0.hs'));
estimated_scatter_run3=to_numpy(stir.ProjData.read_from_file('scatter_estimate_run3.hs'));
#%% read CTACs (aka mu-maps)
correctCTAC=to_numpy(stir.FloatVoxelsOnCartesianGrid.read_from_file('CTAC_g1.hv'));
wrongCTAC=to_numpy(stir.FloatVoxelsOnCartesianGrid.read_from_file('wrong_CTAC.hv'));
#%% bitmap display of CTACs
maxforplot=correctCTAC.max();

slice=10;
plt.figure();
ax=plt.subplot(1,2,1);
plt.imshow(correctCTAC[slice,:,:,]);
plt.colorbar();
plt.clim(0,maxforplot);
plt.axis('off');
ax.set_title('correct CTAC')

ax=plt.subplot(1,2,2);
plt.imshow(wrongCTAC[slice,:,:,]);
plt.clim(0,maxforplot);
plt.colorbar();
plt.axis('off');
ax.set_title('incorrect CTAC')

#%% horizontal profiles through CTACs
plt.figure();
plt.plot(correctCTAC[10,154/2,:],'b');
plt.hold(True);
plt.plot(wrongCTAC[10,154/2,:],'c');
plt.legend(('Input for simulation','FBP (correct AC)', 'FBP (incorrect AC)'));
plt.legend(('correct CTAC', 'incorrect CTAC'));
#%% Display bitmaps of a middle sinogram
maxforplot=org_scatter.max()*1.1;

plt.figure()
ax=plt.subplot(1,3,1);
plt.imshow(org_scatter[10,:,:,]);
plt.clim(0,maxforplot)
ax.set_title('Original');
plt.axis('off');

ax=plt.subplot(1,3,2);
plt.imshow(estimated_scatter_run0[10,:,:,]);
plt.clim(0,maxforplot);
ax.set_title('estimated\n(correct CTAC)');
plt.axis('off');


ax=plt.subplot(1,3,3);
plt.imshow(estimated_scatter_run3[10,:,:,]);
plt.clim(0,maxforplot);
ax.set_title('estimated\n(incorrect CTAC)');
plt.axis('off');
#%% Display central profiles through the sinogram
plt.figure()
plt.plot(org_scatter[10,:,192/2],'b');
plt.hold(True)
plt.plot(estimated_scatter_run0[10,:,192/2],'c');
plt.plot(estimated_scatter_run3[10,:,192/2],'r');
plt.legend(('original','estimated (correct CTAC)','estimated (incorrect CTAC)'));

#%% Read in images
org_image=to_numpy(stir.FloatVoxelsOnCartesianGrid.read_from_file('FDG_g1.hv'));
fbp_result_run0=to_numpy(stir.FloatVoxelsOnCartesianGrid.read_from_file('FBP_recon_with_scatter_correction_run0.hv'));
fbp_result_run3=to_numpy(stir.FloatVoxelsOnCartesianGrid.read_from_file('FBP_recon_with_scatter_correction_run3.hv'));
#%% bitmap display of images
maxforplot=org_image.max()*.6;

slice=10;
plt.figure();
ax=plt.subplot(1,3,1);
plt.imshow(org_image[slice,:,:,]);
plt.colorbar();
plt.clim(0,maxforplot);
plt.axis('off');
ax.set_title('ground truth')

ax=plt.subplot(1,3,2);
plt.imshow(fbp_result_run0[slice,:,:,]);
plt.clim(0,maxforplot);
plt.colorbar();
plt.axis('off');
ax.set_title('FBP\n(correct CTAC)')

ax=plt.subplot(1,3,3);
plt.imshow(fbp_result_run3[slice,:,:,]);
plt.clim(0,maxforplot);
plt.colorbar();
plt.axis('off');
ax.set_title('FBP\n(incorrect CTAC)')

#%% horizontal profiles through images
plt.figure();
plt.plot(org_image[10,154/2,:],'b');
plt.hold(True);
plt.plot(fbp_result_run0[10,154/2,:],'c');
plt.plot(fbp_result_run3[10,154/2,:],'k');
plt.legend(('Input for simulation','FBP (correct AC)', 'FBP (incorrect AC)'));
#%% close all plots
plt.close('all')
