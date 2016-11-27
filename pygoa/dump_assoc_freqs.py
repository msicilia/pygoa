from pygoa.util import dump_assoc_frequencies, MRGOAFrecCounter
from pygoa import GOAssocSnapshot, GOSnapshot


def main():

    sp = GOSnapshot()
    assoc = GOAssocSnapshot(sp)
    dump_assoc_frequencies(assoc, "assoc_freqs.txt")
    job = MRGOAFrecCounter.run()

if __name__ == "__main__":
    main()
