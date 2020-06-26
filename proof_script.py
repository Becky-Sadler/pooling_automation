from opentrons import protocol_api 

# version 2.4 is still in beta (can reduce speed of touch tip to 1mm/s in this one so upgarde?) - What is the robot software version? I've assumed 2.3 is ok for now, will query.  

metadata = {
	'protocolName' : 'Test Protocol'
	'author' : 'Becky Sadler'
	'description' : 'Proof of concept protocol to check that the simulation module works and the protocol runs correctly on the OT2'
	'api_level' :  '2.3'
}

'''
Protocol requirements: 

Pipettes: P20 GEN2 single channel 1-20ul (LEFT), P300 GEN2 single channel 20-300ul (RIGHT)

Custom Labware: 
	NonSkirted 96-well plate in flat plate holder (API Load name = 4t_96_wellplate_200ul)
	4x6 rack for 1.5ml microfuge tubes (API Load name = biomekmicrofuge_24_wellplate_1700ul)

Deck Layout:
	Position 10:	OpenTrons 20ul tip rack (opentrons_96_tiprack_20ul)
	Position 11:	OpenTrons 300ul tip rack (opentrons_96_tiprack_300ul)
	Position 8:		NonSkirted 96-well plate in flat plate holder
	Position 7:		4x6 rack for 1.5ml microfuge tubes (Wells used: A1 D1 500ul in each)

Liquid Handling properties:
	Aspirate at 5mm from the bottom of the well.
	Dispense at 1mm from the bottom of the well.
	Do some tip touch commands (Vary the speed).

Transfers:
	1: {
	Source Position : 7
	Source Well : A1
	Destination Position : 8
	Destination Well : A1
	Volume : 10ul 
	}
	2: {
	Source Position : 7
	Source Well : A6/D1?
	Destination Position : 8
	Destination Well : H1
	Volume : 10ul
	}
	3: {
	Source Position : 7
	Source Well : A1
	Destination Position : 8
	Destination Well : A12
	Volume : 150ul
	}
	4: {
	Source Position : 7
	Source Well : A6/D1
	Destination Position : 8
	Destination Well : H12
	Volume : 150ul 
	}

'''

def run(protocol: protocol_api.ProtocolContext):

	# Add labware
	non_skirted_plate = protocol.load_labware('4t_96_wellplate_200ul', '8')
	biomek_tube_rack = protocol.load_labware('biomekmicrofuge_24_wellplate_1700ul', '7')
	20ul_tiprack = protocol.load_labware('opentrons_96_tiprack_20ul', '10')
	300ul_tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '11')

	# Add pipettes
	left_pipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[20ul_tiprack])
	right_pipette = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[300ul_tiprack])

	# Commands

	# Command 1:
	left_pipette.pick_up_tip()
	left_pipette.aspirate(10, biomek_tube_rack['A1'])
	left_pipette.tip_touch(well = 'A1' speed = 20.0) 
	left_pipette.dispense(10, non_skirted_plate['A1'])
	left_pipette.tip_touch() 
	left_pipette.drop_tip()

	# Command 2: 
	left_pipette.pick_up_tip()
	left_pipette.aspirate(10, biomek_tube_rack['D1'])
	left_pipette.tip_touch() 
	left_pipette.dispense(10, non_skirted_plate['H1'])
	left_pipette.tip_touch() 
	left_pipette.drop_tip()

	# Command 3:
	right_pipette.pick_up_tip()
	right_pipette.aspirate(150, biomek_tube_rack['A1'])
	right_pipette.tip_touch() 
	right_pipette.dispense(150, non_skirted_plate['A12'])
	right_pipette.tip_touch() 
	right_pipette.drop_tip()

	# Command 4:
	right_pipette.pick_up_tip()
	right_pipette.aspirate(150,biomek_tube_rack['D1'])
	right_pipette.tip_touch() 
	right_pipette.dispense(150, non_skirted_plate['H12'])
	right_pipette.tip_touch() 
	right_pipette.drop_tip()







