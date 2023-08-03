## !/RHM-Lustre3.2/users/wg-slmod/rfadeev/miniconda_rmm/draw_rmm_env/bin/python
#!/usr/bin/python3




import numpy as np
import pandas as pd
import time as time_p
import sys 
import netCDF4 as netcdf4

import sys

from scipy.io import netcdf
from pathlib import Path

from painter import *
from nc_fig_paths import *
from eofs.multivariate.standard import MultivariateEof
from eofs.standard import Eof

# start_time = time_p.time() # process time 
# normalization factors from WMO letter 
variance_olr  =  15.1
variance_u200 =  4.81 
variance_u850 =  1.81
variance_olr_all =  15.1 
variance_u200_all = 4.81 
variance_u850_all = 1.81


#==================================

vars=[ "olr", "u850hpa", "u200hpa" ]


config = {
  "date":  "2014123000",
  "dirin": "",
  "dirout": "",
  "direra5": "",
  "slav": {
    "pattern": "erfclim-<var>-<year><month><day><hour>-<member>.nc"
  },
  "era5": {
    "dir": "",
    "pattern": "era5-<var>-day-2p5grid-79-0-01-mermV13-120.nc",
    "vars":    [ "olr", "u" ] # vars in netcdf files
  },
  "txt_out":  False
}
#==================================

inp_conf = {}
ln = 0; lv = 0;
for s in sys.argv:
  word = s.split("=")
  if len(word) == 1:
    continue
    print ("Error: '=' not found in attributes!")
    exit()
  elif len(word) == 2:
    print (word[0])
    inp_conf[word[0].strip()] = word[1].strip()
    ln = max(ln, len(word[0].strip()))
    lv = max(lv, len(word[1].strip()))
  else:
    print ("Error: to many '=' in attributes!")
    exit()

if True:
  print ("\nInput attributes:")
  for s in inp_conf:
    st = '   ' + f'{s:<{ln}}'.format(s,ln) + '   ' + f'{inp_conf[s]:<{lv}}'.format(inp_conf[s],lv)
    if s in config:
      config[s] = inp_conf[s]
      print ( st + '  >> config' )
    else:
      print ( st )
  

config["year"] =config["date"][0:4]
config["month"]=config["date"][4:6]
config["day"]  =config["date"][6:8]
config["hour"] =config["date"][8:10]

