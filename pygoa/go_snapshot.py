"""
pygoa.go_snapshot
===============
This submodule contains the definition of the GOSnapshot class.
Represents a concrete snapshot of the GO.
"""

from pronto import Ontology, Relationship
import wget
import gzip
import os
import  pandas as pd

class GOSnapshot(Ontology):
     """A snapshopt of the Gene Ontology for a given day.
     """

     def __init__(self, date="2006-11-01"):
        """
        Intermmediate files are removed after usage.
        """
        self._date = date
        #TODO: Extend to other filenames.
        self.filename = "gene_ontology_edit.obo.{DATE}".format(DATE=date)

        if date is not None:
            self.get_snapshot(self.date)
        if self.downloaded:
            super(GOSnapshot, self).__init__(self.filename + ".obo")
            os.remove(self.filename + ".gz")
            os.remove(self.filename + ".obo")

     def get_snapshot(self, date):
        """Loads a concrete snapshot of the GO.
        Notes
        -----
        Currently, it gets the OBO files from the archive:
        ftp://ftp.geneontology.org/go/ontology-archive/

        Versions should be expressed as dates YYYY-MM-01 (day is always 01).
        """
        url = "ftp://ftp.geneontology.org/go/ontology-archive/"
        #TODO: Before 2016-11 file names are different.
        filename = "gene_ontology_edit.obo.{DATE}".format(DATE=date)
        url = url + filename + ".gz"
        try:
            wget.download(url)
            infile = gzip.GzipFile(filename + ".gz", 'rb')
            s = infile.read()
            infile.close()
            outfile = open(filename+ ".obo" , 'wb')
            # Encoding with replace is needed, some GO files are not utf8
            outfile.write(s.decode('UTF-8', errors='replace').encode())
            outfile.close()
            self.downloaded = True
        except:
            raise OSError('Ontology file {} could not be found'.format(filename))
            self.downloaded = False

     @property
     def summary(self):
        """Returns a GOSnapshotSummary object, containing summary info.
        """
        return GOSnapshotSummary(self)
     @property
     def date(self):
        return self._date

class GOSnapshotSummary(object):
    """A summary of statistics from a GOSnapshot.
    """
    # Properties to be dumped to pandas DataFrame:
    dfprops = ["date", "nterms", "nchildren", "nparents", "nrelations",
               "nobsolete", "nbioprocess", "nmolfunction", "ncelcomp"]

    def __init__(self, gos):
        self._date = gos.date
        self._nterms = len(gos)
        # get stats:
        self._nchildren = 0
        self._nparents = 0
        self._nrelations = 0
        self._nobsolete = 0
        # Counting for the three sub-ontologies:
        self._nbioprocess = 0
        self._nmolfunction = 0
        self._ncelcomp = 0

        for term in gos:
            self._nchildren += len(term.children)
            self._nparents += len(term.parents)
            self._nrelations +=len(term.relations)
            # "other" relation is_obsolete mark deprecations.
            if "is_obsolete" in term.other:
                self._nobsolete +=1
            if "namespace" in term.other:
                ns = term.other["namespace"]
                if ns == "biological_process":
                    self._nbioprocess +=1
                elif ns == "molecular_function":
                    self._nmolfunction +=1
                elif ns == "cellular_component":
                    self._ncelcomp +=1

    @property
    def nbioprocess(self):
        return self._nbioprocess
    @property
    def nmolfunction(self):
        return self._nmolfunction
    @property
    def ncelcomp(self):
        return self._ncelcomp


    @property
    def date(self):
        return self._date

    @property
    def nterms(self):
        return self._nterms

    @property
    def nchildren(self):
        return self._nchildren

    @property
    def nparents(self):
        return self._nparents
    @property
    def nrelations(self):
        return self._nrelations
    @property
    def nobsolete(self):
        return self._nobsolete

def to_df(summaries):
    """Transforms a list of GOSnapshotSummary objects into a pandas DataFrame.
    """
    df = pd.DataFrame()
    for p in GOSnapshotSummary.dfprops:
        df[p] = [getattr(s, p) for s in summaries]
    return df

class GOSnapshotsDelta(Ontology):
    """ Differences among two GO snapshots.
    """
    pass
