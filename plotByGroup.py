#make one py file to plot up a figure...
#KLongnecker, 18 April 2017
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import palettable as pal
from Bio import SeqIO
from Bio.KEGG.REST import *
from Bio.KEGG.KGML import KGML_parser
from Bio.Graphics.KGML_vis import KGMLCanvas
from IPython.display import Image, HTML
import os
import pdb
from sklearn import preprocessing
import seaborn as sns

from IPython.core.debugger import Tracer
#os._exit(0)

def plotGroup(oneGroup,prunedBRITE,useCO,mtabPruned,oneStrain,scaleMM):
    #oneStrain = 'pmg'
    shortList = prunedBRITE.loc[(prunedBRITE['B']==oneGroup)] 
    onePath = shortList.loc[:,'map']
    onePath_ann = []
    for item in onePath:
        onePath_ann.append(oneStrain + item)

    gatherGroup = pd.DataFrame()
    for one in onePath_ann:
        #print(one)
        #not all pathways annotated in Prochlorococcus
        setKeep = 1
        try:
            kegg_get(one).read()
        except:
            #use the ko map if there is nothing species specific
            usePathway = 'ko' + one[3:8]
            setKeep = 0
            try:
                kegg_get(usePathway).read()
            except:
                pass
            
        if setKeep:
            usePathway = one
        
        try:
            mCpds = set(getCfrom_ko(usePathway))
        except:
            #no ko pathway either
            break
                          
        ProData= set(useCO)
        handh = mCpds.intersection(ProData)
        for cpd in handh:
            #print(cpd)
            #pdb.set_trace()
            tm = mtabPruned.loc[cpd,:]
            if (cpd in gatherGroup.index): 
                pass
            else: #only add the mtab if it is new...can have mtabs in multiple pathways
                gatherGroup = gatherGroup.append(tm)

    if not gatherGroup.empty: #don't try to plot if empty
        if scaleMM:
            scaled = preprocessing.minmax_scale(gatherGroup,feature_range=(0,1),axis = 1,copy=True)
            #get row/column labels back
            df = pd.DataFrame(scaled,columns = gatherGroup.columns,index = gatherGroup.index) 
        else:
            df = gatherGroup
       
        #hfont = {'fontname':'Palatino'}
        plt.title(oneGroup)
        plt.xlabel('xlabel')
        plt.pcolor(df,cmap = 'YlGnBu')
        plt.yticks(np.arange(0.5, len(gatherGroup.index), 1), gatherGroup.index,fontsize = 8)
        plt.xticks(np.arange(0.5,(len(list(mtabPruned)) + 0.1),1), gatherGroup.columns,rotation = 90)

        #Tracer()()
        #plt.show()
        fig = plt.gcf()
        fig.set_size_inches(18.5, 13)
        fig.savefig(oneGroup + '.png', dpi=100)
        plt.colorbar()
        plt.show()
            
    else:
        print(oneGroup + ': has no metabolites')


def plotGroup_cluster(oneGroup,prunedBRITE,useCO,mtabPruned,oneStrain,scaleMM):
    folder = 'clustermaps/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    #oneStrain = 'pmg'
    shortList = prunedBRITE.loc[(prunedBRITE['B']==oneGroup)] 
    onePath = shortList.loc[:,'map']
    onePath_ann = []
    for item in onePath:
        onePath_ann.append(oneStrain + item)

    gatherGroup = pd.DataFrame()
    for one in onePath_ann:
        #print(one)
        #not all pathways annotated in Prochlorococcus
        setKeep = 1
        try:
            kegg_get(one).read()
        except:
            #use the ko map if there is nothing species specific
            usePathway = 'ko' + one[3:8]
            setKeep = 0
            try:
                kegg_get(usePathway).read()
            except:
                pass
            
        if setKeep:
            usePathway = one
        
        try:
            mCpds = set(getCfrom_ko(usePathway))
        except:
            #no ko pathway either
            break
                          
        ProData= set(useCO)
        handh = mCpds.intersection(ProData)
        for cpd in handh:
            #print(cpd)
            #pdb.set_trace()
            tm = mtabPruned.loc[cpd,:]
            if (cpd in gatherGroup.index): 
                pass
            else: #only add the mtab if it is new...can have mtabs in multiple pathways
                gatherGroup = gatherGroup.append(tm)
    
    if not gatherGroup.empty: #don't try to plot if empty
        if scaleMM:
            scaled = preprocessing.minmax_scale(gatherGroup,feature_range=(0,1),axis = 1,copy=True)
            df = pd.DataFrame(scaled,columns = gatherGroup.columns,index = gatherGroup.index) 
        else:
            df = gatherGroup

        sns.set(font_scale = 2)
        g = sns.clustermap(df,cmap = 'YlGnBu',method = 'ward',metric = 'cityblock')
        plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0)
        plt.title(oneGroup)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 13)
        g.savefig(folder + oneGroup + '.png', dpi=100)
        plt.show() #this will suppress all the rows of 'None'
    else:
        print(oneGroup + ': has no metabolites')
        
    #for item in onePath:
        #print(kegg_list('ko' + item).read())
    
    for item in gatherGroup.index.sort_values():
        print(kegg_list(item).read())
          
