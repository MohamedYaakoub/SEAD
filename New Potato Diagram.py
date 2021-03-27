#draw potato diagram of BAE RJ85:
import numpy as np
import matplotlib.pyplot as plt
#MEGA-BEUN, get old plot, in light gray, under new
######### START POTATO DIAGRAM.py #########
######### INPUT PARAMETERS ###########
#CGs of parts
x_lemac = 11.45 #m
mac = 3.17 #m

x_OEW_lemac = 0.25 #%Lemac   #it can be between 0.25 and 0.3
x_OEW_ac = x_OEW_lemac*mac + x_lemac

x_FrontHold_ac = 7.99 #m
x_BackHold_ac = 16.66 #m

x_1stseat = 7.138 #m  #STILL FAKE
deltacgseat = 31*0.0254 #m  (inches to m)
n_row = 17     #2 last rows are missing 2 aisle people
x_lastseat = x_1stseat + (n_row*deltacgseat) #m

x_tankwing = 12.494 #m
x_tankcenter = 11.504 #m
x_tankaux = 13.781 #m

#Weights
W_OEW = 24820 #kg
W_FrontHold_max = 1519.34 #kg
W_BackHold_max = 1505.97 #kg
W_pax = 95 #kg

#W_fuel_max = 9147.84 #kg
W_fuel_max_wings = 16160*0.45359237 #kg
W_fuel_max_center = 4160*0.45359237 #kg  #nominal tanks are 9217 kg which is almost fuel max
W_fuel_max_aux = 2064 *0.45359237 #kg
#this gives tot of 10153 kg

########################################
#CARGO LOADING
#Back hold 1st
cg_back1 = []
W_back1 = []
for W_cargo in np.arange(0,W_BackHold_max +0.01, 0.01):
    W_total = W_OEW + W_cargo
    cg = ((x_OEW_ac*W_OEW) + (W_cargo*x_BackHold_ac ))/(W_total)
    cg_back1.append(cg)
    W_back1.append(W_total)
# print(cg_back1)
# print((W_back1))

#Front hold 2nd
cg_front2 = []
W_front2 = []
for W_cargo in np.arange(0,W_FrontHold_max +0.01, 0.01):
    W_total = W_OEW + W_BackHold_max + W_cargo  #back hold already loaded
    cg = ((x_OEW_ac*W_OEW) + (x_BackHold_ac*W_BackHold_max)+ (W_cargo*x_FrontHold_ac ))/(W_total)
    cg_front2.append(cg)
    W_front2.append(W_total)
# print(cg_front2)
# print((W_front2))

#Front hold 1st
cg_front1 = []
W_front1 = []
for W_cargo in np.arange(0,W_FrontHold_max + 0.01, 0.01):
    W_total = W_OEW + W_cargo
    cg = ((x_OEW_ac*W_OEW) + (W_cargo*x_FrontHold_ac ))/(W_total)
    cg_front1.append(cg)
    W_front1.append(W_total)
# print(cg_front1)
# print((W_front1))

#Back hold 2nd
cg_back2 = []
W_back2 = []
for W_cargo in np.arange(0,W_BackHold_max + 0.01, 0.01):
    W_total = W_OEW + W_FrontHold_max + W_cargo  #back hold already loaded
    cg = ((x_OEW_ac*W_OEW) + (x_BackHold_ac*W_cargo)+ (W_FrontHold_max*x_FrontHold_ac ))/(W_total)
    cg_back2.append(cg)
    W_back2.append(W_total)
# print(cg_back2)
# print((W_back2))

#PLOT CARGO POTATO DIAGRAM
# plt.axhline(W_OEW, color = 'red', label = 'OEW')
# plt.plot(cg_back1, W_back1, color = 'c', label = 'Back hold 1st')
# plt.plot(cg_front2, W_front2,  color = 'yellowgreen', label = 'Front hold 2nd')
# plt.plot(cg_front1, W_front1, color = 'yellowgreen', label = 'Front hold 1st')
# plt.plot(cg_back2, W_back2,  color = 'c', label = 'Back hold 2nd')
# plt.xlabel('Xcg (m)')
# plt.ylabel("Total Weight (kg)")
# plt.title('Potato diagram')
# plt.legend(loc= 'best')
# plt.show()

#Check for errors, get next initial values

W_withcargo = W_front2[-1]  #now initial weight
cg_withcargo = cg_back2[-1] #now initial cg

