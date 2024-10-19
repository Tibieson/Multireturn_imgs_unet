
import os
import re
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

def ExtractListofFiles(path):
    """ We wil split the images into sublists
        we are trading off time for simplicity
    """

    sublists = ['Ret1','Ret2','Ret3','Ret4','FULL']
    fetchfiles = os.listdir(path)
    
    fetchfiles = [os.path.join(path,x) for x in fetchfiles]

    tempDict = {}

    for sublist in sublists:
        new_list = [x for x in fetchfiles if re.search(sublist, x)]
        if(new_list == []): # we don't have any return images. Only Full Labels-> we are in the folder label
            tempDict['FULL'] = [x for x in fetchfiles if re.search('FULL', x)]
            break
        else:
            tempDict[sublist] = [x for x in fetchfiles if re.search(sublist, x)]

    return tempDict

    

        
def GetFileStruct(directorypath):
    """ 
        This function will create a dictionary of dictionaries. similar as a C-struct. 
        Folder ------>Fullimg  ---> Ret1, Ret2, Ret3, Ret4, Full
                 |
                 |--->FullLabel ---> Full
                 |
                 |--->RangeImg ---> Ret1, Ret2, Ret3, Ret4, Full
    """
    filepath  = directorypath #r"F:\\SLABOs_image_ManualSegmented\\"
    filelist  = os.listdir(filepath)


    ImagesDict = {'Fullimg':{},'FullLabel':{},'RangeImg':{}}
    subfolders = ['Fullimg','FullLabel','RangeImg']
    for path in filelist[:]: # filelist[:] makes a copy of filelist.
        joinpath = os.path.join(filepath,path)
        if os.path.isdir(joinpath):
            print(joinpath)
            for subfolder in subfolders:
                fullpath = os.path.join(joinpath,subfolder)
                print(fullpath)
                fetchfiles = ExtractListofFiles(fullpath) #os.listdir(fullpath)
                for dictkey in fetchfiles.keys():
                    try:
                        ImagesDict[subfolder][dictkey].extend(fetchfiles[dictkey]) #append was adding a sublist, extends on the other hand adds a flatten extension
                    except:
                        ImagesDict[subfolder][dictkey] = fetchfiles[dictkey]
                fetchfiles = {}

    return ImagesDict


def GetTestStruct(directorypath):
    """ 
        This function will create a dictionary of dictionaries. similar as a C-struct. 
        Folder ------>Fullimg  ---> Ret1, Ret2, Ret3, Ret4, Full
                 |
                 |--->FullLabel ---> Full
                 |
                 |--->RangeImg ---> Ret1, Ret2, Ret3, Ret4, Full
    """
    filepath  = directorypath #r"F:\\SLABOs_image_ManualSegmented\\"
    filelist  = os.listdir(filepath)


    ImagesDict = {'Fullimg':{},'FullLabel':{},'RangeImg':{}}
    subfolders = ['Fullimg','RangeImg']

    for subfolder in subfolders:
        fullpath = os.path.join(filepath,subfolder)
        print(fullpath)
        fetchfiles = ExtractListofFiles(fullpath) #os.listdir(fullpath)
        for dictkey in fetchfiles.keys():
            try:
                ImagesDict[subfolder][dictkey].extend(fetchfiles[dictkey]) #append was adding a sublist, extends on the other hand adds a flatten extension
            except:
                ImagesDict[subfolder][dictkey] = fetchfiles[dictkey]
            fetchfiles = {}

    return ImagesDict

def ReadImageList(filelist):
    """
        Function will receive any list with image paths and it will return a 3D Matrix of size:  Number of Images x 32 x128
    """
    M = len(filelist)
    temp_img = np.zeros((M,32,128))
    #temp_img_norm =  np.zeros((32,128))
    isRange  = filelist[0].find('Range')
    for jj in range(M):
        temp_img[jj,:,:] = mpimg.imread(filelist[jj]) * 65535
        if(isRange != -1 and np.max(temp_img[jj,:,:]) > 60):  #if we have range image in s-unit convert2meters
            temp_img[jj,:,:] = temp_img[jj,:,:] / 256
    
    return temp_img

def GetImageMatrix(Imagedict):
    """
        This function will receive a dictionary and read all images with the following structure
                Full matrix : 5 x Len x 32x 128
        dict_keys(['Fullimg', 'FullLabel', 'RangeImg'])
    """
    M = len(Imagedict['FullLabel']['FULL'])
    FullMatrix_img   = np.zeros((5,M,32,128))
    idxcounter = 0

    for imgkey in Imagedict.keys():
        if imgkey == 'FullLabel':
            temp = ReadImageList(Imagedict[imgkey]['FULL'])
            FullMatrix_img[4,:,:,:] = temp
        else:
            temp = ReadImageList(Imagedict[imgkey]['Ret1'])
            FullMatrix_img[idxcounter,:,:,:] = temp
            idxcounter = idxcounter + 1
            temp = ReadImageList(Imagedict[imgkey]['Ret2'])
            FullMatrix_img[idxcounter,:,:,:] = temp
            idxcounter = idxcounter + 1

    return FullMatrix_img

