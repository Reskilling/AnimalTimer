AnimalTimer App

AnimalTimer is a Python desktop application built using Tkinter and PIL (Pillow) for managing feeding schedules for pets.

Features

    Feeding Reminder: Notifies you when it's time to feed your pet.
    Interactive Interface: Simple GUI with buttons for feeding and toggling fullscreen mode.
    Customizable Settings: You can set morning and evening feeding times and update UI configurations.

Requirements

    Python 3.6+
    Tkinter (usually included with Python installations)
    PIL (Pillow) library (pip install pillow)

Installation

    Clone the repository:
    git clone https://github.com/Reskilling/AnimalTimer.git
    
Navigate to the project directory
    
    cd AnimalTimer

Install the required dependencies:

    pip install pillow
    pip install tkinter

Usage

Run the application:

    python AnimalTimer.py

    The application window will open, displaying the main interface.

    Click on the dog bowl icon to indicate that your pet has been fed.

    You can toggle fullscreen mode using the fullscreen button located at the top right corner.


Alternatively you can download the AnimalTimer.exe I have provided.

Customization

You can customize the application behavior by modifying the AppConfig class variables in AnimalTimer.py:

    RESET_TIME_MORNING: Morning feeding reset time (default: 6:00 AM)
    RESET_TIME_EVENING: Evening feeding reset time (default: 4:30 PM)
    UPDATE_INTERVAL: Timer update interval in milliseconds (default: 1000 ms)
    FONT_STYLE: Font style used for text elements
    TEXT_COLOR: Color of the text elements

This application was developed as a learning project based on Tkinter GUI programming and timer management in Python.
License

This project is licensed under the MIT License - see the LICENSE file for details.
