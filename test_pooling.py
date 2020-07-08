from opentrons import protocol_api 
import csv 

# Use 'author' to specify the operator? 
metadata = {
	'apiLevel' :  '2.4',
	'protocolName' : 'Test Pooling Protocol',
	'author' : 'Becky Sadler',
	'description' : 'Protocol to check that the functions used for pooling work as expected'
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
	Position 7:		4x6 rack for 1.5ml microfuge tubes (Wells used: A1 D1 500ul in each)

Liquid Handling properties:
	Aspirate height: 2mm from bottom
	Dispense height: 1mm from bottom at start increase by 0.5mm with each loop 
	Touch tip on aspirate: 2-3mm from top
	Blow out on the dispense (+0.5mm above dispense height)

Transfer process:
	Loop through the transfers from a csv (Exact process to be discussed - might change with StarLIMS integration)
	Get tip (NEW ONE)
	Aspirate from well at 2mm 
	Touch tip (2-3mm from top)
	Dispense into well (Initially at 1mm)
	Blow out (+0.5mm above)
	Drop tip. 
'''

# Sorting out data input: 

data = '''Well,Vol to Pool,Pool,PreCap Worklist,MID,Sample ID,Library conc
A1,2.16,AA,2010750,U001,00000000,86.72
B1,1.92,AA,2010750,U002,00000000,97.66
C1,1.94,AA,2010750,U003,00000000,96.50
D1,1.85,AA,2010750,U004,00000000,101.21
E1,1.89,AA,2010750,U005,00000000,99.01
F1,1.90,AA,2010750,U006,00000000,98.63
G1,1.77,AA,2010750,U007,00000000,105.78
H1,1.79,AA,2010750,U008,00000000,104.59
A2,1.94,AB,2010750,U009,00000000,96.61
B2,1.94,AB,2010750,U010,00000000,96.56
C2,2.12,AB,2010750,U011,00000000,88.62
D2,2.02,AB,2010750,U012,00000000,92.70
E2,2.54,AB,2010750,U013,00000000,73.81
F2,2.08,AB,2010750,U014,00000000,90.13
G2,1.98,AB,2010750,U015,00000000,94.86
H2,1.86,AB,2010750,U016,00000000,100.91
A3,1.91,AC,2010750,U017,00000000,97.94
B3,1.80,AC,2010750,U018,00000000,104.44
C3,1.85,AC,2010750,U019,00000000,101.33
D3,1.84,AC,2010750,U020,00000000,102.00
E3,1.92,AC,2010750,U021,00000000,97.89
E3,1.92,AC,2010750,U021,00000000,97.89
F3,2.00,AC,2010750,U022,00000000,93.91
G3,2.23,AC,2010750,U023,00000000,84.03
H3,1.91,AC,2010750,U024,00000000,97.94
A4,1.80,AD,2010750,U025,00000000,104.40
B4,1.98,AD,2010750,U026,00000000,94.89
C4,1.89,AD,2010750,U027,00000000,99.45
D4,1.74,AD,2010750,U028,00000000,107.58
E4,1.79,AD,2010750,U029,00000000,105.04
F4,2.10,AD,2010750,U030,00000000,89.41
G4,2.04,AD,2010750,U031,00000000,91.81
H4,2.06,AD,2010750,U032,00000000,90.92
'''

csv_data = data.splitlines() 
reader = csv.DictReader(csv_data)

def run(protocol: protocol_api.ProtocolContext):

	# Add labware
	non_skirted_plate = protocol.load_labware('4t_96_wellplate_200ul', '8')
	biomek_tube_rack = protocol.load_labware('biomekmicrofuge_24_wellplate_1700ul', '7')
	tiprack_20ul = protocol.load_labware('opentrons_96_tiprack_20ul', '10')

	# Add pipettes
	left_pipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack_20ul])
	# Height for the aspirate doesn't change, so I will state outside the loop. Variable for dispense also created here.
	left_pipette.well_bottom_clearance.aspirate = 2
	dispense_height = 1

	# Transfers - .transfer() not specific enough for what is needed.
	for row in reader: 
		left_pipette.pick_up_tip()
		left_pipette.aspirate(float(row['Vol to Pool']), non_skirted_plate[(row['Well'])])
		left_pipette.touch_tip(non_skirted_plate[(row['Well'])], speed = 20.0, v_offset = -3.0) 
		left_pipette.well_bottom_clearance.dispense = dispense_height
		blow_out_height = dispense_height + 0.5
		if row['Pool'] == 'AA':
			left_pipette.dispense(float(row['Vol to Pool']), biomek_tube_rack['A1'])
			left_pipette.move_to(biomek_tube_rack['A1'].bottom(blow_out_height), force_direct=True)
		if row['Pool'] == 'AB':
			left_pipette.dispense(float(row['Vol to Pool']), biomek_tube_rack['B1'])
			left_pipette.move_to(biomek_tube_rack['B1'].bottom(blow_out_height), force_direct=True)
		if row['Pool'] == 'AC':
			left_pipette.dispense(float(row['Vol to Pool']), biomek_tube_rack['C1'])
			left_pipette.move_to(biomek_tube_rack['C1'].bottom(blow_out_height), force_direct=True)
		if row['Pool'] == 'AD':
			left_pipette.dispense(float(row['Vol to Pool']), biomek_tube_rack['D1'])
			left_pipette.move_to(biomek_tube_rack['D1'].bottom(blow_out_height), force_direct=True)
		left_pipette.blow_out() 
		left_pipette.drop_tip()
		if dispense_height <= 4.0:
			dispense_height += 0.5
		else: 
			dispense_height = 1




		



