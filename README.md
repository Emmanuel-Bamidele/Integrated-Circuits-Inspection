-----------------------------------------
IC Visual Aiding Inspection by Emmanuel Bamidele
-----------------------------------------

-----------------------------------------
Overview
-----------------------------------------

This project aims to automate the visual inspection process of Integrated Circuits (ICs) and Printed Circuit Boards (PCBs) by comparing test images against a control image. The application could also be used for other image comparison applications.

-----------------------------------------
Features
-----------------------------------------

Load and display a control image (usually a standard or reference image).

Load and display a test image for inspection.

Perform multiple tests to check for discrepancies such as written items, additions, missing items, cracks, and orientation mismatches.

Show the inspection results via a user-friendly GUI.

Save the inspection results to a user-defined directory.

-----------------------------------------
Requirements
-----------------------------------------

Python 3.x

OpenCV

Tkinter for GUI

PIL (Pillow) for image manipulation

-----------------------------------------
Installation
-----------------------------------------

Clone the repository to your local machine.

Install the required packages:

bash

Copy code

pip install opencv-contrib-python Pillow

Run the main Python file to start the application:

bash

Copy code

python main.py

-----------------------------------------
Usage
-----------------------------------------

Open the application and click "Select Control Image" to load your control or standard image.

Click "Select Test Image" to load the image you wish to inspect.

Click "Start Inspection" to begin the visual inspection process.

View the results in the pop-up dialog box.

Optionally, click "Save Results" to save the inspection images to your desired directory.

-----------------------------------------
Testing Functions
-----------------------------------------

```check_for_written_items```: Compares text between control and test images.

```check_for_additions```: Checks for additional items in the test image.

```check_for_missing_items```: Checks for missing items in the test image.

```check_for_cracks```: Detects cracks using edge detection and line transforms.

```check_orientation```: Checks the orientation of items using feature matching algorithms like SIFT.

-----------------------------------------
Author
-----------------------------------------

Emmanuel Bamidele
License

If you use this project, please cite the author and the project appropriately.