#PAX LOADING - window-rule

#Window rows 1st
#A - from front to back
cg_pax_windowA = [cg_withcargo]
W_pax_windowA = [W_withcargo]
W_pax_total = 0

#for x in np.arange(x_1stseat, x_lastseat + deltacgseat, deltacgseat):
for x in np.linspace(x_1stseat, x_lastseat, n_row):
    W_pax_total = W_pax_total + W_pax * 2 #increase W of pax group by 2 pax
    x_pax = (x_1stseat + x)/2 #cg of pax group

    W_total = W_withcargo + W_pax_total #2 new pax each time

    cg = ((cg_withcargo*W_withcargo) + (x_pax*W_pax_total))/(W_total)
    cg_pax_windowA.append(cg)
    W_pax_windowA.append(W_total)

#B - from back to front
cg_pax_windowB = [cg_withcargo]
W_pax_windowB = [W_withcargo]
W_pax_total = 0

#for x in np.arange(x_lastseat, x_1stseat - deltacgseat, -deltacgseat):
for x in np.linspace(x_lastseat, x_1stseat, n_row):
    W_pax_total = W_pax_total + W_pax*2 #increase W of pax group by 2 pax
    x_pax = x_lastseat - ((x_lastseat - x)/2) #cg of pax group
    #print(x_pax)
    W_total = W_withcargo + W_pax_total #2 new pax each time

    cg = ((cg_withcargo*W_withcargo) + (x_pax*W_pax_total))/(W_total)
    cg_pax_windowB.append(cg)
    W_pax_windowB.append(W_total)

W_withcargoandwindow = W_pax_windowA[-1]  #now initial weight
cg_withcargoandwindow = cg_pax_windowA[-1] #now initial cg

#Middle rows 2nd
#A - from front to back
cg_pax_middleA = [cg_withcargoandwindow]
W_pax_middleA = [W_withcargoandwindow]
W_pax_total = 0
#for x in np.arange(x_1stseat, x_lastseat + deltacgseat, deltacgseat):
for x in np.linspace(x_1stseat, x_lastseat, n_row):
    W_pax_total = W_pax_total + W_pax * 2 #increase W of pax group by 2 pax
    x_pax = (x_1stseat + x)/2 #cg of pax group

    W_total = W_withcargoandwindow + W_pax_total #2 new pax each time

    cg = ((cg_withcargoandwindow*W_withcargoandwindow) + (x_pax*W_pax_total))/(W_total)
    cg_pax_middleA.append(cg)
    W_pax_middleA.append(W_total)

#B - from back to front
cg_pax_middleB = [cg_withcargoandwindow]
W_pax_middleB = [W_withcargoandwindow]
W_pax_total = 0
#print(np.arange(x_lastseat, x_1stseat + deltacgseat, -deltacgseat))
#for x in np.arange(x_lastseat, x_1stseat - deltacgseat, -deltacgseat):
for x in np.linspace(x_lastseat, x_1stseat, n_row):
    W_pax_total = W_pax_total + W_pax * 2 #increase W of pax group by 2 pax
    x_pax = x_lastseat - ((x_lastseat - x)/2) #cg of pax group
    #print(x_pax)
    W_total = W_withcargoandwindow + W_pax_total #2 new pax each time

    cg = ((cg_withcargoandwindow*W_withcargoandwindow) + (x_pax*W_pax_total))/(W_total)
    cg_pax_middleB.append(cg)
    W_pax_middleB.append(W_total)

W_withcargowindowandmiddle = W_pax_middleA[-1]  #now initial weight
cg_withcargowindowandmiddle = cg_pax_middleA[-1] #now initial cg

#Aisle rows 2nd
#A - from front to back
cg_pax_aisleA = [cg_withcargowindowandmiddle]
W_pax_aisleA = [W_withcargowindowandmiddle]
W_pax_total = 0
#for x in np.arange(x_1stseat, x_lastseat + deltacgseat, deltacgseat):
rows = np.linspace(x_1stseat, x_lastseat , n_row)
for x in rows[:-2]:  #only 15 rows
   
    W_pax_total = W_pax_total + W_pax * 2 #increase W of pax group by 2 pax
    x_pax = (x_1stseat + x)/2 #cg of pax group

    W_total = W_withcargowindowandmiddle + W_pax_total #2 new pax each time

    cg = ((cg_withcargowindowandmiddle*W_withcargowindowandmiddle) + (x_pax*W_pax_total))/(W_total)
    cg_pax_aisleA.append(cg)
    W_pax_aisleA.append(W_total)
