import pyautogui
import cv2
import numpy as np
from time import sleep
from PIL import ImageGrab
import pygetwindow as gw
import winsound

def locate_button_in_window(button_image_path, app_window_title):
    try:
        # Get the window object (focus on the first matching window)
        window = gw.getWindowsWithTitle(app_window_title)[0]
        window_x, window_y, window_width, window_height = window.left, window.top, window.width, window.height

        # Capture only the window area
        screenshot = ImageGrab.grab(bbox=(window_x, window_y, window_x + window_width, window_y + window_height))
        screenshot_np = np.array(screenshot)

        # Convert to grayscale
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        # Load the button image
        button_image = cv2.imread(button_image_path, 0)

        # Match the template
        result = cv2.matchTemplate(screenshot_gray, button_image, cv2.TM_CCOEFF_NORMED)

        # Get the best match location
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Threshold to determine if the button is found
        threshold = 0.8
        if max_val >= threshold:
            # Adjust for window position (the button's location is relative to the window)
            return (max_loc[0] + window_x, max_loc[1] + window_y)  # return the global screen position
    except Exception as e:
        print(f"Error: {e}")
    return None

def click_button_in_window(button_image_path, app_window_title):
    # Run indefinitely, check screen every 10 seconds
    while True:
        # Locate the button inside the application window
        location = locate_button_in_window(button_image_path, app_window_title)

        # If the button is found, click it
        if location:
            print(f"Button found at: {location}")

            # Calculate the center of the button (adjust based on button size)
            button_width, button_height = 100, 50  # Replace with the actual size of the button image
            button_center = (location[0] + button_width / 2, location[1] + button_height / 2)

            # Move the mouse to the calculated center
            pyautogui.moveTo(button_center)
            pyautogui.click()
            print("Button clicked!")
        else:
            print("Button not found, checking again...")
            # Play a beep sound when the button is not found
            winsound.Beep(1000, 500)  # Frequency 1000 Hz, duration 500 ms

        # Wait 10 seconds before checking again
        sleep(10)

if __name__ == "__main__":
    # Path to the image of the button to click
    button_image_path = "button_print.png"

    # Title of the application window (must match exactly)
    app_window_title = "Browser Window"  # Replace with the actual window title
    
    try:
        # Start the function to check and click the button in a loop
        click_button_in_window(button_image_path, app_window_title)
    except KeyboardInterrupt:
        print("\nApplication stopped manually. Exiting...")
