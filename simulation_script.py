# Can python -m opentrons.simulate /path/to/protocol 
import opentrons.simulate

protocol_file = open('/path/to/protocol.py')
opentrons.simulate.simulate(protocol_file)