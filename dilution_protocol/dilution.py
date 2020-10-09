from opentrons import protocol_api 
import csv 

metadata = {
	'apiLevel' :  '2.4',
	'protocolName' : 'Test Dilution Protocol',
	'author' : 'Becky Sadler',
	'description' : 'Test protocol for dilution'
}

''' 
Protocol Requirements: 

Pipettes: P20 GEN2 single channel 1-20ul (LEFT), P300 GEN2 single channel 20-300ul (RIGHT)

Custom Labware: 
	NonSkirted 96-well plate in flat plate holder (API Load name = 4t_96_wellplate_200ul)

Deck Layout:
	Position 10:	OpenTrons 20ul tip rack (opentrons_96_tiprack_20ul)
	Position 11:	OpenTrons 300ul tip rack (opentrons_96_tiprack_300ul)
	Position 8:		NonSkirted 96-well plate in flat plate holder (Plate 1 - full strength)
	Position 7:		NonSkirted 96-well plate in flat plate holder (Plate 2 - Diluted)
	Position 4:		4x6 rack for 1.5ml microfuge tubes (Water pot - A1) ???Would water be held this way???

Liquid Handling properties:
	??? Do these need to change????
	Aspirate height: 2mm from bottom
	Dispense height: 1mm from bottom at start increase by 0.5mm with each loop 
	Touch tip on aspirate: 2-3mm from top

Transfer process:
	Adding water to the diluted plate:
	Get tip 
	Aspirate 200ul of water 
	Touch tip (2-3mm from top)
	Cycle through water values in csv and dispense appropriate amount in each. 
	Have loop to make sure that the amount of water in the tip is always enough for next dispense. 

	Loop through the dna transfers from a csv file
	Get tip (NEW ONE)
	Aspirate from well at 2mm 
	Touch tip (2-3mm from top)
	Dispense into well (At 1mm)
	Blow out (+0.5mm above) - ??? Should this instead be a mix ??? 
	Touch tip 
	Drop tip. 
'''

csv_name = '11111_dilution.csv'

source_welllist=[]
destination_welllist = []
dnalist=[]
waterlist=[]
with open(csv_name, newline='') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')
	for row in reader:
		source_welllist.append(row['SourceWell'])
		destination_welllist.append(row['DestinationWell'])
		dnalist.append(float(row['Vol of dna']))
		waterlist.append(float(row['Vol of water']))

def run(protocol: protocol_api.ProtocolContext):

	# Add labware
	dna_plate = protocol.load_labware('4t_96_wellplate_200ul', '8')
	dilution_plate = protocol.load_labware('4t_96_wellplate_200ul', '7')
	biomek_tube_rack = protocol.load_labware('biomekmicrofuge_24_wellplate_1700ul', '4')
	tiprack_20ul = protocol.load_labware('opentrons_96_tiprack_20ul', '10')
	tiprack_300ul = protocol.load_labware('opentrons_96_tiprack_300ul', '11')

	# Add pipettes
	left_pipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack_20ul])
	right_pipette = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_300ul])
	# Height for the aspirate and dispense doesn't change, so I will state outside the loop. 
	left_pipette.well_bottom_clearance.aspirate = 2
	left_pipette.well_bottom_clearance.dispense = 1
	right_pipette.well_bottom_clearance.aspirate = 2
	right_pipette.well_bottom_clearance.dispense = 1
	
	# Add water via distribute (disposal volume is 20ul - the minimum for the pipette)
	right_pipette.distribute(waterlist, biomek_tube_rack['A1'], [dilution_plate.wells_by_name()[well_name] for well_name in destination_welllist], touch_tip=True, disposal_volume=20 )

	# Transfer DNA using Transfer function (Mixing after each dispense with maximum volume of pipette + tip touch)

	left_pipette.transfer(dnalist, [dna_plate.wells_by_name()[source_well_name] for source_well_name in source_welllist], [dilution_plate.wells_by_name()[destination_well_name]for destination_well_name in destination_welllist], new_tip='always', mix_after=(8, 20), touch_tip=True)
