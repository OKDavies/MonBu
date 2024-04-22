from cinemagoer import is_valid_movie

def test_is_valid_movie():
    # Test it correctly identifies a movie exists
    assert is_valid_movie("Shrek") == True
    # Test it correctly identifies no movie matches
    assert is_valid_movie("not  a movie string") == False