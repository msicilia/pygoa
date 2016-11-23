"""
Represents the information of a GOTerm, associated to a particular
snapshot of the GO.
"""

from pronto import Term, TermList
from math import log

class GOTerm(Term):
    """A GO term, including metrics.
    The term is linked to a particular GO instance, so metrics are relative
    to that snapshot.
    """

    def __init__(self, id, onto):
        """Get the term from the ontology for the given id.
        """
        self._onto = onto
        self._term = self._onto[id]
        GOTerm._similarities = {"wang": self.similarity_wang,
                                "lin":  self.similarity_lin}


    def __getattr__(self, name):
        """Delegate to the internal term object
        """
        return getattr(self._term, name)

    @staticmethod
    def ic(term, criterion="wang"):
        """Compute information content for the term.
        The criterion parameter determines the IC approach.
        """
        # TODO: Make this generic.
        return GOTerm.wang_sv(term)

    @staticmethod
    def ancestors(term):
        """Get the ancestors of the term recursively
        """
        _ancestors = []
        if term.parents:
            _ancestors.extend(term.parents)
            for parent in term.parents:
                _ancestors.extend(GOTerm.ancestors(parent))

        _ancestors = TermList(set(_ancestors))
        return _ancestors

    @staticmethod
    def s(root, end, subdag, contribs):
        """Computes Wang's S value for a term.
        Note the implementation is inefficient as it repeats many computations.
        """
        if root == end:
            return 1.0
        else:
            chld = [t for t in root.children if t in subdag]
            # Get the relations of the children as a list of dicts.
            rels = []
            for c in chld:
                rels.extend(c.relations.items())
            rels_filtrd = [r for r in rels
                           if r[0].obo_name in contribs.keys()
                           and root in r[1]]
            # If no relationship contributes:
            if not rels_filtrd:
                return 0.0
            # Now get the relation types for each.
            reltypes =[]
            for r, t in rels_filtrd:
                reltypes.append(r.obo_name)

            svs = [GOTerm.s(c, end, subdag, contribs) for c in chld]
            return max([ contribs[val[1]] * val[0]
                        for val in zip(svs, reltypes)])

    @staticmethod
    def wang_sv(term, contribs = {"is_a":0.8, "part_of":0.6}):
        """Wang's et al (2007) semantic value (SV) for the term.
        This is a topological-only measure, not considering annotations.
        """
        # Take all the ancestors, the measure only considers them.
        term_subdag = GOTerm.ancestors(term)
        # Get the scores of each term in the subdag.
        ss = [GOTerm.s(root, term, term_subdag+[term], contribs)
                       for root in term_subdag]
        return sum(ss)

    @staticmethod
    def similarity(term, other, kind="wang"):
        """Dispatches to the funtion implementing the requested
        similairy kind.
        """
        return GOTerm._similarities[kind](term, other)

    @staticmethod
    def similarity_generic(term, other, mu, correction,
                           alpha, beta, gamma):
        """Generic Mazandu et al. (2016) formula for most of node or
        edge based similarity measures.
        """
        common = set(GOTerm.ancestors(term)).intersection(GOTerm.ancestors(other))
        d = (alpha * mu(common)
                    + beta * mu(GOTerm.ancestors(term))
                    + gamma * mu(GOTerm.ancestors(other)))

        return correction*mu(common)/d if d !=0 else float('nan')
    @staticmethod
    def similarity_lin(term, other):
        """Linn similarity
        """
        # TODO: Note now takes default IC implementation
        mu = lambda x:  max([GOTerm.ic(t) for t in x] ) if x else 0.0
        return GOTerm.similarity_generic(term, other, mu,
                                         correction=1.0,
                                         alpha = 0, beta=0.5, gamma=0.5)


    @staticmethod
    def similarity_wang(term, other, contribs={"is_a":0.8, "part_of":0.6}):
        """Compute Wang's similarity formula.
        """
        self_subdag  = GOTerm.ancestors(term)  + [term]
        other_subdag = GOTerm.ancestors(other) + [other]
        common = set(self_subdag).intersection(set(other_subdag))
        ss = [0]
        # Compute s(term) in each of the subdags
        for t in common:
            ss1 = GOTerm.s(t, term,  self_subdag, contribs)
            ss2 = GOTerm.s(t, other, other_subdag, contribs)
            ss.append(ss1+ ss2)

        d =  GOTerm.wang_sv(term, contribs) + GOTerm.wang_sv(other, contribs)
        return sum(ss) / d if d != 0 else float('nan')
