from common.code_utils import CodesGenerator


def test_all_codes_unique():
    """
    Generator must create unique codes. Let's test it
    """
    codes_num = 1000000

    new_codes = CodesGenerator(codes_num).generate()
    assert len(new_codes) == len(set(new_codes))
