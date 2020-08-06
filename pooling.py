from opentrons import protocol_api 
import csv 

metadata = {
	'apiLevel' :  '2.5',
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
	Position 10:	OpenTrons 20ul tip rack (opentrons_96_tiprack_20ul)
	Position 8:		NonSkirted 96-well plate in flat plate holder
	Position 7:		4x6 rack for 1.5ml microfuge tubes 

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

# Sorting out data input: 

csv_name = 'test_pooling.csv'

csvfile = open(csv_name, newline='')
reader = csv.DictReader(csvfile)

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
