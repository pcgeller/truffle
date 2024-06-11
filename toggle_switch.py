from gpiozero import Button
from signal import pause

# Define the GPIO pin connected to the toggle switch
TOGGLE_PIN = 26

# Function to execute when the toggle button is turned on
def execute_script():
    print("The rest of the script is executing!")
    # Add the rest of your script here
    # For example:
    print("The script is now running...")

# Setup the button
toggle_switch = Button(TOGGLE_PIN)

# Assign the execute_script function to run when the button is pressed
toggle_switch.when_pressed = execute_script

print("Listening for toggle switch...")

# Pause the script to keep it running and listening for the button press
pause()