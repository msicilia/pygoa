from pygoa import GOSnapshot, GOTerm


def test_get_term():
    """Attempts to get an existing and a non-existing term.
    """
    sp = GOSnapshot()
    term1 = sp.term("GO:0043231") # existing id
    try:
        term2 = sp.term("GO:0001010010101") # non-existing id
        return False
    except:
        return True
    return True


def test_similarity():
    """Computes similarity measures.
    """
    sp = GOSnapshot()
    term2 = sp.term("GO:0043231")._term # existing id
    term1 = sp.term("GO:0043229")._term # existing id
    print(GOTerm.ic(term1), GOTerm.ic(term2))
    print(GOTerm.similarity(term1, term2))
    print(GOTerm.similarity(term1, term2, kind="lin"))
    return True
