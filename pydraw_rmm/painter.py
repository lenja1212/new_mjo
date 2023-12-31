import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from pathlib import Path
from metrix import * 

#===========================================================
def getMembersPc(pc_text_file: Path, members_number):
    pc1_all = []
    pc2_all = []
#Read data
    with open(pc_text_file) as f1:
        for line in f1:
            if line != ['']:
                line = line.split(",")
                pc1_all.append(float(line[0]))
                pc2_all.append(float(line[1]))
    pc1_all_memb = np.array_split(pc1_all, members_number)
    pc2_all_memb = np.array_split(pc2_all, members_number)
    return pc1_all_memb, pc2_all_memb

#===========================================================
def rotate_vector(data, angle):
    # make rotation matrix
    # angle = -55
    theta = np.radians(angle)
    co = np.cos(theta)
    si = np.sin(theta)
    rotation_matrix = np.array(((co, -si), (si, co)))
    # rotate data vector
    rotated_vector = data.dot(rotation_matrix)
    return rotated_vector

#===========================================================
def form_data(arr1, arr2):
  data =[]
  for i in range(len(arr1)):
    data.append([arr1[i], arr2[i]])
  return np.array(data)

#===========================================================
def drawPc_OLD(pc_text_file: Path, pc_png_file: Path, inverse1 = 1, inverse2 = 1): # 3moths
    pc1 = []
    pc2 = []
    days = np.arange(0, 93, 1, dtype=int)
    #  PCs2     PsCs
    print("path pc: ", pc_text_file)

    with open(pc_text_file) as f1:
        next(f1)
        for line in f1:
            if line != ['']:
                line = line.split(",")
                pc1.append(inverse1 * float(line[0]))
                pc2.append(inverse2 * float(line[1]))

    # plt.figure(figsize=(6,6))
    fig, ax = plt.subplots()
    fig.set_figheight(6)
    fig.set_figwidth(6)
    jan_arr_pc1 = pc1[0:31]
    feb_arr_pc1 = pc1[31:59]
    mar_arr_pc1 = pc1[59:90]
    jan_arr_pc2 = pc2[0:31]
    feb_arr_pc2 = pc2[31:59]
    mar_arr_pc2 = pc2[59:90]
    text31 = np.arange(1, 32, 1, dtype=int)
    len_mar = 28
    text28 = np.arange(1, 29, 1, dtype=int)
    plt.xlim(-4, 4)
    plt.ylim(-4, 4)
    plt.xlabel('$RMM1$')
    plt.ylabel('$RMM2$')

# #ok
    rotated_data = rotate_vector(form_data(jan_arr_pc1, jan_arr_pc2), 0) # 0 -> -10
    plt.plot(rotated_data[:, 0], rotated_data[:, 1], '-o', color='red', ms=2, label='jan', linewidth=2)

# ###

    plt.annotate("START", (rotated_data[:,0][0], rotated_data[:,1][0] + 0.2), fontsize=8)
    for i in range(1,len(text31)):
        plt.annotate(text31[i], (rotated_data[:,0][i], rotated_data[:,1][i] + 0.2), fontsize=5)
      
    # rotated_data = rotate_vector(form_data(jan_arr_pc1[-1], feb_arr_pc1[0]), -10)
    plt.plot([jan_arr_pc1[-1], feb_arr_pc1[0]], [jan_arr_pc2[-1], feb_arr_pc2[0]], '-', color='chartreuse', ms=2, linewidth=2)
# #ok
    rotated_data = rotate_vector(form_data(feb_arr_pc1, feb_arr_pc2), 0)
    # plt.plot(feb_arr_pc1, feb_arr_pc2,'-o', color='chartreuse', ms=2, label='feb')
    plt.plot(rotated_data[:,0], rotated_data[:,1],'-o', color='chartreuse', ms=2, label='feb')
    for i in range(0,len_mar-1):#len(text31)-1):  
        plt.annotate(text31[i], (rotated_data[:,0][i], rotated_data[:,1][i] + 0.2), fontsize=5)
# ###

    # rotated_data = rotate_vector(form_data(jan_arr_pc1, jan_arr_pc2), -10)
    plt.plot([feb_arr_pc1[-1], mar_arr_pc1[0]], [feb_arr_pc2[-1], mar_arr_pc2[0]], '-', color='blue', ms=2)
#ok
    rotated_data = rotate_vector(form_data(mar_arr_pc1, mar_arr_pc2), 0)
    # plt.plot(mar_arr_pc1, mar_arr_pc2, '-o', color='blue', ms=2, label='mar')
    plt.plot(rotated_data[:,0], rotated_data[:,1], '-o', color='blue', ms=2, label='mar')
