import numpy as np
import matplotlib.pyplot as plt
import h5py
import corner

data1 = h5py.File('myout.hdf5','r')
data2 = h5py.File('myout_org.hdf5','r')
data_3D1 = np.array(data1['pos'])
data_3D2 = np.array(data2['pos'])
print(data_3D1.shape)
org_steps = data_3D1.shape[0]
burn_steps = 2500
#Burning the initial walkers, you can choose the burning steps by looking at chain plots
data1_burn = data_3D1[burn_steps:]
data2_burn = data_3D2[burn_steps:]
print(data1_burn.shape)
walker = data1_burn.shape[1] 
steps = data1_burn.shape[0]
points = walker * steps
#reshaping the converging arrays after burning the initial runs
data_new1 = data1_burn.reshape((points,5))
data_new2 = data2_burn.reshape((points,4))
#data_3D1_col_rm = data_new1[:,:4]
#print(data_new1)
#print(data_new2)
#print(np.sort(data_new1[:,-1]))
#plt.plot(np.sort(data_new1[:,-1]))

labels=[r"$log_{10}(\frac{\mathcal{R}}{Gpc^{-3}yr^-1})$", r"$\alpha$", r"$m_{min} [M_\odot$]",r"$m_{max} [M_\odot]$",
        "$\sigma_\epsilon$"]

limits = [(1.8, 2.2),(-2.3,0.5),(2.5,13),(46,57),(0.03,0.065)]
# Calculate the mean values along each dimension
#mean_values1 = np.mean(data_new1, axis=0)
#provide true values if any
truth_values = [2, -1, 10, 50, 0.05]
#plotting the corner plot
figure1 = corner.corner(data_new1,labels=labels
                      ,show_titles=True,plot_datapoints=False,color='orange',
                        truths=truth_values,truth_color='red',smooth=True,range=limits)
figure1.savefig("cor_ecc_005.png")
#plt.show()
labels0=[r"$log_{10}(\frac{\mathcal{R}}{Gpc^{-3}yr^-1})$", r"$\alpha$", r"$m_{min} [M_\odot]$",r"$m_{max} [M_\odot]$"]
limits0 = [(1.8, 2.2),(-2.5,0.4),(3,13),(45,56)]

truth_values1 = [2, -1, 10, 50]
#plotting the corner plot
figure2 = corner.corner(data_new2,labels=labels0
                      ,show_titles=True,plot_datapoints=False,color='black',
                        truths=truth_values1,truth_color='red',range=limits0,smooth=True)
figure2.savefig("cor_scl_005.png")    

#The following code is to create a overplot
# Create an empty column (filled with None values)
new_column = np.empty((org_steps,walker,1))
# Concatenate the new column with the 3D array along the last axis (axis=2)
data_3D2_col_add = np.concatenate((data_3D2, new_column), axis=2)
data3_burn = data_3D2_col_add[burn_steps:]
data3 = data2_burn.reshape((points,4))
print(data3.shape)
# Add an empty column to data3
new_column = np.empty((points, 1))
data3_col_add = np.concatenate((data3, new_column), axis=1)
print(data3_col_add.shape)
#print(data3_burn.shape)
data_new3 = data3_burn.reshape((points,5))
print(data_new3.shape)
limits3 = [(1.8, 2.15),(-2.5,0.4),(3,13),(45,57),(0,0.07)]
figure4 = corner.corner(data3_col_add,labels=labels
                      ,show_titles=False,plot_datapoints=False,color='black',
                        truths=truth_values,truth_color='red',smooth=True,volume=False,range=limits3)
#figure4.savefig("cor_new.png")
# Volume in fucntion should be false, then empty column does not create issue in corner plots.
corner.corner(data_new1,fig=figure4,labels=labels
                      ,show_titles=False, plot_datapoints=False,color='orange',
                      volume=False,range=limits3, smooth=True)
legend_texts = ["CBBH", "EBBH","True Value"]  
legend_colors = ["black", "orange", "red"] 
legend_handles = [plt.Line2D([],[], color=color, linewidth=2) for color in legend_colors]
figure4.legend(legend_handles, legend_texts, loc='upper right', fontsize=15)
figure4.savefig("com_cor_005.png")
