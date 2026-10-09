from app.utils.parsers import clean_number, clean_rate

def test_clean():
    assert clean_number('19,241') == 19241
    assert clean_rate('318,292.90') == 318292.9