for x in rows[-2:]:  #only 15 rows
    
    W_pax_total = W_pax_total + W_pax #only 1 pax in last 2 rows
    x_pax = (x_1stseat + x)/2 #cg of pax group

    W_total = W_withcargowindowandmiddle + W_pax_total #2 new pax each time

    cg = ((cg_withcargowindowandmiddle*W_withcargowindowandmiddle) + (x_pax*W_pax_total))/(W_total)
    cg_pax_aisleA.append(cg)
    W_pax_aisleA.append(W_total)


#B - from back to front
cg_pax_aisleB = [cg_withcargowindowandmiddle]
W_pax_aisleB = [W_withcargowindowandmiddle]
W_pax_total = 0
#print(np.arange(x_lastseat, x_1stseat + deltacgseat, -deltacgseat))
#for x in np.arange(x_lastseat, x_1stseat - deltacgseat, -deltacgseat):
rows_inv = np.linspace(x_lastseat ,x_1stseat, n_row)

for x in rows_inv[:2]:  #1st 2 rows = last 2 rows = 1pax
    print(x)
    W_pax_total = W_pax_total + W_pax
    x_pax = x_lastseat - ((x_lastseat - x)/2) #cg of pax group
    #print(x_pax)
    W_total = W_withcargowindowandmiddle + W_pax_total #2 new pax each time

    cg = ((cg_withcargowindowandmiddle*W_withcargowindowandmiddle) + (x_pax*W_pax_total))/(W_total)
    cg_pax_aisleB.append(cg)
    W_pax_aisleB.append(W_total)
for x in rows_inv[2:]:  #rest of rows
    print(x)
    W_pax_total = W_pax_total + W_pax*2
    x_pax = x_lastseat - ((x_lastseat - x)/2) #cg of pax group
    #print(x_pax)
    W_total = W_withcargowindowandmiddle + W_pax_total #2 new pax each time

    cg = ((cg_withcargowindowandmiddle*W_withcargowindowandmiddle) + (x_pax*W_pax_total))/(W_total)
    cg_pax_aisleB.append(cg)
    W_pax_aisleB.append(W_total)


W_afterpax = W_pax_aisleA[-1]  #now initial weight
cg_afterpax = cg_pax_aisleA[-1] #now initial cg

#FUEL LOADING

#1 - WING TANKS
cg_fuelwing = []
W_fuelwing = []
for W in np.arange(0,W_fuel_max_wings +0.01, 0.01):
    W_total = W_afterpax + W #back hold already loaded
    cg = ((cg_afterpax*W_afterpax) + (x_tankwing*W))/(W_total)
    cg_fuelwing.append(cg)
    W_fuelwing.append(W_total)


W_afterwing = W_fuelwing[-1]  #now initial weight
cg_afterwing = cg_fuelwing[-1] #now initial cg

#2 - Center TANKS
cg_fuelcenter = []
W_fuelcenter = []

for W in np.arange(0,W_fuel_max_center +0.01, 0.01):
    W_total = W_afterwing + W
    #print(W_total)
    cg = ((cg_afterwing*W_afterwing) + (x_tankcenter*W))/(W_total)
    cg_fuelcenter.append(cg)
    W_fuelcenter.append(W_total)


W_aftercenter = W_fuelcenter[-1]  #now initial weight
cg_aftercenter = cg_fuelcenter[-1] #now initial cg

#2 -Aux TANKS
cg_fuelaux = []
W_fuelaux = []

for W in np.arange(0,W_fuel_max_aux +0.01, 0.01):
    W_total = W_aftercenter  + W
    #print(W_total)
    cg = ((cg_aftercenter *W_aftercenter ) + (x_tankaux*W))/(W_total)
    cg_fuelaux.append(cg)
    W_fuelaux.append(W_total)



# W_final = W_fuelwing[-1]  #now initial weight
# cg_final = cg_fuelwing[-1] #now initial cg


#transformm into %mac
values = [cg_front2, cg_back2, cg_back1,cg_front1,cg_pax_aisleA,cg_pax_aisleB ,
          cg_pax_middleA,cg_pax_middleB, cg_pax_windowA,cg_pax_windowB, cg_fuelwing, cg_fuelcenter,cg_fuelaux]


