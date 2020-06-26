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

Pipettes: P20 GEN2 single channel (LEFT), P300 GEN2 single channel (RIGHT)

Custom Labware: 
	NonSkirted 96-well plate in flat plate holder (API Load name = 4t_96_wellplate_200ul)
	4x6 rack for 1.5ml microfuge tubes (API Load name = biomekmicrofuge_24_wellplate_1700ul)

Deck Layout:
	Position 10:	OpenTrons 20ul tip rack
	Position 11:	OpenTrons 300ul tip rack
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





