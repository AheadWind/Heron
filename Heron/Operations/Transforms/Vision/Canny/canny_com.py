
import os
from Heron import general_utils as gu
Exec = os.path.realpath(__file__)


# <editor-fold desc="The following code is called from the GUI process as part of the generation of the node.
# It is meant to create node specific elements (not part of a generic node).
# This is where a new node's individual elements should be defined">

"""
Properties of the generated Node
"""
BaseName = 'Canny'
NodeAttributeNames = ['Parameters', 'Frame In', 'Edges Out']
NodeAttributeType = ['Static', 'Input', 'Output']
ParameterNames = ['Visualisation', 'Min Value', 'Max Value']
ParameterTypes = ['bool', 'int', 'int']
ParametersDefaultValues = [False, 100, 200]
WorkerDefaultExecutable = os.path.join(os.path.dirname(Exec), 'canny_worker.py')

# </editor-fold>


# <editor-fold desc="The following code is called as its own process when the editor starts the graph">
if __name__ == "__main__":
    canny_com = gu.start_the_transform_communications_process(NodeAttributeType, NodeAttributeNames)
    gu.register_exit_signals(canny_com.on_kill)
    canny_com.start_ioloop()

# </editor-fold>