for A in values:
    for i in range(0, len(A)):
        A[i] = (A[i] - x_lemac)/ mac


max_cg = [max(cg_front2), max(cg_back2), max(cg_back1), max(cg_front1), max(cg_pax_aisleA), max(cg_pax_aisleB) ,
          max(cg_pax_middleA), max(cg_pax_middleB), max(cg_pax_windowA),max(cg_pax_windowB), max(cg_fuelwing), max(cg_fuelcenter), max(cg_fuelaux)]
most_aft_cg_margin = max(max_cg) + max(max_cg)*0.02  #2% margin

min_cg = [min(cg_front2), min(cg_back2), min(cg_back1), min(cg_front1), min(cg_pax_aisleA), min(cg_pax_aisleB) ,
          min(cg_pax_middleA), min(cg_pax_middleB), min(cg_pax_windowA),min(cg_pax_windowB), min(cg_fuelwing), min(cg_fuelcenter),  min( cg_fuelcenter)]
most_foward_cg_margin = min(min_cg) - min(min_cg)*0.02  #2% margin


#plots
plt.axhline(W_fuelaux[-1] , color = 'lightgrey',linestyle = "dashdot")

plt.axvline(most_aft_cg_margin, color = 'darkgrey')
plt.axvline(most_foward_cg_margin, color = 'darkgrey')

plt.plot(cg_fuelwing, W_fuelwing, color = 'lightgrey')
plt.plot(cg_fuelcenter, W_fuelcenter, color = 'lightgrey')
plt.plot(cg_fuelaux, W_fuelaux, color = 'lightgrey')

plt.axhline(W_afterpax, color = 'lightgrey',linestyle = "dashdot")

plt.plot(cg_pax_aisleA, W_pax_aisleA, color = 'lightgrey')
plt.plot(cg_pax_aisleB, W_pax_aisleB, color = 'lightgrey', linestyle = "dashed")
plt.plot(cg_pax_middleA, W_pax_middleA, color = 'lightgrey')
plt.plot(cg_pax_middleB, W_pax_middleB,color = 'lightgrey', linestyle = "dashed")
plt.plot(cg_pax_windowA, W_pax_windowA, color = 'lightgrey')
plt.plot(cg_pax_windowB, W_pax_windowB, color = 'lightgrey', linestyle = "dashed")

plt.plot(cg_back1, W_back1, color = 'lightgrey')
plt.plot(cg_front2, W_front2, color = 'lightgrey', linestyle = "dashed")
plt.plot(cg_front1, W_front1,color = 'lightgrey')
plt.plot(cg_back2, W_back2, color = 'lightgrey',  linestyle = "dashed")

plt.axhline(W_OEW, color = 'lightgrey',linestyle = "dashdot")


#plt.xlabel('c.g. (% mac)', fontsize = 15)
#plt.ylabel("Total Weight (kg)", fontsize = 15)
#plt.title('Loading diagram', fontsize = 15)
#plt.legend(loc= 'best', fontsize = 12)
#plt.show()



























######### START NEW POTATO ###########

######### INPUT PARAMETERS ###########
#CGs of parts
x_lemac = 11.45 #m
mac = 3.17 #m

x_OEW_lemac = 0.25 #%Lemac   #it can be between 0.25 and 0.3
x_OEW_ac = x_OEW_lemac*mac + x_lemac - 0.6  #Moved 60 cm forward

x_FrontHold_ac = 7.99 #m
x_BackHold_ac = 16.66 #m

x_1stseat = 7.138 #m  #STILL FAKE
deltacgseat = 31*0.0254 #m  (inches to m)
n_row = 17     #2 last rows are missing 2 aisle people
x_lastseat = x_1stseat + (n_row*deltacgseat) #m

x_tankwing = 12.494 #m
x_tankcenter = 11.504 #m
x_tankaux = 13.781 #m

#Weights
W_OEW = 22338 #kg   #reduced by 10%
W_FrontHold_max = 3381.5 #kg    #Increased with 75% of 'spare' weight
W_BackHold_max = 2126.5 #kg     #Increased with 25% of 'spare' weight
W_pax = 95 #kg

