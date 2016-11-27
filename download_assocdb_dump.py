from pygoa.util import download_assoc_database
from pygoa import GOAssocSnapshot, GOSnapshot


def main():

    sp = GOSnapshot()
    assoc = GOAssocSnapshot(sp)
    download_assoc_database(assoc)

if __name__ == "__main__":
    main()
