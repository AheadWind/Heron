
import logging
import os
from pathlib import Path

heron_path = Path(os.path.dirname(os.path.realpath(__file__)))
logging.basicConfig(filename=os.path.join(heron_path, 'heron.log'), level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%H:%M:%S')

DATA_FORWARDER_SUBMIT_PORT = '5560'
DATA_FORWARDER_PUBLISH_PORT = '5561'
DATA_FORWARDER_CAPTURE_PORT = '5562'

PARAMETERS_FORWARDER_SUBMIT_PORT = '5563'
PARAMETERS_FORWARDER_PUBLISH_PORT = '5564'
PARAMETERS_FORWARDER_CAPTURE_PORT = '5565'

HEARTBEAT_FORWARDER_SUBMIT_PORT = '5566'
HEARTBEAT_FORWARDER_PUBLISH_PORT = '5567'
HEARTBEAT_FORWARDER_CAPTURE_PORT = '5568'

PROOF_OF_LIFE_FORWARDER_SUBMIT_PORT = '5569'
PROOF_OF_LIFE_FORWARDER_PUBLISH_PORT = '5570'
PROOF_OF_LIFE_FORWARDER_CAPTURE_PORT = '5571'

HEARTBEAT_RATE = 1  # in seconds
HEARTBEATS_TO_DEATH = 5

MAXIMUM_RESERVED_SOCKETS_PER_NODE = 20

NUMBER_OF_INITIAL_PARAMETERS_UPDATES = 5

IGNORE = 'Ignore'