#W_fuel_max = 9147.84 #kg
W_fuel_max_wings = 16160*0.45359237 #kg
W_fuel_max_center = 4160*0.45359237 #kg  #nominal tanks are 9217 kg which is almost fuel max
W_fuel_max_aux = 2064 *0.45359237 #kg
#this gives tot of 10153 kg

########################################
#CARGO LOADING
#Back hold 1st
cg_back1 = []
W_back1 = []
for W_cargo in np.arange(0,W_BackHold_max +0.01, 0.01):
    W_total = W_OEW + W_cargo
    cg = ((x_OEW_ac*W_OEW) + (W_cargo*x_BackHold_ac ))/(W_total)
    cg_back1.append(cg)
    W_back1.append(W_total)
# print(cg_back1)
# print((W_back1))

#Front hold 2nd
cg_front2 = []
W_front2 = []
for W_cargo in np.arange(0,W_FrontHold_max +0.01, 0.01):
    W_total = W_OEW + W_BackHold_max + W_cargo  #back hold already loaded
    cg = ((x_OEW_ac*W_OEW) + (x_BackHold_ac*W_BackHold_max)+ (W_cargo*x_FrontHold_ac ))/(W_total)
    cg_front2.append(cg)
    W_front2.append(W_total)
# print(cg_front2)
# print((W_front2))

#Front hold 1st
cg_front1 = []
W_front1 = []
for W_cargo in np.arange(0,W_FrontHold_max + 0.01, 0.01):
    W_total = W_OEW + W_cargo
    cg = ((x_OEW_ac*W_OEW) + (W_cargo*x_FrontHold_ac ))/(W_total)
    cg_front1.append(cg)
    W_front1.append(W_total)
# print(cg_front1)
# print((W_front1))

#Back hold 2nd
cg_back2 = []
W_back2 = []
for W_cargo in np.arange(0,W_BackHold_max + 0.01, 0.01):
    W_total = W_OEW + W_FrontHold_max + W_cargo  #back hold already loaded
    cg = ((x_OEW_ac*W_OEW) + (x_BackHold_ac*W_cargo)+ (W_FrontHold_max*x_FrontHold_ac ))/(W_total)
    cg_back2.append(cg)
    W_back2.append(W_total)
# print(cg_back2)
# print((W_back2))

#PLOT CARGO POTATO DIAGRAM
# plt.axhline(W_OEW, color = 'red', label = 'OEW')
# plt.plot(cg_back1, W_back1, color = 'c', label = 'Back hold 1st')
# plt.plot(cg_front2, W_front2,  color = 'yellowgreen', label = 'Front hold 2nd')
# plt.plot(cg_front1, W_front1, color = 'yellowgreen', label = 'Front hold 1st')
# plt.plot(cg_back2, W_back2,  color = 'c', label = 'Back hold 2nd')
# plt.xlabel('Xcg (m)')
# plt.ylabel("Total Weight (kg)")
# plt.title('Potato diagram')
# plt.legend(loc= 'best')
# plt.show()

#Check for errors, get next initial values

print('Final cg after cargo loading is', cg_front2[-1], cg_back2[-1]  )
print('Final W is', W_front2[-1], W_back2[-1]  )
W_withcargo = W_front2[-1]  #now initial weight
cg_withcargo = cg_back2[-1] #now initial cg
print('Diff in cg:', cg_front2[-1] - cg_back2[-1])
print('Diff in W:', W_front2[-1] - W_back2[-1])
print()
#PAX LOADING - window-rule

#Window rows 1st
print(np.linspace(x_lastseat, x_1stseat, n_row))
#A - from front to back
cg_pax_windowA = [cg_withcargo]
W_pax_windowA = [W_withcargo]
W_pax_total = 0

#for x in np.arange(x_1stseat, x_lastseat + deltacgseat, deltacgseat):
for x in np.linspace(x_1stseat, x_lastseat, n_row):
    W_pax_total = W_pax_total + W_pax * 2 #increase W of pax group by 2 pax
    x_pax = (x_1stseat + x)/2 #cg of pax group

    W_total = W_withcargo + W_pax_total #2 new pax each time

    cg = ((cg_withcargo*W_withcargo) + (x_pax*W_pax_total))/(W_total)
    cg_pax_windowA.append(cg)
    W_pax_windowA.append(W_total)

#B - from back to front
cg_pax_windowB = [cg_withcargo]
W_pax_windowB = [W_withcargo]
W_pax_total = 0