def plotGroup_clusterT(oneGroup,prunedBRITE,useCO,mtabPruned,oneStrain,scaleMM):
    folder = 'clustermapsT/'
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    #oneStrain = 'pmg'
    shortList = prunedBRITE.loc[(prunedBRITE['B']==oneGroup)] 
    onePath = shortList.loc[:,'map']
    onePath_ann = []
    for item in onePath:
        onePath_ann.append(oneStrain + item)

    gatherGroup = pd.DataFrame()
    for one in onePath_ann:
        #print(one)
        #not all pathways annotated in Prochlorococcus
        setKeep = 1
        try:
            kegg_get(one).read()
        except:
            #use the ko map if there is nothing species specific
            usePathway = 'ko' + one[3:8]
            setKeep = 0
            try:
                kegg_get(usePathway).read()
            except:
                pass
            
        if setKeep:
            usePathway = one
        
        try:
            mCpds = set(getCfrom_ko(usePathway))
        except:
            #no ko pathway either
            break
                          
        ProData= set(useCO)
        handh = mCpds.intersection(ProData)
        for cpd in handh:
            #print(cpd)
            #pdb.set_trace()
            tm = mtabPruned.loc[cpd,:]
            if (cpd in gatherGroup.index): 
                pass
            else: #only add the mtab if it is new...can have mtabs in multiple pathways
                gatherGroup = gatherGroup.append(tm)
    
    if not gatherGroup.empty: #don't try to plot if empty
        if scaleMM:
            scaled = preprocessing.minmax_scale(gatherGroup,feature_range=(0,1),axis = 1,copy=True)
            df = pd.DataFrame(scaled,columns = gatherGroup.columns,index = gatherGroup.index) 
        else:
            df = gatherGroup

        sns.set(font_scale = 2)
        g = sns.clustermap(df.T,cmap = 'YlGnBu',method = 'ward',metric = 'cityblock')
        plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0)
        plt.title(oneGroup)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 13)
        g.savefig(folder + oneGroup + '.png', dpi=100)
        plt.show() #this will suppress all the rows of 'None'
    else:
        print(oneGroup + ': has no metabolites')
        
    #for item in onePath:
        #print(kegg_list('ko' + item).read())
    
    for item in gatherGroup.index.sort_values():
        print(kegg_list(item).read())
          
#set up a function to get the list of compounds for a given pathway (must be defined as ko00140 NOT map00140)
def getCfrom_ko(ko_id):
    pathway_file = kegg_get(ko_id).read()  # query and read the pathway
    compound_list = []

    current_section = None
    for line in pathway_file.rstrip().split("\n"):
        section = line[:12].strip()  # section names are within 12 columns
        if not section == "":
            current_section = section
        if current_section == "COMPOUND":
            compound_identifiers = line[12:].split("; ")
            t = compound_identifiers[0]
            compound_id = t[0:6]

            if not compound_id in compound_list:
                compound_list.append(compound_id)
    return compound_list
