#!/usr/bin/env python

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from image_processing import search
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCompleter, QMessageBox, QCheckBox
from PIL import ImageGrab
import os
import cv2
import numpy as np

always_dejavu = False

class Ui_MainWindow(object):
    def setup_ui(self, MainWindow):
        # main window setup
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1100, 900)
        MainWindow.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        MainWindow.setWindowTitle("DBDL Perk Checker - by sanmta")
        MainWindow.setWindowIcon(QtGui.QIcon("assets/DBDL.png"))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        create_background_label(self, 0, 0)

        # dictionary to hold line edit widgets
        self.line_edits = {
            'searchPerk_1_Build_1': 'lblPerk_1_Build_1', 
            'searchPerk_2_Build_1': 'lblPerk_2_Build_1', 
            'searchPerk_3_Build_1': 'lblPerk_3_Build_1', 
            'searchPerk_4_Build_1': 'lblPerk_4_Build_1',                 
            'searchPerk_1_Build_2': 'lblPerk_1_Build_2', 
            'searchPerk_2_Build_2': 'lblPerk_2_Build_2', 
            'searchPerk_3_Build_2': 'lblPerk_3_Build_2', 
            'searchPerk_4_Build_2': 'lblPerk_4_Build_2',
            'searchPerk_1_Build_3': 'lblPerk_1_Build_3', 
            'searchPerk_2_Build_3': 'lblPerk_2_Build_3', 
            'searchPerk_3_Build_3': 'lblPerk_3_Build_3', 
            'searchPerk_4_Build_3': 'lblPerk_4_Build_3',
            'searchPerk_1_Build_4': 'lblPerk_1_Build_4', 
            'searchPerk_2_Build_4': 'lblPerk_2_Build_4', 
            'searchPerk_3_Build_4': 'lblPerk_3_Build_4', 
            'searchPerk_4_Build_4': 'lblPerk_4_Build_4'
        }        
        
        for i in range(1, 5): 
            create_build_label(self, str(i), 279, 25 + 202*(i-1)) 
            for j in range(1, 5):
                create_perk_icon(self, str(j), str(i), 180*(j) + 80, 205*(i-1) + 85) 
                create_perk_search_bar(self, str(j), str(i), 180 * j + 80, 205*(i-1) + 58) 

        self.checkbox_eyes = create_checkbox(self, "Assume eye perks are Deja Vu", 40, 846, 200, 22)
        self.checkbox_eyes.stateChanged.connect(self.checkbox_toggled)
        
        btn_paste = create_button(self, 380, 840, 261, 31, "Check Perks")
        btn_reset = create_button(self, 660, 840, 171, 31, "Reset")

        btn_paste.clicked.connect(lambda: paste_image(self))
        btn_reset.clicked.connect(lambda: reset_perks(self))

        MainWindow.show()

    # function that controls effect of the checkbox being toggled
    def checkbox_toggled(value, state):
        global always_dejavu
        if state == Qt.CheckState.Checked.value:
            always_dejavu = True
            print("Always Deja Vu is now True")
        elif state == Qt.CheckState.Unchecked.value:
            always_dejavu = False
            print("Always Deja Vu is now False")

# function to get an image from clipboard and search for perks
def paste_image(self):
    clipboard_image = ImageGrab.grabclipboard() # get image from clipboard

    if (clipboard_image is not None):
        if (clipboard_image.size == (1920, 1032)): # check if image is 1920x1080 (minus task)
            # convert the Pillow Image to a NumPy array
            end_screen = cv2.cvtColor(np.array(clipboard_image), cv2.COLOR_RGB2BGR)
            create_perk_arrays(self, search(end_screen, always_dejavu))
        else:
            show_error_message("Error", "Image size is not 1920x1080.")
    else:
        show_error_message("Error", "No image found in clipboard.")