config["era5"]["dir"] = config["direra5"]
config["slav"]["dir"] = config["dirin"]

  
#==================================
all_members_dfs = [] # These to variebles are used to draw all members graph #Updated 10.07.2023
member_counter = 0  # #Updated 10.07.2023
print("RMM \n")
for h in range(24):
    # if h == 1:
      # break
    for m in range(100):
        # if m == 1:
          # break
        hour = str(h)
        if h < 10:
          hour = "0" + hour
        member = str(m)
        if m < 10:
          member = "0" + member
        
        # print("hour/member: " + hour + "/" + member)
        
        config["hour"] = str(hour)
        
        
        ncfile = {
          "slav": {},
          "era5": {}
        }
        
        data = {
          "slav": {},
          "era5": {}
        }
        
        scc=0
        for dt in [ "slav", "era5" ]:
          for var in vars:
            if dt == "era5":
              dv = var
            else:
              dv = ""
            s = config[dt]["pattern"]
            s = s.replace("<year>"  , str(config["year"]))
            s = s.replace("<month>" , str(config["month"]))
            s = s.replace("<day>"   , str(config["day"]))
            s = s.replace("<hour>"  , str(hour))
            s = s.replace("<var>"   , str(var))
            s = s.replace("<member>", str(member))
            ncfile[dt][var] = config[dt]["dir"] + "/" + dv + "/" + str(s) #Good for script

            if (os.path.isfile(ncfile[dt][var])):  
              # print (dt + " file found: " + ncfile[dt][var])
              f = netcdf4.Dataset(ncfile[dt][var], "r")
              for v in config["era5"]["vars"]:
                if v in f.variables:
                  data[dt][var] = np.array(f.variables[v])
                  scc = scc+1
                  break
            else:
              # print ("file NOT found for \n dt: " + dt + " \n var: " + var + " \n file: " + ncfile[dt][var])
              scc = -1
              break
              exit()
          if scc == -1:
            break
        if not scc == 2*len(vars):
          # print ("no data found!")
          continue

        member_counter += 1 # If we draw forecast -> we have the member
        ### Names of output files and graphs
        pc_path = config["dirout"] + "/mjo-rmm_" + config["year"]
        if not os.path.exists(pc_path):
           os.makedirs(pc_path)
        pc_name = pc_path + "/member_" + config["month"] + config["day"] + str(hour) + "-" + str(member)
        pcstxtfile = pc_name
        psc_png_file = pc_name

        #****** Calculate normalization factor  *******#
        # variance_olr = np.std(df_sst_olr)
        # variance_u200 = np.std(df_sst_u200)
        # variance_u850 = np.std(df_sst_u850)
        # # #facotrs std for all
        # variance_olr_all = np.std(df_olr_all)
        # variance_u200_all = np.std(df_u200_all)
        # variance_u850_all = np.std(df_u850_all)
        #********************************************#

        # print("variance_olr: ",variance_olr, " variance_u200: ", variance_u200, " variance_u850: ", variance_u850, "\n")
        # print("variance_olr_all: ",variance_olr_all, " variance_u200_all: ", variance_u200_all, " variance_u850_all: ", variance_u850_all, "\n")
        
        dt = "era5"
        solver = MultivariateEof([data[dt]["olr"]/variance_olr_all, data[dt]["u850hpa"]/variance_u850_all, data[dt]["u200hpa"]/variance_u200_all], center=True)

        # ##### !!! for WH04 _setEofWH04 in both standard.py
        eof1_list = solver.eofs(neofs=2, eofscaling=0)  #Mandatory step for correct projection on WH04 eofs
        ######################################################
        #******  Find PC  ******#  -1 if initial olr data are negative; 1 if olr data are positive
        dt = "slav"
        pseudo_pcs = np.squeeze(solver.projectField([-1*data[dt]["olr"]/variance_olr, data[dt]["u850hpa"]/variance_u850, data[dt]["u200hpa"]/variance_u200], eofscaling=1, neofs=2, weighted=False)) # same as neofs=2

        psc1, psc2 = [], []
        for pc in pseudo_pcs:
            psc1.append(pc[0])
            psc2.append(pc[1]) 

        df = pd.DataFrame({"PC1": psc1, "PC2": psc2})
        df.to_csv(f'{pcstxtfile}.txt', index=False, float_format="%.5f")
        all_members_dfs.append(df.head(31)) # The first 31 days of PCs #Updated 10.07.2023
        #******  Dwar graphs  ******#
        if True:
          drawPc(f'{pcstxtfile}.txt', psc_png_file) # The last two argument are 1 by ddefault
        else:
          drawPc_OLD(f'{pcstxtfile}.txt', psc_png_file) #The last two argument are 1 by ddefault
        # #****************************#
        #print("--- %s seconds totally ---" % (time_p.time() - start_time))
f.close() 

conf_date = config["year"] + config["month"] + config["day"] + str(hour) 
pcs_txt_file_all_memb = config["dirout"] + "/mjo-rmm_all_members"
with open(f'{pcs_txt_file_all_memb}.txt','w') as file: #Save all_members_dfs into file as dataframe  
    for dframe in all_members_dfs :
        dframe.to_csv(file, index=False, header=False)

psc_png_file_all_memb = config["dirout"] + "/mjo-rmm_all_members_" + config["year"] + config["month"] + config["day"]
drawAllPc(f'{pcs_txt_file_all_memb}.txt', f'{psc_png_file_all_memb}', member_counter)
###***Updated 31.07.2023***### 
psc_png_file_cor = config["dirout"] + "/mjo-rmm_cor_" + config["year"] + config["month"] + config["day"]
drawCor(f'{pcs_txt_file_all_memb}.txt', f'{psc_png_file_cor}', member_counter)

psc_png_file_rmse = config["dirout"] + "/mjo-rmm_rmse_" + config["year"] + config["month"] + config["day"]
drawRmse(f'{pcs_txt_file_all_memb}.txt', f'{psc_png_file_rmse}', member_counter)

psc_png_file_msss = config["dirout"] + "/mjo-rmm_msss_" + config["year"] + config["month"] + config["day"]
drawMsss(f'{pcs_txt_file_all_memb}.txt', f'{psc_png_file_msss}', member_counter)
##############################

print("Done")