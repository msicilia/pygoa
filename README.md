# pygoa

A Python library to get and analyze different versions of the Gene Ontology.  See the [documentation](https://github.com/msicilia/pygoa/blob/master/docs/source/index.rst) for more information.

## Install

A fist development version is yet available via PiyPI.

```
pip install pygoa
```

## Basic usage
Loads snapshots of the GO (terminology and/or annotation databases) for given dates (currently it gets the monthly snapshots made available via FTP).

```python
from pygoa import GOSnapshot
sp = GOSnapshot()        # Loads november 2006 snapshot (the default).
print(sp.summary.nterms) # Prints the number of terms for the snapshot.

```
## License
MIT, [see for more info](https://en.wikipedia.org/wiki/MIT_License).