# function to create arrays of both selected perks and detected perks
def create_perk_arrays(self, perks):
    detected_build1 = [perk.replace("iconPerks_", "").replace(".jpg", "").lower() for perk in perks[0:4]]
    detected_build2 = [perk.replace("iconPerks_", "").replace(".jpg", "").lower() for perk in perks[4:8]]
    detected_build3 = [perk.replace("iconPerks_", "").replace(".jpg", "").lower() for perk in perks[8:12]]
    detected_build4 = [perk.replace("iconPerks_", "").replace(".jpg", "").lower() for perk in perks[12:16]]

    expected_build1 = [
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_1_Build_1").text()).lower(),
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_2_Build_1").text()).lower(),
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_3_Build_1").text()).lower(),
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_4_Build_1").text()).lower()
    ]
    
    expected_build2 = [
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_1_Build_2").text()).lower(), 
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_2_Build_2").text()).lower(), 
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_3_Build_2").text()).lower(), 
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_4_Build_2").text()).lower()
    ]
    
    expected_build3 = [
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_1_Build_3").text()).lower(),
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_2_Build_3").text()).lower(),
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_3_Build_3").text()).lower(),
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_4_Build_3").text()).lower()
    ]

    expected_build4 = [
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_1_Build_4").text()).lower(), 
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_2_Build_4").text()).lower(), 
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_3_Build_4").text()).lower(), 
        format_perk_name(self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_4_Build_4").text()).lower()
    ]

    check_perks(self, detected_build1, detected_build2, detected_build3, detected_build4, expected_build1, 1)
    check_perks(self, detected_build1, detected_build2, detected_build3, detected_build4, expected_build2, 2)
    check_perks(self, detected_build1, detected_build2, detected_build3, detected_build4, expected_build3, 3)
    check_perks(self, detected_build1, detected_build2, detected_build3, detected_build4, expected_build4, 4)

# function to check if the perks in the build exist
def check_perks(self, d1, d2, d3, d4, expected_build, build_no):
    if ((sorted(d1) == sorted(expected_build)) == True):
        set_perk_backgrounds(self, 1, True, None)
    elif ((sorted(d2) == sorted(expected_build)) == True):
        set_perk_backgrounds(self, 2, True, None)
    elif ((sorted(d3) == sorted(expected_build)) == True):
        set_perk_backgrounds(self, 3, True, None)
    elif ((sorted(d4) == sorted(expected_build)) == True):
        set_perk_backgrounds(self, 4, True, None)
    else:
        if build_no == 1:
            non_matching_d1 = find_non_matching_values(d1, expected_build)
            set_perk_backgrounds(self, build_no, False, non_matching_d1)
            show_error_message("Error", f"{non_matching_d1} not found in build " + str(build_no) + ".")
        elif build_no == 2:
            non_matching_d2 = find_non_matching_values(d2, expected_build)
            set_perk_backgrounds(self, build_no, False, non_matching_d2)
            show_error_message("Error", f"{non_matching_d2} not found in build " + str(build_no) + ".")
        elif build_no == 3:
            non_matching_d3 = find_non_matching_values(d3, expected_build)
            set_perk_backgrounds(self, build_no, False, non_matching_d3)
            show_error_message("Error", f"{non_matching_d3} not found in build " + str(build_no) + ".")
        elif build_no == 4:
            non_matching_d4 = find_non_matching_values(d4, expected_build)
            set_perk_backgrounds(self, build_no, False, non_matching_d4)
            show_error_message("Error", f"{non_matching_d4} not found in build " + str(build_no) + ".")

# function to set the background of the perk icons, green being a correct perk and red being incorrect
def set_perk_backgrounds(self, build_no, correct, non_matching_values):
    if correct:    
        for perk_no in range(1, 5):
            perk_bg = self.centralwidget.findChild(QtWidgets.QLabel, "lblPerkBG_" + str(perk_no) + "_Build_" + str(build_no))
            perk_bg.setPixmap(QtGui.QPixmap("assets/perks/perkBGCorrect.png"))
    else:
        for perk_no in range(1, 5):
            if any(perk_no == i for i, _ in non_matching_values):            
                perk_bg = self.centralwidget.findChild(QtWidgets.QLabel, "lblPerkBG_" + str(perk_no) + "_Build_" + str(build_no))
                perk_bg.setPixmap(QtGui.QPixmap("assets/perks/perkBGIncorrect.png"))
            else:
                perk_bg = self.centralwidget.findChild(QtWidgets.QLabel, "lblPerkBG_" + str(perk_no) + "_Build_" + str(build_no))
                perk_bg.setPixmap(QtGui.QPixmap("assets/perks/perkBGCorrect.png"))

# additional function to get the differences between two builds
def find_non_matching_values(d, expected):
    non_matching_values = []
    for i, item in enumerate(expected):
        if item not in d:
            non_matching_values.append((i+1, item))
    return non_matching_values

# function to show an error message
def show_error_message(title, message):
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Icon.Critical)
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()

# function to show a confirmation message
def show_are_you_sure_popup():
    # Create a QMessageBox
    msg_box = QMessageBox()

    # Set the icon, title, and text
    msg_box.setIcon(QMessageBox.Icon.Question)
    msg_box.setWindowTitle("Confirmation")
    msg_box.setText("Are you sure you want to proceed?")

    # Add buttons for the user to confirm or cancel the action
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    # Execute the message box and return the user's response
    return msg_box.exec()

