import cv2 as cv

import numpy as np
from matplotlib import pyplot as plt

# Create a video capture object, in this case we are reading the video from a file
vid_capture = cv.VideoCapture('/home/darshit/Desktop/ENPM673_Proj1/darshit_Proj1/Code/Q1/ball.mov')
if (vid_capture.isOpened() == False):
    print("Error opening the video file")

# Read fps and frame count
else:
    # Get frame rate information
    # You can replace 5 with CAP_PROP_FPS as well, they are enumerations
    fps = vid_capture.get(5)
    print('Frames per second : ', fps,'FPS')
 
    # Get frame count
    # You can replace 7 with CAP_PROP_FRAME_COUNT as well, they are enumerations
    frame_count = vid_capture.get(7)
    print('Frame count : ', frame_count)
x = []
y = [] 
while(True):
  # vid_capture.read() methods returns a tuple, first element is a bool 
  # and the second is frame
    ret, frame = vid_capture.read()
    if ret==True:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        low_red = np.array ([0,175,85])
        high_red = np.array ([5,255,255])
        # low_red = np.array ([0,185,55])
        # high_red = np.array ([20,255,255])
        masking = cv.inRange(hsv, low_red, high_red)

        res = cv.bitwise_and(frame, frame, mask=masking)

        #Use the mask frames to find out nonzero instances in the frame and it's indices
        yis, xis = np.nonzero(masking)
        #Take the centroid of the indices from the above command which is basically the center of the filtered ball
        a=xis.mean()
        b=yis.mean()

        x.append(a)
        y.append(-b)
           

        cv.imshow("Frame",frame)
        cv.imshow("Mask",masking)
        cv.imshow("Result",res)
        # 20 is in milliseconds, try to increase the value, say 50 and observe
        k = cv.waitKey(15)
        if(k==27):
            break
    else:
        break
     
 
# Release the video capture object
vid_capture.release()
cv.destroyAllWindows()

#Plot the captured center points of the red ball
plt.scatter(x,y)
plt.xlabel("x displacement")
plt.ylabel("y displacement")
plt.show()

#Code for fitting the scattered points into a parabola
from math import nan

#Loop to remove points in the frame where ball is out of the frame
x_1=[number for number in x if str(number)!="nan"]
y_1=[number for number in y if str(number)!="nan"]

#Code to calculate the square fitting starts here
square=[number**2 for number in x_1]
cubed=[number**3 for number in x_1]
quadrupled=[number**4 for number in x_1]
x_y=[]
for i in range(0,len(x_1)):
    x_y.append(x_1[i]*y_1[i])
xsquare_y=[]
for i in range(0,len(x_1)):
    xsquare_y.append(square[i]*y_1[i])
A=np.array([[len(x_1),np.sum(x_1),np.sum(square)],
[np.sum(x_1),np.sum(square),np.sum(cubed)],
[sum(square),np.sum(cubed),np.sum(quadrupled)]])
B=np.array([np.sum(y_1),np.sum(x_y),np.sum(xsquare_y)])
sol=np.linalg.solve(A,B)
def funct(x_1):
    parabola = sol[0]+sol[1]*x_1+sol[2]*x_1**2
    return parabola
x_set=np.linspace(0,1200,50)
plt.plot(x_set,funct(x_set),color='r')
plt.xlabel("x displacement")
plt.ylabel("y displacement")
plt.scatter(x,y)
plt.show()

#Printing the equation of the parabola
print ("The equation of the parabola is given as below:")
print("y=",sol[0],"+",sol[1],"x +",sol[2],"x^2")

##Find the distance where the ball landed
x1=(-sol[1]+np.sqrt(sol[1]**2-4*(sol[2]*(sol[0]-sol[0]+300))))/(2*sol[2])
x2=(-sol[1]-np.sqrt(sol[1]**2-4*(sol[2]*(sol[0]-y_1[0]+300))))/(2*sol[2])
#Print the landing point of the ball
if (x1<0 and x2>0):
    print("x1 is not a valid point for the ball's landing point")
    print ("The landing point of the ball is x2 = ",(x2,y_1[0]-300))
elif (x2<0 and x1>0):
    print("x2 is not a valid point for the ball's landing point")
    print ("The landing point of the ball is x1 = ", x1)

