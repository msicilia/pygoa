
from pygoa import GOSnapshot, GOSnapshotSummary, GOAssocSnapshot, goass_to_df
from datetime import date
import sys

def main():
    gos = GOSnapshot()
    goss = GOSnapshotSummary(gos)
    goas = GOAssocSnapshot(goss)
    goass = goas.summary
    print(goass.nevidence["IEA"])
    print(goass_to_df([goass]))
    summaries = retrieve_history()
    df = goass_to_df(summaries)
    df.to_csv("summarygoas.csv")

def retrieve_history():
    """Retrieves overall countings for GO association snapshots.
    """
    summaries = []
    for year in [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]:
        for d in [date(year, m, 1) for m in range(1, 13)]:
            try:
                terms = GOSnapshot(date=d.strftime("%Y-%m-%d"))
                sp = GOAssocSnapshot(terms)
                summaries.append(sp.summary)
            except IOError:
                print("File not available for date:", d, sys.exc_info())
            except:
                print(sys.exc_info())
    return summaries

if __name__ == "__main__":
    main()