# function to create a checkbox widget
def create_checkbox(self, text, x, y, w, h):
    checkbox = QCheckBox(parent=self.centralwidget)
    checkbox.setGeometry(QtCore.QRect(x, y, w, h))
    checkbox.setObjectName("chk_" + text)
    checkbox.setText(text)
    checkbox.setChecked(True)
    return checkbox

# function to create a background label
def create_background_label(self, x, y):
    _translate = QtCore.QCoreApplication.translate
    label_build = QtWidgets.QLabel(parent=self.centralwidget)
    label_build.setGeometry(QtCore.QRect(x, y, 1100, 900))
    label_build.setPixmap(QtGui.QPixmap("assets/main_background.png"))

# function to create a label for each build
def create_build_label(self, build_no, x, y):
    _translate = QtCore.QCoreApplication.translate
    label_build = QtWidgets.QLabel(parent=self.centralwidget)
    label_build.setGeometry(QtCore.QRect(x, y, 100, 22))
    font = QtGui.QFont()
    font.setFamily("Roboto Condensed")
    font.setBold(True)
    font.setPointSize(23)
    label_build.setFont(font)
    label_build.setObjectName("lblBuild_" + build_no)
    label_build.setText(_translate("MainWindow", "BUILD "  + build_no + ":"))

# function to create a perk icon for each perk
def create_perk_icon(self, perk_no, build_no, x, y):
    # create background for icon
    perk_icon_bg = QtWidgets.QLabel(parent=self.centralwidget)
    perk_icon_bg.setGeometry(QtCore.QRect(x, y, 125, 125))
    perk_icon_bg.setPixmap(QtGui.QPixmap("assets/perks/perkBG.png"))
    perk_icon_bg.setScaledContents(True)
    perk_icon_bg.setObjectName("lblPerkBG_" + perk_no + "_Build_" + build_no)
    # create icon on top of background
    perk_icon = QtWidgets.QLabel(parent=self.centralwidget)
    perk_icon.setGeometry(QtCore.QRect(x, y, 125, 125))
    perk_icon.setPixmap(QtGui.QPixmap(""))
    perk_icon.setScaledContents(True)
    perk_icon.setObjectName("lblPerk_" + perk_no + "_Build_" + build_no)     

# function to try and update the perk icon when the search bar is changed
def on_selection_changed(self, perk_search_bar):
    object_name = perk_search_bar.objectName()
    perk_no = object_name.split('_')[1]  
    build_no = object_name.split('_')[3]
    # get the perk_icon object
    perk_icon = self.centralwidget.findChild(QtWidgets.QLabel, "lblPerk_" + perk_no + "_Build_" + build_no)
    try_icon_update(perk_search_bar, perk_icon)
    
# function to update perk icon when selection box changes
def try_icon_update(perk_search_bar, perk_icon):
    perk = format_perk_name(perk_search_bar.text())
    if (perk_exists(perk) == True):
        perk_icon.setPixmap(QtGui.QPixmap("assets/perks/iconPerks_" + perk + ".png"))
        perk_icon.show()
        return True
    else:
        perk_icon.hide()
        return False

# function to check if perk exists in the assets folder
def perk_exists(perk_name):
    if (os.path.exists("assets/perks/iconPerks_" + perk_name + ".png")): return True
    else: return False

# function to create a search bar for each perk
def create_perk_search_bar(self, perk_no, build_no, x, y):
    perk_search_bar = QtWidgets.QLineEdit(parent=self.centralwidget)
    perk_search_bar.setGeometry(QtCore.QRect(x, y, 130, 20))
    perk_search_bar.setObjectName("searchPerk_" + perk_no + "_Build_" + build_no) 
    # create completer for the search bar
    completer = list_of_all_perks()
    completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
    perk_search_bar.setCompleter(completer)
    perk_search_bar.textChanged.connect(lambda: on_selection_changed(self, perk_search_bar))
    return perk_search_bar

# function to create a custom button
def create_button(self, x, y, width, height, text):
    button = QtWidgets.QPushButton(parent=self.centralwidget)
    button.setGeometry(QtCore.QRect(x, y, width, height))
    font = QtGui.QFont()
    font.setFamily("Roboto")
    font.setPointSize(16)
    button.setFont(font)
    button.setObjectName("btn_" + text)
    button.setText(text)
    return button

