import cv2
import cv
import pylab
from SIGBTools import RegionProps
from SIGBTools import getLineCoordinates
from SIGBTools import ROISelector
from SIGBTools import getImageSequence
from SIGBTools import getCircleSamples
import numpy as np
import sys
import math

from scipy.cluster.vq import *
from scipy.misc import *
from matplotlib.pyplot import *
from numpy.core.numeric import ndarray

inputFile = "/Developer/GitRepos/ITU-Image-Analysis-2013-EXERCISES/MandatoryAssignment1/Sequences/eye3.avi"
outputFile = "eyeTrackerResult.mp4"

#--------------------------
#         Global variable
#--------------------------
global imgOrig,leftTemplate,rightTemplate,frameNr
imgOrig = []
#These are used for template matching
leftTemplate = []
rightTemplate = []
frameNr =0

def GetPupil(gray,thr):
    #tempResultImg = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)

    props = RegionProps()
    val,binI = cv2.threshold(gray, thr, 255, cv2.THRESH_BINARY_INV)

    st3 = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    binI = cv2.morphologyEx(binI, cv2.MORPH_CLOSE, st3)
    binI= cv2.morphologyEx(binI, cv2.MORPH_OPEN, st3)

    cv2.imshow("ThresholdPupil",binI)#display result in a window with sliders

    sliderVals = getSliderVals()
    contours, hierarchy = cv2.findContours(binI, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    pupils = []
    pupilEllipses = []
    for cnt in contours:
        if len(cnt)>=5:
            values = props.CalcContourProperties(cnt,['Area','Length','Centroid','Perimiter','Extend'])
            ellipse=cv2.fitEllipse(cnt)# fitEllipse([center][height,width],[angle])
            if values['Area'] < sliderVals['maxSizePupil'] and values['Area'] > sliderVals['minSizePupil']:
                pupils.append(values)
                pupilEllipses.append(ellipse)
                #centroid = (int(values['Centroid'][0]),int(values['Centroid'][1]))
                #cv2.circle(tempResultImg,centroid, 2, (0,0,255),4)

    #cv2.imshow("TempResults",tempResultImg)#display the temporary image

    return pupils,pupilEllipses

def detectPupilKMeans(gray,K,distanceWeight,reSize):
    ''' Detects the pupil in the image, gray, using k-means
        gray : grays scale image
        K : Number of clusters
        distanceWeight : Defines the weight of the position parameters
        reSize : the size of the image to do k-means on
    '''
    gray2=np.copy(gray)
    #Resize for faster performance
    smallI = cv2.resize(gray2, reSize)
    M,N = smallI.shape
    #Generate coordinates in a matrix
    X,Y = np.meshgrid(range(M),range(N))
    #Make coordinates and intensity into one vectors
    z = smallI.flatten()
    x = X.flatten()
    y = Y.flatten()
    O = len(x)
    #Make feature vectors containing (x,y,intensity)
    features = np.zeros((O,3))
    features[:,0] = z
    features[:,1] = y/distanceWeight #Divide so that the distance of position weighs less than intensity
    features[:,2] = x/distanceWeight
    features = np.array(features,'f')
    #Cluster data
    centroids,variance = kmeans(features,K)
    centroids.sort(axis = 0) # Sorting clusters according to intensity (ascending)
    pupilCluster = centroids[0] #Choosing the lowest intensity cluster. pupilCluster[0] is threshold for finding pupil for later

    # use the found clusters to map
    #label,distance = vq(features,centroids)
    # re-create image from
    #labelIm = np.array(np.reshape(label,(M,N)))

    # display the labeling
    #f = figure(1); imshow(labelIm); f.canvas.draw(); f.show()

    '''This snippet applies BLOB detection on labelIm (ex 1.7) .'''
    #labelCopy = []
    #for a in labelIm:
    #    newBlock = []
    #    for b in a:
    #        if b !=0:
    #            b=255
    #        newBlock.append(b)
    #    labelCopy.append(newBlock)

    #Applying some morphology
    #labelCopy = np.array(labelCopy)
    #Here I get binary image showing only cluster containing pixels which intensity equals pupil intensity. Here we should continue with blob detection...
    ''' end snippet'''

    #Do BLOB detection
    tempResultImg = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
    val,binI = cv2.threshold(gray, pupilCluster[0], 255, cv2.THRESH_BINARY_INV)

    #Appplying morphology
    st3 = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))

    binI = cv2.morphologyEx(binI, cv2.MORPH_CLOSE, st3)
    binI= cv2.morphologyEx(binI, cv2.MORPH_OPEN, st3)

    cv2.imshow("ThresholdPupil",binI)

    sliderVals = getSliderVals()
    props = RegionProps()
    contours, hierarchy = cv2.findContours(binI, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #Finding contours/candidates for pupil blob
    pupils = []
    pupilEllipses = []
    for cnt in contours:
        values = props.CalcContourProperties(cnt.astype('int'),['Area','Length','Perimiter','Centroid','Extend','ConvexHull'])
        if len(cnt)>=5 and values['Area'] < sliderVals['maxSizePupil'] and values['Area'] > sliderVals['minSizePupil']:
            centroid = (int(values['Centroid'][0]),int(values['Centroid'][1]))
            pupils.append(values)
            pupilEllipses.append(cv2.fitEllipse(cnt.astype('int')))
            cv2.circle(tempResultImg,centroid, 2, (0,0,255),4)

    cv2.imshow("TempResults",tempResultImg)

    return pupils,pupilEllipses

def getPupilThreshold(gray, K, distanceWeight):
    gray2=np.copy(gray)
    #Resize for faster performance
    smallI = cv2.resize(gray2, (40,40))
    M,N = smallI.shape
    #Generate coordinates in a matrix
    X,Y = np.meshgrid(range(M),range(N))
    #Make coordinates and intensity into one vectors
    z = smallI.flatten()
    x = X.flatten()
    y = Y.flatten()
    O = len(x)
    #make a feature vectors containing (x,y,intensity)
    features = np.zeros((O,3))
    features[:,0] = z;
    features[:,1] = y/distanceWeight; #Divide so that the distance of position weighs lessthan intensity
    features[:,2] = x/distanceWeight;
    features = np.array(features,'f')
    # cluster data
    centroids,variance = kmeans(features,K)
    centroids.sort(axis = 0) # Sorting clusters according to intensity (ascending)
    pupilCluster = centroids[0] #Choosing the lowest intensity cluster. pupilCluster[0] is threshold for finding pupil for later
    return pupilCluster[0]

def getIrisUsingThreshold(gray,pupil):
    ''' Given a gray level image and pupil cluster return a list of iris locations(threshold for iris)'''
    gray2=np.copy(gray)
    #Resize for faster performance
    smallI = cv2.resize(gray, (40,40))
    M,N = smallI.shape
    #Generate coordinates in a matrix
    X,Y = np.meshgrid(range(M),range(N))
    #Make coordinates and intensity into one vectors
    z = smallI.flatten()
    x = X.flatten()
    y = Y.flatten()
    O = len(x)
    #make a feature vectors containing (x,y,intensity)
    features = np.zeros((O,3))
    features[:,0] = z;
    features[:,1] = y/2; #Divide so that the distance of position weighs less than intensity
    features[:,2] = x/2;
    features = np.array(features,'f')
    # cluster data
    centroids,variance = kmeans(features,3)
    centroids.sort(axis = 0) # Sorting clusters according to intensity (ascending)
    irisPupilCluster = centroids[1]

    #   inverted threshold irisPupilCluster (pupil and iris white)
    val,binIrisPupil = cv2.threshold(gray2, irisPupilCluster[0], 255, cv2.THRESH_BINARY_INV)
    #   normal threshold pupilCluster (pupil black, iris white)
    val,binPupil =  cv2.threshold(gray2, pupil, 255, cv2.THRESH_BINARY)

    irisPupilCluster=cv2.cvtColor(binIrisPupil, cv2.COLOR_GRAY2RGB)
    binPupil=cv2.cvtColor(binPupil, cv2.COLOR_GRAY2RGB)

    #   bitwise xor (exactly one should be white - result iris black)
    iris=cv2.bitwise_xor(irisPupilCluster,binPupil)
    #   invert the colors of the resulting image (black to white iris)
    iris=255-iris
    return iris

def GetGlints(gray,thr):
    #tempResultImg = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)

    props = RegionProps()

    val,binI = cv2.threshold(gray, thr, 255, cv2.THRESH_BINARY)

    st7 = cv2.getStructuringElement(cv2.MORPH_CROSS,(7,7))

    binI= cv2.morphologyEx(binI, cv2.MORPH_OPEN, st7)
    binI = cv2.morphologyEx(binI, cv2.MORPH_DILATE, st7, iterations=2)
    
    cv2.imshow("ThresholdGlints",binI)

    sliderVals = getSliderVals()
    contours, hierarchy = cv2.findContours(binI, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    glints = []
    for cnt in contours:
        values = props.CalcContourProperties(cnt,['Area','Length','Centroid','Extend','ConvexHull'])
        if values['Area'] < sliderVals['maxSizeGlints'] and values['Area'] > sliderVals['minSizeGlints']:
            centroid = (int(values['Centroid'][0]),int(values['Centroid'][1]))
            glints.append(centroid)
            #cv2.circle(tempResultImg,centroid, 2, (0,0,255),4)

    #cv2.imshow("TempResults",tempResultImg)

    return glints

def FilterPupilGlint(pupils,glints):
    ''' Given a list of pupil candidates and glint candidates returns a list of pupil and glints'''
#       Filter glints based on fixed distance between them - impossible in a single frame... need a previous frame, but this is not build for that... it is much harder (time consuming for computation) than simply finding the 2 glints that are closest to the pupil
#       Assume that we have found the pupil correctly, we'll find the 2 glints closest to it
#+/-:   for each correct pupil, we are most likely to find the 2 best glint pair candidates (assuming they are among the group of candidates), but it is highly dependent on the pupil/s
    pupilIndex=-1
    filteredGlints=[]

    best_c=2
    blob=-1
    for pupil in range(len(pupils)):
        circularity=pupils[pupil]['Perimiter']/(2*math.sqrt(math.pi*pupils[pupil]['Area']))
        if best_c>circularity:
            best_c=circularity
            blob=pupil
    if blob!=-1:
        pupilIndex=blob
        pupil=pupils[pupilIndex]
        pupil_centroid=pupil['Centroid']

        #finding the 2 min distant glints with 1 loop (need 2 minimums-g1,g2 with values about the current glintEllipse and its distance to the pupil)
        g1,g2=[-1,10**6],[-1,10**6]#[index,min_distance]
        for glint in range(len(glints)):
            if g1[0]==-1:
                g1=[glints[glint],getDistance(pupil_centroid,glints[glint])]
            elif g2[0]==-1:
                g2=[glints[glint],getDistance(pupil_centroid,glints[glint])]
            else:
                min=getDistance(pupil_centroid,glints[glint])
                higher=max(g1[1],g2[1])
                higher_index=1 if higher==g1[1] else 2
                if min<higher:
                    if higher_index==1:
                        g1[0]=glints[glint]
                        g1[1]=min
                    else:
                        g2[0]=glints[glint]
                        g2[1]=min
        if g1[0]!=-1:
            filteredGlints.append(g1[0])
        if g2[0]!=-1:
            filteredGlints.append(g2[0])
    return pupilIndex,filteredGlints

def getDistance(pair1,pair2):
    distance=math.sqrt(math.pow(pair1[0]-pair2[0],2)+math.pow(pair1[1]-pair2[1],2))
    return distance

def circularHough(gray):
    ''' Performs a circular hough transform of the image, gray and shows the  detected circles
    The circe with most votes is shown in red and the rest in green colors '''
    #See help for http://opencv.itseez.com/modules/imgproc/doc/feature_detection.html?highlight=houghcircle#cv2.HoughCircles
    blur = cv2.GaussianBlur(gray, (31,31), 11)

    dp = 6; minDist = 30
    highThr = 20 #High threshold for canny
    accThr = 850 #accumulator threshold for the circle centers at the detection stage. The smaller it is, the more false circles may be detected
    maxRadius = 50
    minRadius = 155
    circles = cv2.HoughCircles(blur,cv2.cv.CV_HOUGH_GRADIENT, dp,minDist, None, highThr,accThr,maxRadius, minRadius)

    #Make a color image from gray for display purposes
    gColor = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    if (circles !=None):
    #print circles
        all_circles = circles[0]
        M,N = all_circles.shape
        k=1
        for c in all_circles:
            cv2.circle(gColor, (int(c[0]),int(c[1])),c[2], (int(k*255/M),k*128,0))
            k=k+1
    c=all_circles[0,:]
    cv2.circle(gColor, (int(c[0]),int(c[1])),c[2], (0,0,255),5)
    cv2.imshow("hough",gColor)

def GetIrisUsingNormals(gray,pupil,normalLength):
    ''' Given a gray level image, gray and the length of the normals, normalLength
    return a list of iris locations'''
    # YOUR IMPLEMENTATION HERE !!!!
    pass

def GetIrisUsingSimplifiedHough(gray,pupil):
    ''' Given a gray level image, gray
    return a list of iris locations using a simplified Hough transformation'''
    # YOUR IMPLEMENTATION HERE !!!!
    pass

def GetEyeCorners(leftTemplate, rightTemplate,pupilPosition=None):
    pass

def getGradientImageInfo(I):
    '''
    given a gray scale image returns images gradient Images (Gx,Gy), gradient magnitude (Gm) and gradient directions(Gd). Recall that
        Orientation: (i,j) = atan( Gx(i,j) , Gy(i,j) ) * 180/pi
        Gradient magnitude: gr I(i,j) = sqrt( pow(Gy(i,j),2) + pow(Gy(i,j),2))
    '''
    #Gx can be represented by filtering with kernel [[-1,0,1],[-2,0,2],[-1,0,1]] or similar larger
    #Gy can be represented by filtering with kernel [[-1,-2,-1],[0,0,0],[1,2,1]] or similar larger
    #or we can also use Sobel or even Scharr(similar to Sobel, but higher weights...makes edges more visible)
    #but gradient images are very sensitive to noise, so we'll smooth the image first
    #inspired by: https://github.com/abidrahmank/OpenCV2-Python/blob/master/Official_Tutorial_Python_Codes/3_imgproc/sobel.py
    I2=np.copy(I)
    '''
    I2=cv2.GaussianBlur(I,(5,5),0)
    Gx=np.copy(I2)
    Gy=np.copy(I2)
    Hfx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    Gx=cv2.filter2D(Gx,-1,Hfx)
    Hfx=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    Gy=cv2.filter2D(Gy,-1,Hfx)
    '''
    I2=cv2.GaussianBlur(I2,(3,3),0)
    #cv2.Sobel(src, ddepth, dx, dy[, dst[, ksize[, scale[, delta[, borderType]]]]]) -> dst
    #cv2.Scharr(src, ddepth, dx, dy[, dst[, scale[, delta[, borderType]]]]) -> dst

    grad_x = np.copy(I2)
    grad_x = cv2.Sobel(grad_x,cv2.CV_16S,1,0,borderType = cv2.BORDER_DEFAULT)
    #grad_x = cv2.Scharr(grad_x,cv2.CV_16S,1,0)

    grad_y = np.copy(I2)
    grad_y = cv2.Sobel(grad_y,cv2.CV_16S,0,1,borderType = cv2.BORDER_DEFAULT)
    #grad_y = cv2.Sobel(grad_y,cv2.CV_16S,0,1)

    '''
    #more accurate, but too slow... instead sum the abstract values
    grad_d = np.copy(I2)
    M,N = np.shape(I2)
    for i in range(M):
        for j in range(N):
            grad_d[i,j]=math.sqrt(grad_x[i,j]**2+grad_y[i,j]**2)
    '''

    abs_grad_x = cv2.convertScaleAbs(grad_x)   # converting back to uint8 + absolute
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    grad_m=cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    #slow, but I can't find anything faster
    grad_d = np.copy(I2)
    M,N = np.shape(I2)
    for i in range(M):
        for j in range(N):
            grad_d[i,j]=math.atan2(grad_y[i,j],grad_x[i,j]) * 180/math.pi

    #cv2.imshow("ThresholdPupil",grad_d)
    #2.2.2
    # grad_x: the first derivative that shows high changes, when looking at the image horizontally (it doesn't show that good tough, can multiply its value to show better...grad_x*100)
    # grad_y: the first derivative that shows high changes, when looking at the image vertically (also doesn't show that good, can multiply its value to show better...grad_y*100)
    # grad_d: has high values where there are high changes in intensity - around the pupil, the glints and eyelashes and barely around the iris
    # grad_m: shows the image as a relief map based on intensity changes

    return (grad_x, grad_y),grad_d, grad_m

def circleTest(gray,pupilBlob,pupilEllipse,(Gx,Gy),Gd,Gm):
    nPts = 20
    centroid = (int(pupilBlob['Centroid'][0]),int(pupilBlob['Centroid'][1]))
    (height,width)=pupilEllipse[1]
    circleRadius = int(height)/2
    normalLength=10
    P= getCircleSamples(center=centroid, radius=circleRadius, nPoints=nPts)
    samplePoints=[]
    normals=[]
    P2= getCircleSamples(center=centroid, radius=circleRadius+normalLength, nPoints=nPts)
    for (x,y,dx,dy) in P:
        samplePoint=(int(x),int(y))
        samplePoints.append(samplePoint)
    for (x,y,dx,dy) in P2:
        normal=(int(x),int(y))
        normals.append(normal)
    for i in range(nPts):
        cv2.circle(Gm,samplePoints[i], 1,(255,0,255),5)
        cv2.line(Gm,samplePoints[i],normals[i],(255,0,255))
    cv2.imshow("TempResults", Gm) #display the gradients magnitude with circle sample
    return None

def findEllipseContour(img, gradientMagnitude, estimatedCenter, estimatedRadius,nPts=30):
    Gm=np.copy(gradientMagnitude)
    P= getCircleSamples(center=estimatedCenter,radius=estimatedRadius ,nPoints= nPts)
    samplePoints=[]
    #< define normalLength as some maximum distance away from initial circle >
    normalLength = 5
    P2=getCircleSamples(center=estimatedCenter,radius=estimatedRadius+normalLength,nPoints= nPts)
    normals=[]
    nPts = 30
    newPupil = np.zeros((nPts,1,2)).astype(np.float32)
    #< get the endpoints of the normal -> p1,p2>
    for (x,y,dx,dy) in P:
        p1 = (int(x),int(y))
        samplePoints.append(p1)
    for (x,y,dx,dy) in P2:
        p2 = (int(x),int(y))
        normals.append(p2)
    t=0
    for i in range(nPts):
        #< maxPoint= findMaxGradientValueOnNormal(gradientMagnitude,p1,p2) >
        maxPoint = findMaxGradientValueOnNormal(Gm,samplePoints[i],normals[i])
        #< store maxPoint in newPupil>
        newPupil[t]=maxPoint
        t=t+1
    #<fitPoints to model using least squares- cv2.fitellipse(newPupil)>
    ellipse = cv2.fitEllipse(newPupil)
    cv2.ellipse(Gm,ellipse,(0,255,0),1)
    cv2.imshow("TempResults", Gm) #display the gradients magnitude with pupilEllipseContour
    #return ellipseParameters
    return ellipse

def findMaxGradientValueOnNormal(gradientMagnitude,p1,p2):
    #Get integer coordinates on the straight line between p1 and p2
    pts = getLineCoordinates(p1, p2)
    #normalVals = gradientMaginitude[pts[:,1],pts[:,0]]
    #Find index of max value in normalVals
    max=0
    highest=[-1,-1]
    for i in range(len(pts)):
        if max<=gradientMagnitude[pts[i][1]][pts[i][0]]:
            max=gradientMagnitude[pts[i][1]][pts[i][0]]
            highest[0]=pts[i][1]
            highest[1]=pts[i][0]
    #return coordinate of max value in image coordinates
    return (highest[0],highest[1])

def update(I):
    '''Calculate the image features and display the result based on the slider values'''
    #global drawImg
    global frameNr,drawImg
    img = I.copy()
    sliderVals = getSliderVals()
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    # Do the magic
    pupilBlobs,pupilEllipses = GetPupil(gray,sliderVals['pupilThr'])
    #pupilBlobs,pupilEllipses = detectPupilKMeans(gray,4,2,(40,40))
    glints = GetGlints(gray,sliderVals['glintThr'])
    pupilIndex,glints=FilterPupilGlint(pupilBlobs,glints)
    pupils=[]
    if pupilIndex!=-1: pupils.append(pupilEllipses[pupilIndex])

    # Show the iris using threshold in another window
    #pupilCluster=getPupilThreshold(gray,4,2) #use to find iris (pupil cluster)
    #irisCluster=getIrisUsingThreshold(gray,pupilCluster) #use to find iris (iris threshold)
    #cv2.imshow("TempResults",irisCluster) #show iris in another window

    (Gx,Gy),Gd,Gm=getGradientImageInfo(gray)
    if len(pupilBlobs)>0 and len(pupilEllipses)>0:
        circleTest(gray,pupilBlobs[pupilIndex],pupilEllipses[pupilIndex],(Gx,Gy),Gd,Gm) #display the gradients magnitude with circle sample

        #Work in progress:
        #pupilEllipseContour=findEllipseContour(img, Gm, pupilBlobs[pupilIndex]['Centroid'], pupils[0][1][0]/2)



    #Do template matching
    global leftTemplate
    global rightTemplate
    GetEyeCorners(leftTemplate, rightTemplate)
    #Display results
    global frameNr,drawImg
    x,y = 15,10
    setText(img,(520,y+10),"Frame:%d" %frameNr)
    sliderVals = getSliderVals()

    # for non-windows machines we print the values of the threshold in the original image
    if sys.platform != 'win32':
        step=18
        cv2.putText(img, "pupilThr :"+str(sliderVals['pupilThr']), (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)
        cv2.putText(img, "glintThr :"+str(sliderVals['glintThr']), (x, y+step), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)
        cv2.putText(img, "maxSizePupil :"+str(sliderVals['maxSizePupil']), (x, y+2*step), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)
        cv2.putText(img, "minSizePupil :"+str(sliderVals['minSizePupil']), (x, y+3*step), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)
        cv2.putText(img, "maxSizeGlints :"+str(sliderVals['maxSizeGlints']), (x, y+4*step), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)
        cv2.putText(img, "minSizeGlints :"+str(sliderVals['minSizeGlints']), (x, y+5*step), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)
        

    for pupil in pupils:
        cv2.ellipse(img,pupil,(0,255,0),1)
        C = int(pupil[0][0]),int(pupil[0][1])
        cv2.circle(img,C, 2, (0,0,255),4)
    for glint in glints:
        C = int(glint[0]),int(glint[1])
        cv2.circle(img,C, 2,(255,0,255),5)
    cv2.imshow("Result", img)

        #For Iris detection - Week 2
        #circularHough(gray)

    #copy the image so that the result image (img) can be saved in the movie
    drawImg = img.copy()


def printUsage():
    print "Q or ESC: Stop"
    print "SPACE: Pause"
    print "r: reload video"
    print 'm: Mark region when the video has paused'
    print 's: toggle video  writing'
    print 'c: close video sequence'

def run(fileName,resultFile='eyeTrackingResults.avi'):

    ''' MAIN Method to load the image sequence and handle user inputs'''
    global imgOrig, frameNr,drawImg
    setupWindowSliders()
    props = RegionProps()
    cap,imgOrig,sequenceOK = getImageSequence(fileName)
    videoWriter = 0

    frameNr =0
    if(sequenceOK):
        update(imgOrig)
    printUsage()
    frameNr=0
    saveFrames = False

    while(sequenceOK):
        sliderVals = getSliderVals()
        frameNr=frameNr+1
        ch = cv2.waitKey(1)
        #Select regions
        if(ch==ord('m')):
            if(not sliderVals['Running']):
                roiSelect=ROISelector(imgOrig)
                pts,regionSelected= roiSelect.SelectArea('Select left eye corner',(400,200))
                if(regionSelected):
                    leftTemplate = imgOrig[pts[0][1]:pts[1][1],pts[0][0]:pts[1][0]]

        if ch == 27:
            break
        if (ch==ord('s')):
            if((saveFrames)):
                videoWriter.release()
                saveFrames=False
                print "End recording"
            else:
                imSize = np.shape(imgOrig)
                videoWriter = cv2.VideoWriter(resultFile, cv.CV_FOURCC('D','I','V','X'), 15.0,(imSize[1],imSize[0]),True) #Make a video writer
                videoWriter.write(drawImg)
                saveFrames = True
                print "Recording..."



        if(ch==ord('q')):
            break
        if(ch==32): #Spacebar
            sliderVals = getSliderVals()
            cv2.setTrackbarPos('Stop/Start','ThresholdGlints',not sliderVals['Running'])
            cv2.setTrackbarPos('Stop/Start','ThresholdPupil',not sliderVals['Running'])
        if(ch==ord('r')):
            frameNr =0
            sequenceOK=False
            cap,imgOrig,sequenceOK = getImageSequence(fileName)
            update(imgOrig)
            sequenceOK=True

        sliderVals=getSliderVals()
        if(sliderVals['Running']):
            sequenceOK, imgOrig = cap.read()
            if(sequenceOK): #if there is an image
                update(imgOrig)
            if(saveFrames):
                videoWriter.write(drawImg)

    if videoWriter!=0:
        videoWriter.release

#--------------------------
#         UI related
#--------------------------

def setText(dst, (x, y), s):
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2, lineType=cv2.CV_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)

def setupWindowSliders():
    ''' Define windows for displaying the results and create trackbars'''
    cv2.namedWindow("Result")
    cv2.namedWindow('ThresholdPupil')
    cv2.namedWindow('ThresholdGlints')
    cv2.namedWindow("TempResults")
    #Threshold value for the pupil intensity
    cv2.createTrackbar('pupilThr','ThresholdPupil', 90, 255, onSlidersChange)
    #Threshold value for the glint intensities
    cv2.createTrackbar('glintThr','ThresholdGlints', 245, 255,onSlidersChange)
    #define the minimum and maximum areas of the pupil
    cv2.createTrackbar('minSizePupil','ThresholdPupil', 20, 200, onSlidersChange)
    cv2.createTrackbar('maxSizePupil','ThresholdPupil', 200,200, onSlidersChange)
    #define the minimum and maximum areas of the glints
    cv2.createTrackbar('minSizeGlints','ThresholdGlints', 10, 50, onSlidersChange)
    cv2.createTrackbar('maxSizeGlints','ThresholdGlints', 50,50, onSlidersChange)
    #Value to indicate whether to run or pause the video
    cv2.createTrackbar('Stop/Start','ThresholdPupil', 0,1, onSlidersChange)
    cv2.createTrackbar('Stop/Start','ThresholdGlints', 0,1, onSlidersChange)

def getSliderVals():
    '''Extract the values of the sliders and return these in a dictionary'''
    sliderVals={}
    sliderVals['pupilThr'] = cv2.getTrackbarPos('pupilThr', 'ThresholdPupil')
    sliderVals['glintThr'] = cv2.getTrackbarPos('glintThr', 'ThresholdGlints')
    sliderVals['minSizePupil'] = 50*cv2.getTrackbarPos('minSizePupil', 'ThresholdPupil')
    sliderVals['maxSizePupil'] = 50*cv2.getTrackbarPos('maxSizePupil', 'ThresholdPupil')
    sliderVals['minSizeGlints'] = 50*cv2.getTrackbarPos('minSizeGlints', 'ThresholdGlints')
    sliderVals['maxSizeGlints'] = 50*cv2.getTrackbarPos('maxSizeGlints', 'ThresholdGlints')
    sliderVals['Running'] = 1==cv2.getTrackbarPos('Stop/Start', 'ThresholdPupil')
    sliderVals['Running'] = 1==cv2.getTrackbarPos('Stop/Start', 'ThresholdGlints')
    return sliderVals

def onSlidersChange(dummy=None):
    ''' Handle updates when slides have changed.
     This  function only updates the display when the video is put on pause'''
    global imgOrig
    sv=getSliderVals()
    if(not sv['Running']): # if pause
        update(imgOrig)

#--------------------------
#         main
#--------------------------
run(inputFile)