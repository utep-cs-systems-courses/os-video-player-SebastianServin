#!/usr/bin/env python3
from multiprocessing import Semaphore
from threading import Thread
import cv2
import numpy as np
import os
import base64
import queue
from BinarySemaphore import BinarySemaphore

outputDir = 'frames'
clipFileName = 'clip.mp4'
frameDelay = 42
convertingToGrayscaleSemaphore  = BinarySemaphore()
# displayingGrayscaleSemaphore = BinarySemaphore()

# Gets the frames from original video
def extractFrames():

    # initialize frame count
    count = 0
    
    # open the video clip
    vidcap = cv2.VideoCapture(clipFileName)

    # create the output directory if it doesn't exist
    if not os.path.exists(outputDir):
        print(f"Output directory {outputDir} didn't exist, creating")
        os.makedirs(outputDir)

    # read one frame
    success,image = vidcap.read()

    print(f'Reading frame {count} {success}')
    while success and count < 72:
        convertingToGrayscaleSemaphore.waitForGettingResource()
        # write the current frame out as a jpeg image
        cv2.imwrite(f"{outputDir}/frame_{count:04d}.bmp", image)   

        success,image = vidcap.read()
        print(f'Reading frame {count}')
        
        count += 1
        convertingToGrayscaleSemaphore.putResource()


# Converts colored frames to grayscale
def convertToGrayscale():
    # initialize frame count
    count = 0

    # get the next frame file name
    inFileName = f'{outputDir}/frame_{count:04d}.bmp'


    # load the next file
    inputFrame = cv2.imread(inFileName, cv2.IMREAD_COLOR)

    while inputFrame is not None and count < 72:
        convertingToGrayscaleSemaphore.waitForResource()
        # displayingGrayscaleSemaphore.waitForGettingResource()
        print(f'Converting frame {count}')

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
        
        # generate output file name
        outFileName = f'{outputDir}/grayscale_{count:04d}.bmp'

        # write output file
        cv2.imwrite(outFileName, grayscaleFrame)


        # generate input file name for the next frame
        inFileName = f'{outputDir}/frame_{count:04d}.bmp'
        
        # load the next frame
        inputFrame = cv2.imread(inFileName, cv2.IMREAD_COLOR)

        convertingToGrayscaleSemaphore.getResource()
        # displayingGrayscaleSemaphore.putResource()
        count += 1

# Displays grayscale frames
def displayFrames():
    # initialize frame count
    count = 0

    # Generate the filename for the first frame 
    frameFileName = f'{outputDir}/grayscale_{count:04d}.bmp'

    # load the frame
    frame = cv2.imread(frameFileName)
    # print(frame)
    # cv2.imshow('Video', frame)

    while frame is not None:

        # displayingGrayscaleSemaphore.waitForResource()        
        print(f'Displaying frame {count}')
        # Display the frame in a window called "Video"
        cv2.imshow('Video', frame)

        # Wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(frameDelay) and 0xFF == ord("q"):
            break    
        
        # get the next frame filename
        frameFileName = f'{outputDir}/grayscale_{count:04d}.bmp'

        # Read the next frame file
        frame = cv2.imread(frameFileName)
        count += 1
        # displayingGrayscaleSemaphore.getResource()

    # make sure we cleanup the windows, otherwise we might end up with a mess
    cv2.destroyAllWindows()

# extractFramesThread = Thread(target=extractFrames)
# convertingToGrayscaleThread = Thread(target=convertToGrayscale)
# displayFramesThread = Thread(target=displayFrames)

# extractFramesThread.start()
# convertingToGrayscaleThread.start()
# displayFramesThread.start()
displayFrames()

# extractFrames()
# convertToGrayscale()