# function to reset all perk search bars, this will in turn reset all the perk icons
def reset_perks(self):
    response = show_are_you_sure_popup()
    
    if response == QMessageBox.StandardButton.Yes:
        for i in range(1, 5):
            for j in range(1, 5): 
                line_edit = self.centralwidget.findChild(QtWidgets.QLineEdit, "searchPerk_" + str(j) + "_Build_" + str(i))
                line_edit.clear()

                perk_bg = self.centralwidget.findChild(QtWidgets.QLabel, "lblPerkBG_" + str(j) + "_Build_" + str(i))
                perk_bg.setPixmap(QtGui.QPixmap("assets/perks/perkBG.png"))

# function to format perk name into valid path to locate the perk icon
def format_perk_name(input_string):
    # Remove : ' - and extra spaces from the string
    formatted_string = input_string.replace(":", "").replace("'", "").replace("-", "").replace(" ", "")
    # Capitalize each word individually
    formatted_string = " ".join(word.capitalize() for word in formatted_string.split())
    return formatted_string

# function to return a QCompleter object with a list of all survivor perks
def list_of_all_perks():
    return QCompleter([
        'Ace in the Hole',
        'Adrenaline',
        'Aftercare',
        'Alert',
        'Any Means Necessary',
        'Appraisal',
        'Autodidact',
        'Babysitter',
        'Background Player',
        'Balanced Landing',
        'Bardic Inspiration',
        'Better Together',
        'Better Than New',
        'Bite the Bullet',
        'Blast Mine',
        'Blood Pact',
        'Blood Rush',
        'Boil Over',
        'Bond',
        'Boon: Circle of Healing',
        'Boon: Dark Theory',
        'Boon: Exponential',
        'Boon: Illumination',
        'Boon: Shadow Step',
        'Borrowed Time',
        'Botany Knowledge',
        'Breakdown',
        'Breakout',
        'Buckle Up',
        'Built to Last',
        'Calm Spirit',
        'Camaraderie',
        'Champion of Light',
        'Chemical Trap',
        'Clairvoyance',
        'Corrective Action',
        'Counterforce',
        'Cut Loose',
        'Dance With Me',
        'Dark Sense',
        'Dead Hard',
        'Deadline',
        'Deception',
        'Decisive Strike',
        'Deja Vu',
        'Deliverance',
        'Desperate Measures',
        'Detective\'s Hunch',
        'Distortion',
        'Diversion',
        'Dramaturgy',
        'Empathic Connection',
        'Empathy',
        'Fast Track',
        'Fixated',
        'Flashbang',
        'Flip-Flop',
        'Fogwise',
        'For the People',
        'Friendly Competition',
        'Head On',
        'Hope',
        'Hyperfocus',
        'Inner Focus',
        'Inner Strength',
        'Invocation: Weaving Spiders',
        'Iron Will',
        'Kindred',
        'Leader',
        'Left Behind',
        'Light-Footed',
        'Lightweight',
        'Lithe',
        'Low Profile',
        'Lucky Break',
        'Lucky Star',
        'Made For This',
        'Mettle of Man',
        'Mirrored Illusion',
        'No Mither',
        'No One Left Behind',
        'Object of Obsession',
        'Off the Record',
        'Open-Handed',
        'Overcome',
        'Overzealous',
        'Parental Guidance',
        'Pharmacy',
        'Plot Twist',
        'Plunderer\'s Instinct',
        'Poised',
        'Potential Energy',
        'Power Struggle',
        'Premonition',
        'Prove Thyself',
        'Quick and Quiet',
        'Quick Gambit',
        'Reactive Healing',
        'Reassurance',
        'Red Herring',
        'Repressed Alliance',
        'Residual Manifest',
        'Resilience',
        'Resurgence',
        'Rookie Spirit',
        'Saboteur',
        'Scavenger',
        'Scene Partner',
        'Second Wind',
        'Self-Care',
        'Self-Preservation',
        'Slippery Meat',
        'Small Game',
        'Smash Hit',
        'Sole Survivor',
        'Solidarity',
        'Soul Guard',
        'Spine Chill',
        'Sprint Burst',
        'Stake Out',
        'Still Sight',
        'Streetwise',
        'Strength in Shadows',
        'Teamwork: Collective Stealth',
        'Teamwork: Power of Two',
        'Technician',
        'Tenacity',
        'This is Not Happening',
        'Troubleshooter',
        'Unbreakable',
        'Up the Ante',
        'Urban Evasion',
        'Vigil',
        'Visionary',
        'Wake Up!',
        'We\'ll Make It',
        'We\'re Gonna Live Forever',
        'Wicked',
        'Windows of Opportunity',
        'Wiretap'
    ])

# main function
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
