"""
pygoa.go_assoc_snapshot
=======================
This submodule contains the definition of the GOAssocSnapshot class.
It represents a concrete snapshot of associations for a given version
of the GO.
"""


class GOAssocSnapshot(object):
     """A dataset of GO associations for a given version of the GO.
     """

     def __init__(self, go):
        """Gets the associations for the GOSnapshot passed.
        """
        print(go.date)