#for x in np.arange(x_lastseat, x_1stseat - deltacgseat, -deltacgseat):
for x in np.linspace(x_lastseat, x_1stseat, n_row):
    W_pax_total = W_pax_total + W_pax*2 #increase W of pax group by 2 pax
    x_pax = x_lastseat - ((x_lastseat - x)/2) #cg of pax group
    #print(x_pax)
    W_total = W_withcargo + W_pax_total #2 new pax each time

    cg = ((cg_withcargo*W_withcargo) + (x_pax*W_pax_total))/(W_total)
    cg_pax_windowB.append(cg)
    W_pax_windowB.append(W_total)

print('cg after cargo + window is', cg_pax_windowA[-1], cg_pax_windowB[-1]  )
print('W after cargo + window is', W_pax_windowA[-1], W_pax_windowB[-1]  )
print('Diff in cg:', cg_pax_windowA[-1] - cg_pax_windowB[-1])
print('Diff in W:', W_pax_windowA[-1] - W_pax_windowB[-1])
print()
W_withcargoandwindow = W_pax_windowA[-1]  #now initial weight
cg_withcargoandwindow = cg_pax_windowA[-1] #now initial cg

#Middle rows 2nd
#A - from front to back
cg_pax_middleA = [cg_withcargoandwindow]
W_pax_middleA = [W_withcargoandwindow]
W_pax_total = 0
#for x in np.arange(x_1stseat, x_lastseat + deltacgseat, deltacgseat):
for x in np.linspace(x_1stseat, x_lastseat, n_row):
    W_pax_total = W_pax_total + W_pax * 2 #increase W of pax group by 2 pax
    x_pax = (x_1stseat + x)/2 #cg of pax group

    W_total = W_withcargoandwindow + W_pax_total #2 new pax each time

    cg = ((cg_withcargoandwindow*W_withcargoandwindow) + (x_pax*W_pax_total))/(W_total)
    cg_pax_middleA.append(cg)
    W_pax_middleA.append(W_total)

#B - from back to front
cg_pax_middleB = [cg_withcargoandwindow]
W_pax_middleB = [W_withcargoandwindow]
W_pax_total = 0
#print(np.arange(x_lastseat, x_1stseat + deltacgseat, -deltacgseat))
#for x in np.arange(x_lastseat, x_1stseat - deltacgseat, -deltacgseat):
for x in np.linspace(x_lastseat, x_1stseat, n_row):
    W_pax_total = W_pax_total + W_pax * 2 #increase W of pax group by 2 pax
    x_pax = x_lastseat - ((x_lastseat - x)/2) #cg of pax group
    #print(x_pax)
    W_total = W_withcargoandwindow + W_pax_total #2 new pax each time

    cg = ((cg_withcargoandwindow*W_withcargoandwindow) + (x_pax*W_pax_total))/(W_total)
    cg_pax_middleB.append(cg)
    W_pax_middleB.append(W_total)

print('cg after cargo + window +middle is', cg_pax_middleA[-1], cg_pax_middleB[-1]  )
print('W after cargo + window +middle is', W_pax_middleA[-1], W_pax_middleB[-1]  )
print('Diff in cg:', cg_pax_middleA[-1] - cg_pax_middleB[-1])
print('Diff in W:', W_pax_middleA[-1] - W_pax_middleB[-1])
print()
W_withcargowindowandmiddle = W_pax_middleA[-1]  #now initial weight
cg_withcargowindowandmiddle = cg_pax_middleA[-1] #now initial cg

#Aisle rows 2nd
#A - from front to back
cg_pax_aisleA = [cg_withcargowindowandmiddle]
W_pax_aisleA = [W_withcargowindowandmiddle]
W_pax_total = 0
#for x in np.arange(x_1stseat, x_lastseat + deltacgseat, deltacgseat):
rows = np.linspace(x_1stseat, x_lastseat , n_row)
for x in rows[:-2]:  #only 15 rows
    print(x)
    W_pax_total = W_pax_total + W_pax * 2 #increase W of pax group by 2 pax
    x_pax = (x_1stseat + x)/2 #cg of pax group

    W_total = W_withcargowindowandmiddle + W_pax_total #2 new pax each time

    cg = ((cg_withcargowindowandmiddle*W_withcargowindowandmiddle) + (x_pax*W_pax_total))/(W_total)
    cg_pax_aisleA.append(cg)
    W_pax_aisleA.append(W_total)
