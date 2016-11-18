from pygoa import GOSnapshot, GOTerm


def test_get_term():
    """Loads the default snapshot.
       Attempts to get an existing and a non-existing term.
    """
    sp = GOSnapshot()
    term1 = sp["GO:0001591"]

    try:
        term2 = sp["GO:0001010010101"] # non-existing id
        return False
    except:
        return True
    return True
