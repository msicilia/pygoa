

from pygoa import GOSnapshot, GOAssocSnapshot, to_df

def test_load_snapshot_default():
    """Loads the default snapshot.
    """
    sp = GOSnapshot()
    summaries = []
    summaries.append(sp.summary)
    df = to_df(summaries)
    return True

def test_load_snapshot_available():
    """Loads an existing snapshot.
    """
    sp = GOSnapshot(date="2008-08-01")
    return True

def test_load_snapshot_not_available():
    """Attempts to load a snapshot not available.
    Should raise an exception.
    """
    try:
        sp = GOSnapshot(date="2018-02-05")
        return False
    except:
        return True

# @with_setup(setup_func, teardown_func)
def test_load_assoc_snapshot_default():
    """Loads the default snapshot and its associations.
    """
    sp = GOSnapshot()
    assoc = GOAssocSnapshot(sp)
    return True