for x in rows[-2:]:  #only 15 rows
    print(x)
    W_pax_total = W_pax_total + W_pax #only 1 pax in last 2 rows
    x_pax = (x_1stseat + x)/2 #cg of pax group

    W_total = W_withcargowindowandmiddle + W_pax_total #2 new pax each time

    cg = ((cg_withcargowindowandmiddle*W_withcargowindowandmiddle) + (x_pax*W_pax_total))/(W_total)
    cg_pax_aisleA.append(cg)
    W_pax_aisleA.append(W_total)


#B - from back to front
cg_pax_aisleB = [cg_withcargowindowandmiddle]
W_pax_aisleB = [W_withcargowindowandmiddle]
W_pax_total = 0
#print(np.arange(x_lastseat, x_1stseat + deltacgseat, -deltacgseat))
#for x in np.arange(x_lastseat, x_1stseat - deltacgseat, -deltacgseat):
rows_inv = np.linspace(x_lastseat ,x_1stseat, n_row)
print(rows_inv)
for x in rows_inv[:2]:  #1st 2 rows = last 2 rows = 1pax
    print(x)
    W_pax_total = W_pax_total + W_pax
    x_pax = x_lastseat - ((x_lastseat - x)/2) #cg of pax group
    #print(x_pax)
    W_total = W_withcargowindowandmiddle + W_pax_total #2 new pax each time

    cg = ((cg_withcargowindowandmiddle*W_withcargowindowandmiddle) + (x_pax*W_pax_total))/(W_total)
    cg_pax_aisleB.append(cg)
    W_pax_aisleB.append(W_total)
for x in rows_inv[2:]:  #rest of rows
    print(x)
    W_pax_total = W_pax_total + W_pax*2
    x_pax = x_lastseat - ((x_lastseat - x)/2) #cg of pax group
    #print(x_pax)
    W_total = W_withcargowindowandmiddle + W_pax_total #2 new pax each time

    cg = ((cg_withcargowindowandmiddle*W_withcargowindowandmiddle) + (x_pax*W_pax_total))/(W_total)
    cg_pax_aisleB.append(cg)
    W_pax_aisleB.append(W_total)

print('cg after cargo + window +middle +aisle is', cg_pax_aisleA[-1], cg_pax_aisleB[-1]  )
print('W after cargo + window +middle +aisle is', W_pax_aisleA[-1], W_pax_aisleB[-1]  )
print('Diff in cg:', cg_pax_aisleA[-1] - cg_pax_aisleB[-1])
print('Diff in W:', W_pax_aisleA[-1] - W_pax_aisleB[-1])

W_afterpax = W_pax_aisleA[-1]  #now initial weight
cg_afterpax = cg_pax_aisleA[-1] #now initial cg

#FUEL LOADING

#1 - WING TANKS
cg_fuelwing = []
W_fuelwing = []
for W in np.arange(0,W_fuel_max_wings +0.01, 0.01):
    W_total = W_afterpax + W #back hold already loaded
    cg = ((cg_afterpax*W_afterpax) + (x_tankwing*W))/(W_total)
    cg_fuelwing.append(cg)
    W_fuelwing.append(W_total)

print('cg after wing fuel is', cg_fuelwing[-1])
print('W after wing fuel is', W_fuelwing[-1] )

W_afterwing = W_fuelwing[-1]  #now initial weight
cg_afterwing = cg_fuelwing[-1] #now initial cg

#2 - Center TANKS
cg_fuelcenter = []
W_fuelcenter = []

for W in np.arange(0,W_fuel_max_center +0.01, 0.01):
    W_total = W_afterwing + W
    #print(W_total)
    cg = ((cg_afterwing*W_afterwing) + (x_tankcenter*W))/(W_total)
    cg_fuelcenter.append(cg)
    W_fuelcenter.append(W_total)

print('cg after fuel is', cg_fuelcenter[-1])
print('W after fuel is', W_fuelcenter[-1] )

W_aftercenter = W_fuelcenter[-1]  #now initial weight
cg_aftercenter = cg_fuelcenter[-1] #now initial cg

#2 -Aux TANKS
cg_fuelaux = []
W_fuelaux = []

for W in np.arange(0,W_fuel_max_aux +0.01, 0.01):
    W_total = W_aftercenter  + W
    #print(W_total)
    cg = ((cg_aftercenter *W_aftercenter ) + (x_tankaux*W))/(W_total)
    cg_fuelaux.append(cg)
    W_fuelaux.append(W_total)

