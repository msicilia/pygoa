import wget
import gzip
import os
import glob
import tarfile

def download_assoc_database(goas):
    """This is getting MySQL dumps of assocdb from:
    ftp://ftp.geneontology.org/go/godatabase/archive/full
    It takes the format of individually dumped tables.
    """
    base_url = "ftp://ftp.geneontology.org/go/godatabase/archive/full/"
    date = goas.date
    base_filename = "go_"+ date[:-2].replace("-", "") +"-assocdb-tables"
    url = base_url + date + "/" + base_filename + ".tar.gz"
    extract = [ "association.txt", "evidence.txt"]
    # First get the database files:
    if all(os.path.exists("go_assoc_"+ date+"_"+fn) for fn in extract):
        return
    # Try to download:
    try:
        wget.download(url)
        tar = tarfile.open(base_filename+".tar.gz", "r:gz")
        for fn in extract:
            infile = tar.extractfile(base_filename+"/"+fn)
            s = infile.read()
            outfile = open("go_assoc_" + date + "_" +fn, 'wb')
            #Encoding with replace is needed, some GO files are not utf8
            outfile.write(s.decode('UTF-8', errors='replace').encode())
            outfile.close()
            os.remove(base_filename+".tar.gz")
    except:
        print("Problem downloading {}".format(url))
    pass
