"""
Initiated on June 04, 2018
Completed on July 18, 2018

Modified: 08/03/2018, 08/21/2018, 11/15/2018

Author: Emmanuel Bamidele

Targeted Application: Visual inspection of ICs and PCBs. Can work for other image comparison applications

If used, please cite the author and project appropriately.

"""


import os 
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button, Canvas, PhotoImage
from PIL import Image, ImageTk

class ICVisualInspection:

    def __init__(self, master):
        self.master = master
        self.master.title("© IC Visual Inspection by Bamidele")
        self.master.geometry("800x600")

        self.initUI()

        self.control_image_path = None
        self.test_image_path = None
        self.control_image = None
        self.test_image = None

        self.failed_tests = []  # Keep track of failed tests
        self.passed_tests = []  # Keep track of passed tests


    def initUI(self):
        Label(self.master, text="IC Visual Inspection v1", font=("Arial", 20, "bold"), fg="blue").grid(row=0, column=0, columnspan=2, pady=20)
        Label(self.master, text="Select the control image, then the test image.", font=("Arial", 12)).grid(row=1, column=0, columnspan=2, pady=10)

        Button(self.master, text="Select Control Image", command=self.load_control_image, width=20, bg="#4CAF50", fg="white").grid(row=2, column=0, pady=10, padx=20)
        self.control_canvas = Canvas(self.master, width=360, height=240, bg="#DDDDDD")
        self.control_canvas.grid(row=3, column=0, pady=10, padx=20)
        Label(self.master, text="Control Image", font=("Arial", 12, "italic")).grid(row=4, column=0)

        Button(self.master, text="Select Test Image", command=self.load_test_image, width=20, bg="#4CAF50", fg="white").grid(row=2, column=1, pady=10, padx=20)
        self.test_canvas = Canvas(self.master, width=360, height=240, bg="#DDDDDD")
        self.test_canvas.grid(row=3, column=1, pady=10, padx=20)
        Label(self.master, text="Test Image", font=("Arial", 12, "italic")).grid(row=4, column=1)

        Button(self.master, text="Start Inspection", command=self.perform_inspection, width=20, bg="#2196F3", fg="white").grid(row=5, column=0, pady=20)
        Button(self.master, text="Save Results", command=self.save_results, width=20, bg="black", fg="white").grid(row=5, column=1, pady=20)

        # Add the status label to the bottom of the UI
        self.status_label = Label(self.master, text="Status: Pending", font=("Arial", 12))
        self.status_label.grid(row=6, column=0, columnspan=2, pady=20)

    def open_webpage(self, url):
        import webbrowser
        webbrowser.open(url)

    def save_results(self):
        save_path = filedialog.askdirectory()
        
        if save_path:
            # Save failed tests
            for idx, test in enumerate(self.failed_tests):
                compared_image = test[2]
                cv2.imwrite(os.path.join(save_path, f"failed_test_{idx+1}.jpg"), compared_image)
            
            # Save passed tests
            for idx, test in enumerate(self.passed_tests):
                compared_image = test[2]
                cv2.imwrite(os.path.join(save_path, f"passed_test_{idx+1}.jpg"), compared_image)
            
            messagebox.showinfo("Success", "Results saved successfully.")
        else:
            messagebox.showwarning("Warning", "No folder selected.")

    def load_control_image(self):
        """Load and display the control image."""
        try:
            # Open a dialog to select the control image
            self.control_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.tif")])
            
            # Open, resize, and display the image on the canvas
            control_img = Image.open(self.control_image_path)
            control_img = control_img.resize((360, 240), Image.ANTIALIAS)
            self.control_image = ImageTk.PhotoImage(control_img)
            self.control_canvas.create_image(0, 0, anchor=tk.NW, image=self.control_image)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading control image: {str(e)}")

    def load_test_image(self):
        """Load a test image, resize it, and display it on the canvas."""
        
        # multiple image formats  can be selected
        try:
            # Prompt the user to select an image
            self.test_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.tif")])
            
            # Open and read the selected image using the PIL library
            test_img = Image.open(self.test_image_path)
            
            # Resize the image to fit the canvas dimensions
            test_img = test_img.resize((360, 240), Image.ANTIALIAS)
            
            # Convert the PIL image to a format suitable for tkinter display
            self.test_image = ImageTk.PhotoImage(test_img)
            
            # Display the image on the test canvas
            self.test_canvas.create_image(0, 0, anchor=tk.NW, image=self.test_image)
        
        # Handle any exceptions that may arise during the process
        except Exception as e:
            messagebox.showerror("Error", f"Error loading test image: {str(e)}")


    def perform_inspection(self):
        """Perform a visual inspection comparing the control and test images."""
        
        try:
            # Ensure both control and test images are selected
            if not self.control_image_path or not self.test_image_path:
                messagebox.showerror("Error", "Both control and test images must be selected.")
                self.status_label.config(text="Status: Pending")
                return

            # Read the images in grayscale format using OpenCV
            control_img = cv2.imread(self.control_image_path, cv2.IMREAD_GRAYSCALE)
            test_img = cv2.imread(self.test_image_path, cv2.IMREAD_GRAYSCALE)

            # List of all the test functions to be applied
            tests = [
                self.check_for_written_items,
                self.check_for_missing_items,
                self.check_for_additions,
                self.check_for_cracks,
                self.check_orientation
            ]

            # Apply all tests and store the results
            results = [test(control_img, test_img) for test in tests]
            
            self.failed_tests = [result for result in results if result[0] == False]
            self.passed_tests = [result for result in results if result[0] != False]

            # If there are any failed tests, provide details on the reasons
            if self.failed_tests:
                reasons = "\n".join([test[1] for test in self.failed_tests])
                messagebox.showerror("Inspection Result", f"Inspection failed for the following reasons:\n\n{reasons}")
                self.status_label.config(text="Status: Fail")
                
            # Check for any warnings in the passed tests
            elif "Warning" in [test[1] for test in self.passed_tests]:
                self.status_label.config(text="Status: Pass with Warning")
                messagebox.showinfo("Inspection Result", "Inspection passed with warnings!")
            
            # If all tests passed, notify the user
            else:
                messagebox.showinfo("Inspection Result", "All tests passed successfully!")
                self.status_label.config(text="Status: Pass")

        # Handle any exceptions that might occur during the inspection process
        except Exception as e:
            messagebox.showerror("Error", f"Error during inspection: {str(e)}")
            self.status_label.config(text="Status: Error")

    def check_for_written_items(self, control_img, test_img):
        # Initialize SIFT detector
        sift = cv2.SIFT_create()

        # Detect keypoints and descriptors in both images
        keypoints1, descriptors1 = sift.detectAndCompute(control_img, None)
        keypoints2, descriptors2 = sift.detectAndCompute(test_img, None)

        # Initialize Brute-Force matcher
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(descriptors1, descriptors2, k=2)

        # Apply ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        # Check for significant changes in the number of matches
        if len(good_matches) < 0.8 * len(keypoints1):
            return (True, "Warning: Written items detected.", test_img)
        else:
            return (True, "No written items detected.", test_img)

    def check_for_additions(self, control_img, test_img):
        # Find contours in the test image but not in the control image
        diff = cv2.absdiff(test_img, control_img)
        contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            return (False, "Additions detected.", test_img)
        else:
            return (True, "No additions detected.", test_img)

    def check_for_missing_items(self, control_img, test_img):
        # Find contours in the control image but not in the test image
        diff = cv2.absdiff(control_img, test_img)
        contours, _ = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            return (False, "Missing items detected.", test_img)
        else:
            return (True, "No missing items detected.", test_img)

    def check_for_cracks(self, control_img, test_img):
        # Use edge detection and Hough line transform to detect cracks
        edges = cv2.Canny(test_img, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=10, maxLineGap=5)
        if lines is not None:
            return (True, "Warning: Cracks detected.", test_img)  # Changed this line to pass but with a warning
        else:
            return (True, "No cracks detected.", test_img)

    def check_orientation(self, control_img, test_img):
        # Use feature matching
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(control_img, None)
        kp2, des2 = orb.detectAndCompute(test_img, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        if len(matches) < 8:
            return (False, "Orientation mismatch detected.", test_img)
        else:
            return (True, "Orientation matches.", test_img)

if __name__ == "__main__":
    root = tk.Tk()
    app = ICVisualInspection(root)
    root.mainloop()

