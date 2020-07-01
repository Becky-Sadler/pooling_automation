from opentrons import protocol_api 

metadata = {
	'apiLevel' :  '2.4',
	'protocolName' : 'Test Pooling Protocol',
	'author' : 'Becky Sadler',
	'description' : 'Protocol to check that the functions used for pooling work as expected'
}

''' 
Protocol Requirements: 

Requirements/Information

Create a starlims script that creates a *.py file to pool twist samples from (at least) 32 individual wells in a 96 well plate into 1.5ml tubes (8 source wells per destination tube).

Each source well will have a different volume to be transferred into the pooling well. 

Users currently run the script PlateWorkflowLifeCycle.AssignPools to assign the pool letter and calculate the transfer volume.  At the end of this all the information you need about the source plate can be found in the starlims database table WELLPLATESAMPLERESULTS.

	I would suggest that we create a function to run at the end of this script to create the python file.

The pooling well positions are not fixed, but we may need to write back into starlims if they may change.

	 We could try code this into the above script and write to  WELLPLATESAMPLERESULTS before trying to make the python script so it’s already there?

Pools have letter designations and these cannot correspond to final well positions (as ther are too many possibilities!)

Typically, <5ul will be transferred, so we need to make sure as little as possible from the outside of the tip is transferred into the final pool.

	This is where a moving aspirate could help; if we can do this, we’d want to mix on the dispense.

	Alternatively each droplet could have a tip touch onto a different part of the well – e.g. the first patient to the top, 2mm from the bottom, the next 4mm, and so on.  This would ensure the outside residual volume isn’t mixed into any other liquid.

	Due to the volume we can use the P20 Gen2 on the left side.

'''

def run(protocol: protocol_api.ProtocolContext):

	# Add labware
	tiprack_20ul = protocol.load_labware('opentrons_96_tiprack_20ul', '10')

	# Add pipettes
	left_pipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack_20ul])
	right_pipette = protocol.load_instrument('PIPETTE_NAME', 'right', tip_racks=[tiprack])
	# Change default aspirate/dispence height 
	left_pipette.well_bottom_clearance.aspirate = value
	right_pipette.well_bottom_clearance.aspirate = value
	left_pipette.well_bottom_clearance.dispense = value
	right_pipette.well_bottom_clearance.dispense = value

	# Transfers
	


