

from pygoa import GOSnapshot, GOTerm
from datetime import date
import csv
import sys

def dump_ics():
    f = open("ic_dump.txt", "wt")
    writer = csv.writer(f)
    for year in [2007, 2008, 2009]:
        for d in [date(year, m, 1) for m in range(1, 13)]:
            try:
                ont = GOSnapshot(date=d.strftime("%Y-%m-%d"))
                initial = ont.term("GO:0000001")
                for t in ont:
                    writer.writerow((d.strftime("%Y-%m-%d"), t.id,
                                     GOTerm.ic(t))
                                    )
            except IOError:
                print("File not available for date:", d, sys.exc_info())
            except:
                print(sys.exc_info())
    f.close()

def main():
    dump_similarities()

def dump_similarities():
    f = open("similarities_dump.txt", "wt")
    writer = csv.writer(f)
    for year in [2007, 2008, 2009]:
        for d in [date(year, m, 1) for m in range(1, 13)]:
            try:
                ont = GOSnapshot(date=d.strftime("%Y-%m-%d"))
                initial = ont.term("GO:0000001")
                for t in ont:
                    for q in ont:
                        writer.writerow((d.strftime("%Y-%m-%d"), t.id, q.id,
                                     GOTerm.similarity_wang(t, q),
                                     GOTerm.similarity_lin(t, q))
                                    )
            except IOError:
                print("File not available for date:", d, sys.exc_info())
            except:
                print(sys.exc_info())
    f.close()

if __name__ == "__main__":
    main()
