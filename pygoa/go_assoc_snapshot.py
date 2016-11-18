"""
pygoa.go_assoc_snapshot
=======================
This submodule contains the definition of the GOAssocSnapshot class.
It represents a concrete snapshot of associations for a given version
of the GO.
"""
import wget
import gzip
import os
import pandas as pd


class GOAssocSnapshot(object):
    """A dataset of GO associations for a given version of the GO.
     """

    def __init__(self, go):
        """Gets the associations for the GOSnapshot (or GOSnapshotSummary) passed.
           Uses the summaries found in the GO database dump archive.
        """
        self.date = go.date
        self.downloaded = False
        self.filename = "go_{YYYY}{MM}-assocdb-summary.txt".format(YYYY=self.date[0:4],
                                                                   MM=self.date[5:7])

        if go.date is not None:
            self.get_snapshot(self.date)
        if self.downloaded:
            self.load_summary()
            os.remove(self.filename + ".gz")
            os.remove(self.filename)

    def load_summary(self):
        self.rawdata = [line.strip() for line in open(self.filename, "r")]

    def get_snapshot(self, date):
        """ Attempts to get the summary file from the GO database archive.
        """
        url = "ftp://ftp.geneontology.org/go/godatabase/archive/full/"
        url = url + self.date + "/" + self.filename + ".gz"
        try:
            wget.download(url)
            infile = gzip.GzipFile(self.filename + ".gz", 'rb')
            s = infile.read()
            infile.close()
            outfile = open(self.filename, 'wb')
            # Encoding with replace is needed, some GO files are not utf8
            outfile.write(s.decode('UTF-8', errors='replace').encode())
            outfile.close()
            self.downloaded = True
        except:
            self.downloaded = False
            raise OSError('Summary file {} could not be found'.format(self.filename))
        pass

    @property
    def summary(self):
        """Returns a GOSnapshotSummary object, containing summary info.
         """
        return GOAssocSnapshotSummary(self)


class GOAssocSnapshotSummary(object):
    """A summary of the dataset of GO associations for a given version of the GO.
     """

    def __init__(self, goas):
        self.date = goas.date
        self.process_data(goas.rawdata)

    def process_data(self, rawdata):
        """Data conversion into attributes.
         """
        self._nevidence = {}
        for line in rawdata:
            if line.startswith("Associations type"):
                attr, number = line.split(":")
                number = number[:-1]  # Remove trailing carriage return
                evidence_code = attr.split(" ")[-1]
                self._nevidence[evidence_code] = number
            else:
                pass

    @property
    def nevidence(self):
        return self._nevidence


def goass_to_df(summaries):
    """Transforms a list of GOAssocSnapshotSummary objects into a pandas DataFrame.
    """
    df = pd.DataFrame()
    df["date"] = [s.date for s in summaries]
    for k in summaries[0].nevidence:
        df["nevidence" + k] = [s.nevidence[k] for s in summaries]
    return df
