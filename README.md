## Overview

We use the donkeycar stack on our kart. Donkeycar provides the software architecture for the kart. Donkeycar uses different parts which have inputs and outputs. These parts can be added to a vehicle. The vehicle loop runs the parts in order and stores and modifies data in the vehicle memory.

Here is more information on donkeycar: [donkeycar](https://docs.donkeycar.com/)

Here is a link to our current software architecture: [github link](https://github.com/Autonomous-Motorsports-Purdue/AMP_ASS_donkeycar?tab=readme-ov-file)

The kart currently has these parts:

* Frame Publisher  
* Heartbeat  
* Segment Model  
* Logger  
* UART Driver

### Frame Publisher

[Code Link](https://github.com/Autonomous-Motorsports-Purdue/AMP_ASS_donkeycar/blob/main/parts/frame_publisher.py)

Inputs: N/A  
Outputs:

* sensors/ZED/RGB/Left  
* sensors/ZED/RGB/Right

This part reads in and publishes the current left and right frames on the ZED camera.

### Heartbeat

[Code Link](https://github.com/Autonomous-Motorsports-Purdue/AMP_ASS_donkeycar/blob/main/parts/health_check.py)

Inputs: N/A  
Outputs: 

* safety/heartbeat

Determines if there is an active connection between the kart and the host. If the connection fails, the kart will automatically stop. 

### Segment Model

[Code Link](https://github.com/Autonomous-Motorsports-Purdue/AMP_ASS_donkeycar/blob/main/parts/segment_model.py)

Inputs: 

* sensors/ZED/RGB/Left

Outputs:

* perception/segmentedTrack  
* controls/steering  
* controls/throttle  
* centroid

Runs the segmentation model on the inputted image from the frame publisher. Calculates the centroid of the detected road from the segmentation model. Determines steering and throttle values based on the location of the centroid. Uses a PID controller to follow the centroid. 

### Logger

[Code Link](https://github.com/Autonomous-Motorsports-Purdue/AMP_ASS_donkeycar/blob/main/parts/logger.py)

Inputs:

* sensors/ZED/RGB/Left  
* perception/segmentedTrack  
* controls/steering  
* controls/throttle  
* centroid

Outputs: N/A

Logs the current image, segmented image, centroid, steering, and throttle values. Saves the images in a folder and stores the image paths and other data in a CSV file.

### UART Driver

[Code Link](https://github.com/Autonomous-Motorsports-Purdue/AMP_ASS_donkeycar/blob/main/parts/uart_backup.py)

Inputs:

* controls/steering  
* controls/throttle  
* safety/heartbeat

Outputs: N/A

Writes the throttle and steering commands over serial to the STM which actuates the kart. Maps the inputted values from (-1,1) to the expected values for serial communication.

### Main Loop

[Code Link](https://github.com/Autonomous-Motorsports-Purdue/AMP_ASS_donkeycar/blob/main/donkeycar_runner.py)

1. Instantiates the donkey car vehicle.   
2. Adds the heartbeat, frame publisher, segment model, and logger parts to the vehicle.   
3. Adds the web controller to the vehicle.   
4. Adds the UART driver to the vehicle.   
5. Starts the drive loop.

The main loop instantiates and adds all of the parts to the vehicle. It executes each part sequentially in the order they were added to the vehicle. Each loop executes the parts in the same order. 

## Project

Create the parts and drive loop for simple object detection.

It should contain these parts:

* Image publisher  
* Object Detection  
* Logger

It also needs a main loop

### Clone Repository
Create a new folder and clone this repository into it.

* `git init`
* `git clone https://github.com/Autonomous-Motorsports-Purdue/AMP_Software_Onboarding.git`

### Install Conda
Install miniconda: [miniconda installation](https://docs.anaconda.com/miniconda/install/#quick-command-line-install)

* Create environment: `conda create -n AMP python=3.10`
* Activate environment: `conda activate AMP`
* Install requirements: `conda install --file requirements.txt`

### Image Publisher

Inputs: N/A  
Outputs: 

* image

This part should read images from your webcam and return them in the run function. The run function is what runs each time the part is called in the drive loop. It takes in inputs and returns outputs in the vehicle memory. 

Outline:

* Create a file called image\_publisher.py in the parts directory.   
* Imports  
  * cv2  
* Create a class called Image\_Publisher  
* Create an \_\_init\_\_() method  
  * initialize a cv2 VideoCapture()  
* Create a run() method  
  * read a frame from the VideoCapture()  
  * Return the frame if it is not null

[**Completed Code**](https://github.com/Autonomous-Motorsports-Purdue/AMP_Software_Onboarding/blob/main/parts/image_publisher.py)

### Object Detection

Inputs:

* image

Outputs:

* image\_cv  
* object\_x  
* object\_y  
* contour\_area

This part should detect objects on the inputted image. It should identify objects in the image and return the coordinates of the largest contour by area. It should also return the area of the largest contour.

Outline:

* Create a file called image\_cv.py in the parts directory  
* Imports  
  * cv2  
* Create a class called Object\_Detection  
* Create a run() method which takes in an image  
  * check if the image is not null  
  * convert the image to grayscale  
  * detect the contours in the grayscale image  
  * find and draw largest contour by area  
    * Calculate and draw the centroid of the largest contour  
  * Return the modified image, the contour x coordinate, the contour y coordinate, and contour area

[**Completed Code**](https://github.com/Autonomous-Motorsports-Purdue/AMP_Software_Onboarding/blob/main/parts/image_cv.py)

### Logger

Inputs:

* object\_x  
* object\_y  
* contour\_area

Outputs:

* N/A

Writes the current timestamp, object\_x, object\_y, and contour\_area to a CSV file. 

Outline:

* Imports  
  * datetime  
  * csv  
* Create a file called log.py  
* Create a class called Logger  
* Create an \_\_init\_\_() method  
  * Open a file object with filename “logger.csv” in writemode with newline=’’  
  * Create a csv writer using the file object  
  * Write the fields of the csv: ‘timestamp’, ‘object\_x’, ‘object\_y’, ‘contour\_area’  
* Create a run() method which takes in object\_x, object\_y, and contour\_area  
  * Check that the inputted values are not null  
  * Get the current timestamp  
  * Write the row to the csv file: timestamp, object\_x, object\_y, contour\_area

[**Completed Code**](https://github.com/Autonomous-Motorsports-Purdue/AMP_Software_Onboarding/blob/main/parts/log.py)

### Main Loop

Instantiates the vehicle and adds parts to it. The program runs in an infinite loop, running each part in a sequential order.

Outline:

* Imports  
  * donkeycar  
    * *This will be dependent on the path which donkeycar was cloned into your directory*  
  * Image\_Publisher  
  * Object\_Detection  
  * Logger  
    * *these will be imported from the files in your parts directory*  
* if \_\_name\_\_ \== “\_\_main\_\_”:  
  * Create a donkeycar vehicle  
  * instantiate an Image\_Publisher() and add it to the vehicle.   
    * inputs=\[\]  
    * outputs=\[‘image’\]  
  * instantiate an Object\_Detection() and add it to the vehicle   
    * inputs=\[‘image\]  
    * outputs=\[‘image\_cv’, ‘object\_x’, ‘object\_y’, ‘contour\_area’\]  
  * instantiate a Logger() and add it to the vehicle  
    * inputs=\[‘object\_x’, ‘object\_y’, ‘contour\_area’\]  
    * outputs=\[\]  
  * Start the vehicle with rate\_hz=30

[**Completed Code**](https://github.com/Autonomous-Motorsports-Purdue/AMP_Software_Onboarding/blob/main/onboarding_runner.py)

  
