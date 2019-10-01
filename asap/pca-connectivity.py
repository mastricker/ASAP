#!/usr/bin/python3

import numpy as np
import argparse
import matplotlib.pyplot as plt
from matplotlib import cm
from asaplib.pca import pca
from asaplib.plot import *
from asaplib.io import str2bool
from ase.io import read

def main(fmat, fxyz, fconnect, ftags, fcolor, colorscol, prefix, scale, pca_d, pc1, pc2, adtext):

    # if it has been computed before we can simply load it
    try:
        desc = np.genfromtxt(fmat, dtype=float)
    except:
        raise ValueError('Cannot load the descriptor matrix')

    print("loaded",fmat)
    if ftags != 'none':
        tags = np.loadtxt(ftags, dtype="str")
        ndict = len(tags)

    # scale & center
    if (scale):
        from sklearn.preprocessing import StandardScaler
        desc = StandardScaler().fit_transform(desc) # normalizing the features

    # main thing
    proj = pca(desc,pca_d)

    # save
    np.savetxt(prefix+"-pca-d"+str(pca_d)+".coord", proj, fmt='%4.8f', header='low D coordinates of samples')

    # color scheme
    plotcolor, colorlabel = set_color_function(fcolor, fxyz, colorscol, len(proj))

    # connectivity information
    try:
        connect = np.genfromtxt(fconnect, dtype=int)
        print(np.shape(connect))
    except:
        raise ValueError('Cannot load the connectivity information')

    # make plot
    plot_styles.set_nice_font()
    #fig, ax = plt.subplots()

    fig, ax = plot_styles.plot_connectivity_map(proj[:,[pc1,pc2]], plotcolor, connect,
                xlabel='Princple Axis '+str(pc1), ylabel='Princple Axis '+str(pc2), 
                clabel=colorlabel, label=None,
                centers=None,
                psize=15,
                out_file='PCA_4_'+prefix+'.png', 
                title='PCA for: '+prefix, 
                show=False, cmap='gnuplot',
                remove_tick=False,
                rasterized = True,
                fontsize = 15,
                vmax = -168,
                vmin = None)

    fig.set_size_inches(18.5, 10.5)

    if ftags != 'none':
        texts = []
        for i in range(ndict):
            ax.scatter(proj[i, pc1],proj[i, pc2], marker='^', c='black')
            texts.append(ax.text(proj[i, pc1],proj[i, pc2], tags[i],
                         ha='center', va='center', fontsize=15, color='red'))
            #ax.annotate(tags[i], (proj[i,pc1], proj[i,pc2]))
        if (adtext):
            from adjustText import adjust_text
            adjust_text(texts,on_basemap=True,# only_move={'points':'', 'text':'x'},
                    expand_text=(1.01, 1.05), expand_points=(1.01, 1.05),
                   force_text=(0.03, 0.5), force_points=(0.01, 0.25),
                   ax=ax, precision=0.01,
                  arrowprops=dict(arrowstyle="-", color='black', lw=1,alpha=0.8))

    plt.show()
    fig.savefig('PCA_4_'+prefix+'-c-'+fcolor+'.png')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-fmat', type=str, required=True, help='Location of descriptor matrix file. You can use gen_descriptors.py to compute it.')
    parser.add_argument('-fxyz', type=str, default='none', help='Location of xyz file for reading the properties.')
    parser.add_argument('-fconnect', type=str, required=True, default='none', help='Location of file for reading connectivity information. format = [No.ts, No.min1, No,min2]')
    parser.add_argument('-tags', type=str, default='none', help='Location of tags for the first M samples')
    parser.add_argument('-colors', type=str, default='none', help='Location of a file that contains properties for all samples (N floats) used to color the scatter plot')
    parser.add_argument('--colorscolumn', type=int, default=0, help='The column number of the properties used for the coloring. Starts from 0.')
    parser.add_argument('--prefix', type=str, default='ASAP', help='Filename prefix')
    parser.add_argument('--scale', type=str2bool, nargs='?', const=True, default=True, help='Scale the coordinates (True/False). Scaling highly recommanded.')
    parser.add_argument('--d', type=int, default=10, help='number of the principle components to keep')
    parser.add_argument('--pc1', type=int, default=0, help='Plot the projection along which principle axes')
    parser.add_argument('--pc2', type=int, default=1, help='Plot the projection along which principle axes')
    parser.add_argument('--adjusttext', type=str2bool, nargs='?', const=True, default=False, help='Do you want to adjust the texts (True/False)?')

    args = parser.parse_args()

    main(args.fmat, args.fxyz, args.fconnect, args.tags, args.colors, args.colorscolumn, args.prefix, args.scale, args.d, args.pc1, args.pc2, args.adjusttext)