def MultiLabelReturnMAtrix(Imagedict):
    """
    """
    N_return = 3

    M = len(Imagedict['FullLabel']['Ret1'])
    FullMatrix_img    = np.zeros((N_return * 2,M,32,128))
    LabelMatrix_img   = np.zeros((4,M,32,128))
    idxcounter = 0
    #label_idxccounter = 0

    Extract_list = ['Ret1', 'Ret2', 'Ret3']

    for imgkey in Imagedict.keys():

        for extraction in Extract_list:
            temp = ReadImageList(Imagedict[imgkey][extraction])
            if imgkey == 'FullLabel':
                LabelMatrix_img[idxcounter,:,:,:] = temp
            elif(imgkey == 'RangeImg'):
                FullMatrix_img[idxcounter + 3,:,:,:] = temp
            else:
                FullMatrix_img[idxcounter,:,:,:] = temp

            idxcounter = idxcounter + 1
        idxcounter = 0
    
    return FullMatrix_img,LabelMatrix_img








        


#ImagesDict = GetFileStruct(r"F:\\SLABO_MULTIRETURN_IMG\\")


#print("lol")
#FullMatrix, FullLabelMatrix = MultiLabelReturnMAtrix(ImagesDict)

#FullMatrix = GetImageMatrix(ImagesDict)
#print("lol")



#N = 500
#plot1 = plt.figure(1)
#plt.subplot(4, 1, 1)
#plt.imshow(FullMatrix[0,N,:,:])
#plt.colorbar()
#plt.subplot(4, 1, 2)
#plt.imshow(FullMatrix[1,N,:,:])
#plt.colorbar()
#plt.subplot(4, 1, 3)
#plt.imshow(FullMatrix[3,N,:,:])
#plt.colorbar()
#plt.subplot(4, 1, 4)
#plt.imshow(FullMatrix[4,N,:,:])
#plt.colorbar()

#plot2 = plt.figure(2)
#plt.subplot(4, 1, 1)
#plt.imshow(FullLabelMatrix[0,N,:,:])
#plt.colorbar()
#plt.subplot(4, 1, 2)
#plt.imshow(FullLabelMatrix[1,N,:,:])
#plt.colorbar()
#plt.subplot(4, 1, 3)
#plt.imshow(FullLabelMatrix[2,N,:,:])
#plt.colorbar()
#plt.subplot(4, 1, 4)
#plt.imshow(FullLabelMatrix[3,N,:,:])
#plt.colorbar()
#plt.show()


#----------------------------------------------
#----------------------------------------------

#plt.subplot(3, 1, 1)
#plt.imshow(FullMatrix[2,N,:,:])
#plt.colorbar()
#plt.subplot(3, 1, 2)
#plt.imshow(FullMatrix[3,N,:,:])
#plt.colorbar()
#plt.subplot(3, 1, 3)
#plt.imshow(FullMatrix[4,N,:,:])
#plt.colorbar()
#plt.subplot(3, 2, 4)
#plt.imshow(FullMatrix[3,N,:,:])
#plt.colorbar()
#plt.subplot(3, 2, 5)
#plt.imshow(FullMatrix[4,N,:,:])
#plt.colorbar()
#plt.show()

#read images from the following list
#ImagesDict['Fullimg']['Ret1']
#ImagesDict['Fullimg']['Ret2']
#ImagesDict['RangeImg']['Ret1']
#ImagesDict['RangeImg']['Ret2']
#ImagesDict['FullLabel']['FULL']



#rangelist = {}
##this part is only to fix the range img ---- ):
#range2fixlist = ImagesDict['FullLabel']['FULL']

#for element in range2fixlist:
#    lastsubstring  = element.split('\\')[-1]
#    lastsubs_split = lastsubstring.split('_frame_') # 0 is rec name, 1 is the rest of the string
#    frame = lastsubs_split[1].split('_')
#    try:
#        #rangelist[lastsubs_split[0]].extend((frame[0])) 
#        rangelist.setdefault(lastsubs_split[0],[]).append((frame[0]))
#    except:
#        rangelist[lastsubs_split[0]] = ((frame[0])) 
#        print("lol")
    

#print("lol")

#import json

#with open('range2fix.json', 'w') as fp:
#    json.dump(rangelist, fp)