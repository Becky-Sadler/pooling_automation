from opentrons import protocol_api 
import csv 
import sys
import re

metadata = {
    'apiLevel' :  '2.7',
    'protocolName' : 'Pooling Protocol',
    'author' : 'Becky Sadler',
    'description' : 'Pooling protocol for the TWIST library preparation'
}

''' 
Protocol Requirements: 

Pipettes: P20 GEN2 single channel 1-20ul (LEFT)

Custom Labware: 
    NonSkirted 96-well plate in flat plate holder (API Load name = 4t_96_wellplate_200ul)
    4x6 rack for 1.5ml microfuge tubes (API Load name = biomekmicrofuge_24_wellplate_1700ul)

Deck Layout:
    Position 10:    OpenTrons 20ul tip rack (opentrons_96_tiprack_20ul)
    Position 8:        NonSkirted 96-well plate in flat plate holder
    Position 7:        4x6 rack for 1.5ml microfuge tubes 

Liquid Handling properties:
    Aspirate height: 2mm from bottom
    Dispense height: 1mm from bottom at start increase by 0.5mm with each loop 
    Touch tip on aspirate: 2-3mm from top
    Blow out on the dispense (+0.5mm above dispense height)

Transfer process:
    Loop through the transfers from a csv file 
    Get tip (NEW ONE)
    Aspirate from well at 2mm 
    Touch tip (2-3mm from top)
    Dispense into well (At 1mm)
    Blow out (+0.5mm above)
    Touch tip (at different points each time)
    Drop tip. 
'''

# Sorting out data input - user input:  

worklist_number = None
#First test to see if the user has entered a numerical value:
while True:
    worklist_number = input('Please enter the worklist number: ')
    try:
        worklist_number = int(worklist_number)

        worklist_number = str(worklist_number)
        filename = worklist_number + '_pooling.csv'
        print('Worklist inputted is {0}'.format(worklist_number))
        break

#The alternative output for the first test code for if a non-numerical value is entered:
    except:
        print('Invalid input, please enter a numeric input')
        #Creates loop back up
        continue    

# Addition of code to catch the error where there is no CSV file for that worklist. 

try:
    # Open csv file and create reader 
    csvfile = open(filename, newline='')
except FileNotFoundError:
    print('Error: File {0}_pooling.csv cannot be found.'.format(worklist_number)) 
    print('Please check that the correct worklist number has been inputted.')
    print('If the worklist number is correct, please check that the CSV file has been uploaded to the robot')
    sys.exit()

reader = csv.DictReader(csvfile)

# Define the protocol desk set up and steps. 
def run(protocol: protocol_api.ProtocolContext):

# Add labware
    non_skirted_plate = protocol.load_labware('4t_96_wellplate_200ul', '8')
    biomek_tube_rack = protocol.load_labware('biomekmicrofuge_24_wellplate_1700ul', '7')
    tiprack_20ul = protocol.load_labware('opentrons_96_tiprack_20ul', '10')

    # Add pipettes
    left_pipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack_20ul])
    # Height for the aspirate and dispense doesn't change, so I will state outside the loop. 
    left_pipette.well_bottom_clearance.aspirate = 2
    left_pipette.well_bottom_clearance.dispense = 1
    
    #User input to specify starting tip to use 
    start_tip = ""

    while start_tip == "":
        start_tip = input("Please enter the starting tip: ")
        # Check the inputted value is valid location in the tip box e.g A1
        is_valid = re.match(r'[A-H][1-9]$|[A-H][0-1][0-2]', start_tip)
        if not is_valid:
            print('Invalid input, please re-enter the location of the starting tip')
            start_tip = ""
    
        # If start tip is valid, check that there will not be an out of tips error. 
        if is_valid:
            print('Start tip is {0}'.format(start_tip))
            left_pipette.starting_tip = tiprack_20ul.well(start_tip)
            
            try:
                # Transfers 
                for row in reader: 
                    left_pipette.pick_up_tip()
                    left_pipette.aspirate(float(row['Vol to Pool']), non_skirted_plate[(row['Well'])])
                    left_pipette.touch_tip(non_skirted_plate[(row['Well'])], speed = 20.0, v_offset = -3.0) 
                    # Blow out height is 0.5 above the dispense height (1 + 0.5) 
                    blow_out_height = 1.5
                    left_pipette.dispense(float(row['Vol to Pool']), biomek_tube_rack[row['Pool']])
                    left_pipette.move_to(biomek_tube_rack[row['Pool']].bottom(blow_out_height), force_direct=True)
                    left_pipette.touch_tip(biomek_tube_rack[(row['Pool'])], speed = 20.0, v_offset = -4.0) 
                    left_pipette.blow_out()
                    left_pipette.drop_tip()
            except protocol_api.labware.OutOfTipsError as e:
                print('Not enough tips to complete transfers. Please re-enter starting tip location')
                # If not enough tips - the user will be prompted to re-enter the tip location
                start_tip = ""

    