###

    for i in range(0,len_mar-1):#len(text31)-1):  
        plt.annotate(text31[i], (rotated_data[:,0][i], rotated_data[:,1][i] + 0.2), fontsize=5)
    plt.annotate("FINISH", (mar_arr_pc1[-1], mar_arr_pc2[-1] + 0.2), fontsize=8)
    plt.legend()
    # print("coordinate of the las point:", mar_arr_pc1[-1], mar_arr_pc2[-1])
#add Circle
    circle1 = plt.Circle((0, 0), 1, color='k', fill=False, linewidth=1)
    ax.plot([0, 1], [0, 1], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([1, 0], [0, 1], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([0, 1], [0.5, 0.5], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([0.5, 0.5], [0, 1], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    # plt.text(-0.6, 0, "Weak MJO", fontsize=10, weight='bold')
    ax.add_artist(circle1)

    is_exist = os.path.exists(pc_png_file)
    if not is_exist:
        os.makedirs(pc_png_file)
    fig_name = os.path.basename(pc_png_file)


    # plt.savefig(f'{pc_png_file}/{fig_name}_{inverse1}_{inverse2}.png')
    saveFig(pc_png_file, False)
    plt.close()

#===========================================================
def drawPc(pc_text_file: Path, pc_png_file: Path, inverse1 = 1, inverse2 = 1): #only one month
    pc1 = []
    pc2 = []
    # days = np.arange(0, 93, 1, dtype=int)
    #  PCs2     PsCs
    print("path pc: ", pc_text_file)
    with open(pc_text_file) as f1:
        next(f1)
        for line in f1:
            if line != ['']:
                line = line.split(",")
                pc1.append(inverse1 * float(line[0]))
                pc2.append(inverse2 * float(line[1]))

    fig, ax = plt.subplots()
    fig.set_figheight(6)
    fig.set_figwidth(6)
    jan_arr_pc1 = pc1[0:31]
    jan_arr_pc2 = pc2[0:31]
    text31 = np.arange(1, 32, 1, dtype=int)
    len_mar = 28 #TODO check if month is march
    text28 = np.arange(1, 29, 1, dtype=int)
    plt.xlim(-4, 4)
    plt.ylim(-4, 4)
    plt.xlabel('$RMM1$')
    plt.ylabel('$RMM2$')

    rotated_data = rotate_vector(form_data(jan_arr_pc1, jan_arr_pc2), 0) # 0 -> -10
    plt.plot(rotated_data[:, 0], rotated_data[:, 1], '-o', color='red', ms=2, label='jan', linewidth=2)

    plt.annotate("START", (rotated_data[:,0][0], rotated_data[:,1][0] + 0.2), fontsize=8)

    for i in range(1,len(text31)):
        plt.annotate(text31[i], (rotated_data[:,0][i], rotated_data[:,1][i] + 0.2), fontsize=5)
    plt.legend()
    # print("coordinate of the last point:", jan_arr_pc1[-1], jan_arr_pc2[-1])
# Add Circle
    circle1 = plt.Circle((0, 0), 1, color='k', fill=False, linewidth=1)
    ax.plot([0, 1], [0, 1], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([1, 0], [0, 1], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([0, 1], [0.5, 0.5], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([0.5, 0.5], [0, 1], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    # plt.text(-0.6, 0, "Weak MJO", fontsize=10, weight='bold')
    ax.add_artist(circle1)

    #is_exist = os.path.exists(pc_png_file)
    #if not is_exist:
    #    os.makedirs(pc_png_file)
    #fig_name = os.path.basename(pc_png_file)
    #plt.savefig(f'{pc_png_file}/{fig_name}_{inverse1}_{inverse2}.png')
    
    # plt.savefig(f'{pc_png_file}.png')
    saveFig(pc_png_file, False)
    plt.close()

#===========================================================
def drawAllPc(pc_text_file: Path, pc_png_file: Path, members_number): #ALL participants of the ensemble
    print("drawAllPc")
    print("path pc: ", pc_text_file)

    pc1_all_memb, pc2_all_memb = getMembersPc(pc_text_file, members_number)
    memb_to_draw = len(pc1_all_memb) - 1 # memb_to_draw; do not draw the last element - it's era
# Prepare figure fields
    # fig, ax = plt.subplots(layout="constrained")
    plt.rc('legend', fontsize=9) # legend font size 
    fig, ax = plt.subplots()
    fig.set_figheight(6)
    fig.set_figwidth(6)
    plt.xlim(-4, 4)
    plt.ylim(-4, 4)
    plt.xlabel('$RMM1$')
    plt.ylabel('$RMM2$')
    text31 = np.arange(1, 32, 1, dtype=int)

# Find 25-75 and middle
    elements_pc1_max, elements_pc2_max, elements_pc1_min, elements_pc2_min, pc1_mean_arr, pc2_mean_arr = getMaxMinMedMemb(pc1_all_memb, pc2_all_memb, memb_to_draw)
# Draw max/min lines    
    # ax.plot(elements_pc1_max, elements_pc2_max, marker='.', color='green', ms=2.5, label='jan', linewidth=1.2)
    # ax.plot(elements_pc1_min, elements_pc2_min, marker='.', color='blue', ms=2.5, label='jan', linewidth=1.2)

# Draw middle line
    plt.plot(pc1_mean_arr, pc2_mean_arr, marker='.', color='black', ms=2.5, linewidth=1.2, label='Mean')

# Draw unpertubed ansamble member - (unshifted member)
    plt.plot(pc1_all_memb[0], pc2_all_memb[0], marker='.', color='red', ms=2.5, linewidth=1.2, label='Unperturbed')
# Draw last ansamble member - (controll ERA)
    plt.plot(pc1_all_memb[-1], pc2_all_memb[-1], marker='.', color='blue', ms=2.5, linewidth=1.2, label='Era5')

# Draw all, but one members 
    for i in range(0, memb_to_draw):
        jan_arr_pc1 = pc1_all_memb[i]
        jan_arr_pc2 = pc2_all_memb[i]
    #Fill area between all members
        ax.fill(
            np.append(pc1_mean_arr, jan_arr_pc1[::-1]),
            np.append(pc2_mean_arr, jan_arr_pc2[::-1]),
            "lightgrey"
        )
    #Fill 50% middle
    ax.fill(
        np.append(elements_pc1_min, elements_pc1_max[::-1]),
        np.append(elements_pc2_min, elements_pc2_max[::-1]),
        "darkgray"
    )
    ax.fill(
        np.append(elements_pc1_min, pc1_mean_arr[::-1]),
        np.append(elements_pc2_min, pc2_mean_arr[::-1]),
        "darkgray"
    )
    ax.fill(
        np.append(elements_pc1_max, pc1_mean_arr[::-1]),
        np.append(elements_pc2_max, pc2_mean_arr[::-1]),
        "darkgray"
    )     
# Add dashed lines
    ax.plot([0, 0.414], [0, 0.414], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([0.586, 1], [0.586, 1], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([1, 0.586], [0, 0.414], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([0.414, 0], [0.586, 1], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([0, 0.375], [0.5, 0.5], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([0.625, 1], [0.5, 0.5], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([0.5, 0.5], [0, 0.375], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
    ax.plot([0.5, 0.5], [0.625, 1], transform=ax.transAxes, color='k', linewidth = 0.5, ls="--" )
# Add Circle
    circle1 = plt.Circle((0, 0), 1, color='k', fill=False, linewidth=1)
    ax.add_artist(circle1)
# Add phase numbers
    ax.text(-3.5, -1.5, "1", fontsize=12)
    ax.text(-1.5, -3.5, "2", fontsize=12)
    ax.text(1.5, -3.5, "3", fontsize=12)
    ax.text(3.5, -1.5, "4", fontsize=12)
    ax.text(3.5, 1.5, "5", fontsize=12)
    ax.text(1.5, 3.5, "6", fontsize=12)
    ax.text(-1.5, 3.5, "7", fontsize=12)
    ax.text(-3.5, 1.5, "8", fontsize=12)
# Add subtitles X,Y
    ax.text(-3.8, -0.6, "West. Hem. \n and Africa", rotation = 90, fontsize=12)
    ax.text(-0.5, 3.5, "Western\n Pacific", rotation = 0, rotation_mode='anchor', fontsize=12)
    ax.text(3.4, -0.5, " Maritime\nContinent", rotation = -90, fontsize=12)
    ax.text(-0.4, -3.9, "Indian\nOcean", rotation = 0, fontsize=12)
# Add date number
    plt.annotate("START", (pc1_mean_arr[0], pc2_mean_arr[0] + 0.1), fontsize=6)
    for i in range(3, len(text31), 3): # Mark every 3 day as number
        plt.annotate(text31[i], (pc1_mean_arr[i], pc2_mean_arr[i] + 0.1), fontsize=5)

    legend = plt.legend( loc = "upper right", frameon = False) # No legend shift
    plt.tick_params(top = True, right = True, axis='both', direction='in')

# Save into the file
    saveFig(pc_png_file)
    
#===========================================================
def drawCor(pc_text_file: Path, pc_png_file: Path, members_number):
    print("drawCor")
    print("path pc: ", pc_text_file)
    pc1_all_memb, pc2_all_memb = getMembersPc(pc_text_file, members_number)
    memb_to_draw = len(pc1_all_memb) - 1 # memb_to_draw; do not draw the last element - it's era
    corr = findCor(pc1_all_memb, pc2_all_memb, memb_to_draw)

    fig, ax = plt.subplots()
    plt.xlabel('days')
    plt.ylabel('Correlation')
    plt.axhline(y=0.0, color='black', linestyle='-', linewidth=0.5)
    plt.plot(np.arange(len(corr)), corr, marker='.', color='black', ms=2.5, linewidth=1.2) # -1: start from the second day of plav 
    saveFig(pc_png_file)
    saveMetric("Cor", corr, pc_png_file)

#===========================================================
def drawRmse(pc_text_file: Path, pc_png_file: Path, members_number): # TODO devide on find and draw functions 
    print("drawRmse")
    print("path pc: ", pc_text_file)
    pc1_all_memb, pc2_all_memb = getMembersPc(pc_text_file, members_number)
    memb_to_draw = len(pc1_all_memb) - 1 # memb_to_draw; do not draw the last element - it's era
    rmse = findRmse(pc1_all_memb, pc2_all_memb, memb_to_draw)

    fig, ax = plt.subplots()
    plt.xlabel('days')
    plt.ylabel('RMSE')
    plt.axhline(y=0.0, color='black', linestyle='-', linewidth=0.5)
    plt.plot(np.arange(len(rmse)), rmse, marker='.', color='black', ms=2.5,  linewidth=1.2)
    saveFig(pc_png_file)
    saveMetric("RMSE", rmse, pc_png_file)

#===========================================================
def drawMsss(pc_text_file: Path, pc_png_file: Path, members_number): 
    print("drawMsss")
    print("path pc: ", pc_text_file)
    pc1_all_memb, pc2_all_memb = getMembersPc(pc_text_file, members_number)
    memb_to_draw = len(pc1_all_memb) - 1 # memb_to_draw; do not draw the last element - it's era
    msss = findMsss(pc1_all_memb, pc2_all_memb, memb_to_draw)

    fig, ax = plt.subplots()
    plt.xlabel('days')
    plt.ylabel('MSSS')
    plt.axhline(y=0.0, color='black', linestyle='-', linewidth=0.5)
    plt.plot(np.arange(len(msss)), msss, marker='.', color='black', ms=2.5, linewidth=1.2)
    saveFig(pc_png_file)
    saveMetric("MSSS", msss, pc_png_file)

#===========================================================
def saveFig(pc_png_file, make_dir=False):
    fig_path = ""
    fig_name = os.path.basename(pc_png_file)
    if make_dir:
        exists = os.path.exists(pc_png_file)
        if not exists:
           os.makedirs(pc_png_file)
        fig_path = f'{pc_png_file}/{fig_name}.png'
    else:
        fig_path = f'{pc_png_file}.png'
    plt.savefig(fig_path)
    plt.close()
    print("Graph saved: ", fig_path)





































































#WH04 eofs
# 2.01374E-02, 9.58089E-03
# 2.12196E-02, 1.13089E-02
# 2.25498E-02, 1.41104E-02
# 2.46027E-02, 1.42294E-02
# 2.60908E-02, 1.10940E-02
# 2.79008E-02, 9.94701E-03
# 3.22317E-02, 8.09211E-03
# 3.46887E-02, 1.17310E-02
# 3.45138E-02, 1.24562E-02
# 3.38656E-02, 1.06626E-02
# 3.03988E-02, 1.15963E-02
# 2.56968E-02, 1.32034E-02
# 1.78561E-02, 1.99815E-02
# 1.02285E-02, 2.74937E-02
# 4.53011E-03, 3.04519E-02
# 6.14469E-03, 2.32545E-02
# 1.32819E-02, 1.74511E-02
# 1.40669E-02, 1.59341E-02
# 1.46942E-02, 1.57556E-02
# 1.56117E-02, 1.62830E-02
# 1.83624E-02, 1.90520E-02
# 1.81316E-02, 2.42762E-02
# 1.77290E-02, 3.11741E-02
# 1.81438E-02, 3.76878E-02
# 1.72264E-02, 4.50025E-02
# 1.39292E-02, 5.14328E-02
# 9.30649E-03, 5.90102E-02
# 4.57712E-03, 6.69728E-02
# -7.17312E-04, 7.64230E-02
# -4.57682E-03, 8.57754E-02
# -6.70664E-03, 9.10636E-02
# -1.00101E-02, 9.56418E-02
# -1.37183E-02, 0.102474
# -1.96981E-02, 0.106402
# -2.58130E-02, 0.106235
# -3.37611E-02, 0.104352
# -4.08956E-02, 9.89848E-02
# -4.79849E-02, 9.14328E-02
# -4.84854E-02, 8.22559E-02
# -4.47961E-02, 6.87424E-02
# -4.30943E-02, 5.69484E-02
# -5.05088E-02, 4.12172E-02
# -5.35225E-02, 3.67422E-02
# -5.47074E-02, 3.36825E-02
# -5.52229E-02, 2.64891E-02
# -5.79831E-02, 1.38642E-02
# -6.78749E-02, -2.14241E-03
# -7.17353E-02, -5.42421E-03
# -7.03387E-02, -7.21298E-03
# -6.93571E-02, -7.38861E-03
# -7.07544E-02, -9.91884E-03
# -7.35821E-02, -1.44488E-02
# -7.51303E-02, -1.76688E-02
# -7.30513E-02, -2.10441E-02
# -7.15953E-02, -2.16920E-02
# -7.16052E-02, -2.48268E-02
# -7.18432E-02, -2.88845E-02
# -6.99083E-02, -3.01265E-02
# -6.88868E-02, -3.34528E-02
# -6.41975E-02, -3.59306E-02
# -5.97874E-02, -3.35921E-02
# -5.52623E-02, -3.03340E-02
# -5.01976E-02, -3.18772E-02
# -4.36187E-02, -3.13677E-02
# -3.66819E-02, -3.16697E-02
# -3.04950E-02, -3.06539E-02
# -2.56779E-02, -3.03318E-02
# -1.78308E-02, -2.88865E-02
# -1.22115E-02, -2.91738E-02
# -8.87276E-03, -2.79465E-02
# -6.00968E-03, -2.73986E-02
# -2.60972E-03, -2.70587E-02
# 3.90224E-05, -2.52093E-02
# 1.84028E-03, -2.31686E-02
# 3.84327E-03, -2.17293E-02
# 5.17609E-03, -1.99558E-02
# 5.36145E-03, -1.91789E-02
# 6.19168E-03, -1.73411E-02
# 6.77228E-03, -1.71970E-02
# 7.41259E-03, -1.56240E-02
# 7.86270E-03, -1.33725E-02
# 8.15142E-03, -1.11757E-02
# 7.70560E-03, -1.06421E-02
# 5.56621E-03, -1.04113E-02
# 1.93326E-03, -9.83380E-03
# -2.42119E-04, -1.01611E-02
# -1.65450E-03, -9.85301E-03
# -3.36905E-03, -1.13636E-02
# -3.89634E-03, -1.14898E-02
# -2.99886E-03, -1.11339E-02
# -3.39545E-03, -1.07688E-02
# -3.94282E-03, -1.00396E-02
# -4.37929E-03, -8.31864E-03
# -3.89380E-03, -7.19017E-03
# -4.04911E-03, -7.66026E-03
# -2.72953E-03, -8.22100E-03
# -1.35433E-03, -8.41961E-03
# 1.54235E-03, -9.25039E-03
# 3.86602E-03, -9.09037E-03
# 6.87731E-03, -6.99287E-03
# 9.98862E-03, -6.23772E-03
# 1.27367E-02, -4.92925E-03
# 1.55295E-02, -4.45328E-03
# 1.73478E-02, -3.24854E-03
# 1.88295E-02, -2.28958E-03
# 2.12428E-02, -1.38109E-03
# 2.27043E-02, -1.14546E-03
# 2.36280E-02, -1.28836E-03
# 2.45448E-02, -1.90807E-03
# 2.57113E-02, -2.67862E-03
# 2.09384E-02, -4.16100E-03
# 1.76776E-02, -3.71043E-03
# 2.07567E-02, 2.72118E-03
# 1.81543E-02, 3.41484E-03
# 1.92714E-02, 1.92593E-03
# 1.56624E-02, -2.18031E-03
# 1.39781E-02, -6.32215E-03
# 1.54408E-02, -8.98941E-03
# 1.55888E-02, -9.66138E-03
# 1.59456E-02, -7.56295E-03
# 1.60208E-02, -6.82583E-03
# 1.69180E-02, -4.73672E-03
# 1.75327E-02, -4.05507E-03
# 1.76317E-02, -8.58132E-04
# 1.74300E-02, 1.08304E-05
# 1.84341E-02, -2.40619E-03
# 2.00613E-02, -4.34712E-03
# 1.87954E-02, -5.81352E-03
# 1.44050E-02, -6.49319E-03
# 1.20837E-02, -6.90525E-03
# 1.01869E-02, -8.86570E-03
# 9.26868E-03, -9.80415E-03
# 9.37289E-03, -1.04891E-02
# 1.03832E-02, -1.07919E-02
# 1.17766E-02, -1.18044E-02
# 1.34736E-02, -1.07099E-02
# 1.50654E-02, -9.47473E-03
# 1.58359E-02, -7.84316E-03
# 1.60454E-02, -7.36479E-03
# 1.65487E-02, -6.41768E-03
# 1.60455E-02, -3.92210E-03
# 1.67569E-02, -2.65673E-04
# 1.85898E-02, 3.96705E-03
# 1.81330E-02, 6.38851E-03
# -7.69157E-03, -2.34452E-02
# -6.98243E-03, -2.37286E-02
# -6.62455E-03, -2.42598E-02
# -6.62111E-03, -2.57541E-02
# -6.64728E-03, -2.78498E-02
# -6.06547E-03, -2.94054E-02
# -4.38712E-03, -3.03809E-02
# -1.90436E-03, -3.19434E-02
# 3.73514E-04, -3.42800E-02
# 1.90309E-03, -3.59705E-02
# 3.69470E-03, -3.65111E-02
# 7.26594E-03, -3.76269E-02
# 1.23041E-02, -4.02691E-02
# 1.66557E-02, -4.20170E-02
# 1.90799E-02, -3.99291E-02
# 2.11441E-02, -3.51674E-02
# 2.51961E-02, -3.20557E-02
# 3.11204E-02, -3.23623E-02
# 3.64453E-02, -3.34973E-02
# 3.97054E-02, -3.29368E-02
# 4.24366E-02, -3.18463E-02
# 4.70069E-02, -3.25456E-02
# 5.35115E-02, -3.46512E-02
# 5.99051E-02, -3.59585E-02
# 6.47376E-02, -3.57852E-02
# 6.84882E-02, -3.52198E-02
# 7.21129E-02, -3.46471E-02
# 7.55184E-02, -3.31987E-02
# 7.82485E-02, -3.04558E-02
# 8.08046E-02, -2.66977E-02
# 8.40393E-02, -2.17509E-02
# 8.76444E-02, -1.50198E-02
# 9.02979E-02, -7.02443E-03
# 9.15534E-02, 8.85274E-04
# 9.22151E-02, 8.40301E-03
# 9.24828E-02, 1.61540E-02
# 9.12462E-02, 2.36249E-02
# 8.82696E-02, 2.94164E-02
# 8.56379E-02, 3.41187E-02
# 8.54632E-02, 4.06856E-02
# 8.65953E-02, 5.03799E-02
# 8.59436E-02, 6.04260E-02
# 8.28683E-02, 6.75964E-02
# 7.99892E-02, 7.26156E-02
# 7.90847E-02, 7.86174E-02
# 7.82669E-02, 8.61369E-02
# 7.48994E-02, 9.26036E-02
# 6.93828E-02, 9.63852E-02
# 6.41287E-02, 9.87894E-02
# 5.97114E-02, 0.101292
# 5.45226E-02, 0.103404
# 4.78804E-02, 0.104572
# 4.13055E-02, 0.105997
# 3.59102E-02, 0.108846
# 3.07764E-02, 0.111869
# 2.46864E-02, 0.112703
# 1.80825E-02, 0.110945
# 1.21473E-02, 0.108157
# 6.87356E-03, 0.105394
# 1.16650E-03, 0.102463
# -5.44650E-03, 9.94906E-02 
# -1.23998E-02, 9.74651E-02
# -1.90376E-02, 9.66793E-02
# -2.51422E-02, 9.60792E-02
# -3.07719E-02, 9.48586E-02
# -3.61533E-02, 9.36616E-02
# -4.15277E-02, 9.33611E-02
# -4.68901E-02, 9.35477E-02
# -5.16167E-02, 9.29809E-02
# -5.52519E-02, 9.12897E-02
# -5.80781E-02, 8.89774E-02
# -6.07702E-02, 8.64298E-02
# -6.34341E-02, 8.34015E-02
# -6.58179E-02, 7.98574E-02
# -6.80831E-02, 7.62572E-02
# -7.08260E-02, 7.29790E-02
# -7.42776E-02, 6.99297E-02
# -7.80657E-02, 6.68393E-02
# -8.16845E-02, 6.36088E-02
# -8.48312E-02, 6.02340E-02
# -8.72401E-02, 5.65644E-02
# -8.87773E-02, 5.25721E-02
# -8.95861E-02, 4.84972E-02
# -8.99703E-02, 4.45474E-02
# -9.00481E-02, 4.06455E-02
# -8.98451E-02, 3.66346E-02
# -8.95526E-02, 3.26256E-02
# -8.92548E-02, 2.88074E-02
# -8.87724E-02, 2.52221E-02
# -8.80212E-02, 2.16650E-02
# -8.73167E-02, 1.80298E-02
# -8.70046E-02, 1.43985E-02
# -8.68854E-02, 1.09248E-02
# -8.66139E-02, 7.71490E-03
# -8.63483E-02, 4.84922E-03
# -8.64178E-02, 2.34623E-03
# -8.66975E-02, 1.10995E-04
# -8.69166E-02, -1.98180E-03
# -8.72618E-02, -3.94542E-03
# -8.78698E-02, -5.59749E-03
# -8.79444E-02, -6.75630E-03
# -8.65207E-02, -7.48939E-03
# -8.39534E-02, -8.07443E-03
# -8.15094E-02, -8.63512E-03
# -7.94092E-02, -8.97245E-03
# -7.66289E-02, -8.80599E-03
# -7.29821E-02, -8.24406E-03
# -6.98060E-02, -7.87414E-03
# -6.79594E-02, -8.17657E-03
# -6.64851E-02, -8.86797E-03
# -6.42112E-02, -9.15007E-03
# -6.13989E-02, -8.66971E-03
# -5.86163E-02, -7.97850E-03
# -5.51112E-02, -7.78810E-03
# -5.00799E-02, -8.03620E-03
# -4.48506E-02, -8.15831E-03
# -4.16956E-02, -7.99570E-03
# -4.09135E-02, -8.07151E-03
# -4.07608E-02, -8.75679E-03
# -4.03254E-02, -9.75870E-03
# -4.04758E-02, -1.06593E-02
# -4.14793E-02, -1.15414E-02
# -4.19738E-02, -1.25294E-02
# -4.11025E-02, -1.32587E-02
# -3.99144E-02, -1.32845E-02
# -3.94365E-02, -1.29509E-02
# -3.86569E-02, -1.30156E-02
# -3.59715E-02, -1.36162E-02
# -3.18139E-02, -1.41890E-02
# -2.81682E-02, -1.45138E-02
# -2.59671E-02, -1.51912E-02
# -2.44760E-02, -1.66178E-02
# -2.30017E-02, -1.83296E-02
# -2.17156E-02, -1.96762E-02
# -2.06420E-02, -2.06360E-02
# -1.91016E-02, -2.14353E-02
# -1.68365E-02, -2.19605E-02
# -1.45803E-02, -2.21473E-02
# -1.30754E-02, -2.24057E-02
# -1.21898E-02, -2.30720E-02
# -1.13337E-02, -2.36528E-02
# -1.03485E-02, -2.35880E-02
# -9.40524E-03, -2.31723E-02
# -8.53862E-03, -2.31141E-02
# -1.22800E-02, 7.91631E-02
# -1.37469E-02, 7.90005E-02
# -1.54980E-02, 7.88534E-02
# -1.74376E-02, 7.89558E-02
# -1.90510E-02, 7.87191E-02
# -2.00425E-02, 7.74737E-02
# -2.08478E-02, 7.56332E-02
# -2.21674E-02, 7.42641E-02
# -2.40613E-02, 7.36642E-02
# -2.59248E-02, 7.33340E-02
# -2.74498E-02, 7.31754E-02
# -2.90222E-02, 7.36516E-02
# -3.09363E-02, 7.45217E-02
# -3.27655E-02, 7.47221E-02
# -3.40371E-02, 7.40168E-02
# -3.52318E-02, 7.37468E-02
# -3.74099E-02, 7.50394E-02
# -4.08110E-02, 7.71997E-02
# -4.45613E-02, 7.86181E-02
# -4.78055E-02, 7.87603E-02
# -5.05966E-02, 7.82321E-02
# -5.33830E-02, 7.74238E-02
# -5.61654E-02, 7.61246E-02
# -5.85784E-02, 7.43177E-02
# -6.04649E-02, 7.23194E-02
# -6.19197E-02, 7.00339E-02
# -6.30260E-02, 6.69886E-02
# -6.39154E-02, 6.31553E-02
# -6.48608E-02, 5.90989E-02
# -6.59653E-02, 5.51053E-02
# -6.68296E-02, 5.07950E-02
# -6.70171E-02, 4.57437E-02
# -6.66264E-02, 4.00045E-02
# -6.59283E-02, 3.38417E-02
# -6.47346E-02, 2.74063E-02
# -6.28534E-02, 2.08336E-02
# -6.10320E-02, 1.42543E-02
# -6.04559E-02, 7.66961E-03
# -6.10782E-02, 1.09225E-03
# -6.14025E-02, -5.23726E-03
# -6.04273E-02, -1.12136E-02
# -5.90740E-02, -1.72968E-02
# -5.87639E-02, -2.38690E-02
# -5.92178E-02, -3.01866E-02
# -5.86868E-02, -3.49345E-02
# -5.62655E-02, -3.78971E-02
# -5.28085E-02, -4.03500E-02
# -4.94552E-02, -4.33452E-02
# -4.62145E-02, -4.64284E-02
# -4.24591E-02, -4.86450E-02
# -3.80782E-02, -5.00033E-02
# -3.34394E-02, -5.11831E-02
# -2.87290E-02, -5.23248E-02
# -2.39256E-02, -5.29911E-02
# -1.92251E-02, -5.30197E-02
# -1.48561E-02, -5.26386E-02
# -1.05703E-02, -5.18305E-02
# -5.87696E-03, -5.04277E-02
# -7.67209E-04, -4.87145E-02
# 4.27069E-03, -4.72683E-02
# 8.95735E-03, -4.61335E-02
# 1.35548E-02, -4.47949E-02
# 1.83650E-02, -4.29802E-02
# 2.32447E-02, -4.09365E-02
# 2.78099E-02, -3.88102E-02
# 3.18479E-02, -3.64719E-02
# 3.54006E-02, -3.40076E-02
# 3.85788E-02, -3.18638E-02
# 4.15054E-02, -3.01844E-02
# 4.43063E-02, -2.85471E-02
# 4.69735E-02, -2.65874E-02
# 4.93299E-02, -2.44549E-02
# 5.12493E-02, -2.23750E-02
# 5.28702E-02, -2.02376E-02
# 5.45275E-02, -1.79119E-02
# 5.64457E-02, -1.55990E-02
# 5.85617E-02, -1.34939E-02
# 6.06407E-02, -1.14276E-02
# 6.24901E-02, -9.13373E-03
# 6.41243E-02, -6.65026E-03
# 6.56639E-02, -4.18182E-03
# 6.70932E-02, -1.77488E-03
# 6.81587E-02, 6.09018E-04
# 6.86882E-02, 2.92501E-03
# 6.88776E-02, 5.18573E-03
# 6.90932E-02, 7.60343E-03
# 6.94483E-02, 1.03284E-02
# 6.97894E-02, 1.32870E-02
# 7.00489E-02, 1.64629E-02
# 7.03865E-02, 2.00893E-02
# 7.08682E-02, 2.42832E-02
# 7.13362E-02, 2.87332E-02
# 7.17237E-02, 3.30737E-02
# 7.22182E-02, 3.73579E-02
# 7.29299E-02, 4.18128E-02
# 7.36012E-02, 4.62510E-02
# 7.39705E-02, 5.02042E-02
# 7.41624E-02, 5.34924E-02
# 7.44402E-02, 5.63000E-02
# 7.47549E-02, 5.88074E-02
# 7.47830E-02, 6.09455E-02
# 7.43817E-02, 6.26960E-02
# 7.36134E-02, 6.41730E-02
# 7.24196E-02, 6.55986E-02
# 7.06768E-02, 6.72265E-02
# 6.84931E-02, 6.91885E-02
# 6.60702E-02, 7.12013E-02
# 6.31681E-02, 7.26767E-02
# 5.93634E-02, 7.33663E-02
# 5.49676E-02, 7.36165E-02
# 5.10964E-02, 7.36208E-02
# 4.84687E-02, 7.27544E-02
# 4.64915E-02, 7.02890E-02
# 4.41226E-02, 6.66258E-02
# 4.13382E-02, 6.30563E-02
# 3.90102E-02, 6.03652E-02
# 3.75236E-02, 5.82434E-02
# 3.61749E-02, 5.62297E-02
# 3.43044E-02, 5.44859E-02
# 3.22515E-02, 5.33236E-02
# 3.07502E-02, 5.26080E-02
# 2.98098E-02, 5.20874E-02
# 2.88038E-02, 5.19043E-02
# 2.74610E-02, 5.23358E-02
# 2.61657E-02, 5.33471E-02
# 2.52067E-02, 5.47808E-02
# 2.42053E-02, 5.66722E-02
# 2.25907E-02, 5.90521E-02
# 2.02882E-02, 6.16297E-02
# 1.77335E-02, 6.40005E-02
# 1.52805E-02, 6.60821E-02
# 1.29144E-02, 6.79986E-02
# 1.04478E-02, 6.98162E-02
# 7.83532E-03, 7.15819E-02
# 5.18663E-03, 7.33821E-02
# 2.64540E-03, 7.51242E-02
# 3.00452E-04, 7.64421E-02
# -1.83757E-03, 7.71948E-02
# -3.75601E-03, 7.76564E-02
# -5.41928E-03, 7.80945E-02
# -6.83637E-03, 7.84187E-02
# -8.13856E-03, 7.85314E-02
# -9.49339E-03, 7.86706E-02
# -1.08943E-02, 7.89785E-02
