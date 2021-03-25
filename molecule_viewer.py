import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
#import matplotlib.transforms as mtransforms
#from matplotlib import rc

#usage: pyton molecule_viewer.py n
# n = 0: plot molecule
# n > 0: plot molecule with basis connections

basis=int(sys.argv[1])

# Axes min/max
lim=5

#systems=['nh3+ar']
systems=['h2o+h']
pips=['66']

atom_list = []
x_list = []
y_list = []
z_list = []
c_list = [] # atom colors
s_list = [] # atom sizes

points_list = []
bf_list = []
rms_list = []
cv_list = []
diff_list = []
div_list = []
des_list = []
plots = []

#i=0 # system
for system in systems:
    xyzfile='minimum.xyz'
    print("loading in "+xyzfile)
    try:
        with open(xyzfile,"r") as f:
            k=0
            for a in f:
                line = a.split()
                if k == 0:
                    natoms = int(line[0])
                elif k == 1:
                    minE = float(line[2])
                elif k >= 2:
                    atom_list.append(str(line[0]))
                    x_list.append(float(line[1]))
                    y_list.append(float(line[2]))
                    z_list.append(float(line[3]))
                k += 1
#            print(k)
    except IOError:
        print("No file "+xyzfile+" found")

    if basis > 0:
        for pip in pips:
            filename=system+'_'+pip+'_subsets.dat'
            try:
                with open(filename,"r") as f:
                    k=0
                    for a in f:
                        if k==0:
                            subset = a.split()
                            points = int(subset[0])
                            bf = int(subset[1])
                            rms = float(subset[2])
                            cv = float(subset[3])
                            diff = float(subset[4])
                            div = float(subset[5])
                            points_list.append(points)
                            bf_list.append(bf)
                            rms_list.append(rms)
                            cv_list.append(cv)
                            diff_list.append(diff)
                            div_list.append(div)
                            print("# of basis functions = ",bf)
                        elif k<=bf:
                            subset = re.split('( ||) ',a)
#                            print("Subset = ",subset)
                            des_list.append(str(subset[0]))
                        k += 1
            except IOError:
                print("No file "+filename+" found")
#    s=system.split('+')
#    i=i+1 # system

#print(des_list)

#fig = plt.figure(figsize=plt.figaspect(0.5)*1.5) #Adjusts the aspect ratio and enlarges the figure (text does not enlarge)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

natoms=int(len(atom_list))

print("Atoms: "+str(natoms))
print(atom_list)
npairs=int(natoms*(natoms-1)/2)
pair_list = [0]*npairs
index_list = np.zeros((npairs, 2))
#print(npairs)

k=0
for i in range(natoms):
    for j in range(i+1,len(atom_list)):
        pair_list[k] = atom_list[i]+atom_list[j]
        index_list[k,0] = i
        index_list[k,1] = j
        k+=1

print("Pairs: "+str(npairs))
print(pair_list)
#print(index_list)

unique_pairs = []
for pair in pair_list:
    if pair not in unique_pairs:
        unique_pairs.append(pair)

print("Unique Pairs: "+str(len(unique_pairs)))
print(unique_pairs)

for atom in atom_list:
    if atom == 'N':
        c_list.append('blue')
        s_list.append(150)
    elif atom == 'H':
        c_list.append('red')
        s_list.append(100)
    elif atom == 'Ar':
        c_list.append('orange')
        s_list.append(180)
    else:
        c_list.append('gray')
        s_list.append(100)

xs = x_list
ys = y_list
zs = z_list
cs = c_list
ss = s_list
ax.scatter(xs, ys, zs, c=cs, s=ss)
i = 0
for x, y, z in zip(xs, ys, zs):
    label = str(atom_list[i])
    ax.text(x, y, z, label)
    i += 1

#ax.set_box_aspect([np.ptp(i) for i in x_list])
#ax.set_box_aspect([1,1,1])

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xlim(-lim,lim)
ax.set_ylim(-lim,lim)
ax.set_zlim(-lim,lim)

def key_event(e):
    global curr_pos

    if e.key == "right":
        curr_pos = curr_pos + 1
    elif e.key == "left":
        curr_pos = curr_pos - 1
    else:
        return
    curr_pos = curr_pos % len(plots)

    ax.cla()
    ax.plot(plots[curr_pos][0], plots[curr_pos][1])
    fig.canvas.draw()

if basis == 0:
    plt.show()
elif basis > 0:
#    for b in range(len(des_list)):
    temp=des_list[basis-1].split('(')
#    temp=des_list[b-1].split('(')
#    print(temp)
    temp2=temp[1].split(')')
#    print(temp2)
    bas=temp2[0]
#    print(bas)
    bas2 = []
    bas2[:] = bas
    print("Basis:")
    print(bas2)
    # Create vectors:
    k = 0
    for i in bas2:
        if int(i) > 0:
            xplt = []
            yplt = []
            zplt = []
            print("Index = ",k)
            xplt.append(xs[int(index_list[k,0])])
            yplt.append(ys[int(index_list[k,0])])
            zplt.append(zs[int(index_list[k,0])])
            xplt.append(xs[int(index_list[k,1])])
            yplt.append(ys[int(index_list[k,1])])
            zplt.append(zs[int(index_list[k,1])])
            ax.plot(xplt, yplt, zplt)
        k += 1
    plt.title("Basis: "+str(basis))
#    fig.canvas.mpl_connect('key_press_event', key_event)
#    ax = fig.add_subplot(111)
    plt.show()
else:
    plt.show()

#plt.title(s[0]+"+"+s[1])
#plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
#plt.tight_layout()
#plt.subplots_adjust(right=0.7)
#plt.show()
