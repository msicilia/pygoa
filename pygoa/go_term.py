"""
Represents the information of a GOTerm, associated to a particular
snapshot of the GO.
"""

from pronto import Term

class GOTerm(Term):
    """A GO term, including metrics.
    """
    def __init__(self, id, onto):
        """Get the term from the ontology for the given id.
        """
        self._onto = onto
        self._term = self._onto[id]


    def ic(self):
        """Information content.
        """
        pass