print('cg after aux  fuel is', cg_fuelaux[-1])
print('W after aux fuel is', W_fuelaux[-1] )


# W_final = W_fuelwing[-1]  #now initial weight
# cg_final = cg_fuelwing[-1] #now initial cg


#transformm into %mac
values = [cg_front2, cg_back2, cg_back1,cg_front1,cg_pax_aisleA,cg_pax_aisleB ,
          cg_pax_middleA,cg_pax_middleB, cg_pax_windowA,cg_pax_windowB, cg_fuelwing, cg_fuelcenter,cg_fuelaux]


for A in values:
    for i in range(0, len(A)):
        A[i] = (A[i] - x_lemac)/ mac


max_cg = [max(cg_front2), max(cg_back2), max(cg_back1), max(cg_front1), max(cg_pax_aisleA), max(cg_pax_aisleB) ,
          max(cg_pax_middleA), max(cg_pax_middleB), max(cg_pax_windowA),max(cg_pax_windowB), max(cg_fuelwing), max(cg_fuelcenter), max(cg_fuelaux)]
most_aft_cg_margin = max(max_cg) + max(max_cg)*0.02  #2% margin

min_cg = [min(cg_front2), min(cg_back2), min(cg_back1), min(cg_front1), min(cg_pax_aisleA), min(cg_pax_aisleB) ,
          min(cg_pax_middleA), min(cg_pax_middleB), min(cg_pax_windowA),min(cg_pax_windowB), min(cg_fuelwing), min(cg_fuelcenter),  min( cg_fuelcenter)]
most_foward_cg_margin = min(min_cg) - min(min_cg)*0.02  #2% margin

print()
print('CG most foward is', min(min_cg), '%,  with margin: ', most_foward_cg_margin , '%' )
print('CG most aft is', max(max_cg) ,'%,  with margin: ', most_aft_cg_margin , '%')

#plots
plt.axhline(W_fuelaux[-1] , color = 'gold',linestyle = "dashdot", label = 'MTOW')

plt.axvline(most_aft_cg_margin, color = 'tomato', label = 'most_aft')
plt.axvline(most_foward_cg_margin, color = 'tomato', label = 'most_foward')

plt.plot(cg_fuelwing, W_fuelwing, color = 'grey',label = 'Fuel Wing Tanks')
plt.plot(cg_fuelcenter, W_fuelcenter, color = 'darkgrey',label = 'Fuel Center Tank')
plt.plot(cg_fuelaux, W_fuelaux, color = 'gainsboro',label = 'Fuel Center Tank')

plt.axhline(W_afterpax, color = 'orange',linestyle = "dashdot", label = 'MZFW')

plt.plot(cg_pax_aisleA, W_pax_aisleA, color = 'plum',label = 'Aisle seats: front to back')
plt.plot(cg_pax_aisleB, W_pax_aisleB, color = 'plum', linestyle = "dashed",label = 'Aisle seats: back to front')
plt.plot(cg_pax_middleA, W_pax_middleA, color = 'lightskyblue',label = 'Middle seats: front to back')
plt.plot(cg_pax_middleB, W_pax_middleB,color = 'lightskyblue', linestyle = "dashed", label = 'Middle seats: back to front')
plt.plot(cg_pax_windowA, W_pax_windowA, color = 'green', label = 'Window seats: front to back')
plt.plot(cg_pax_windowB, W_pax_windowB, color = 'green', linestyle = "dashed",label = 'Window seats: back to front')

plt.plot(cg_back1, W_back1, color = 'c', label = 'Back hold 1st')
plt.plot(cg_front2, W_front2, color = 'yellowgreen', linestyle = "dashed", label = 'Front hold 2nd')
plt.plot(cg_front1, W_front1,color = 'yellowgreen', label = 'Front hold 1st')
plt.plot(cg_back2, W_back2, color = 'c',  linestyle = "dashed", label = 'Back hold 2nd')

plt.axhline(W_OEW, color = 'red',linestyle = "dashdot", label = 'OEW')


plt.xlabel('c.g. (% mac)', fontsize = 15)
plt.ylabel("Total Weight (kg)", fontsize = 15)
plt.title('Loading diagram', fontsize = 15)
plt.legend(loc= 'best', fontsize = 12)
plt.show()
