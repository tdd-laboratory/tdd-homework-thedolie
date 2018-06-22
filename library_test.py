import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # Forth unit test; if we have a date in a text, extract the date from the text.
    def test_extract_date(self):
      self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, '2015-07-25')

    # Fifth test; if the date is incorrect
    def test_wrong_date(self):
        self.assert_extract("2013-12-25.", library.dates_iso8601)

    def test_dates_valid(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_valid_func, '25 Jan 2017')

    def test_dates_with_timestamps(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_valid_with_timestamp)

    def test_dates_with_timesstamps_end_with_seconds(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_valid_with_timestamp_with_time, '25 Jan 2017')

    def test_dates_spaceing(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_valid_spacing, '25 Jan 2017')

    def test_matching_month(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_match_month, '25 Jan 2017')

    def test_dates_comma(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_valid_comma_seperation, '25 Jan 2017')

    def test_handle_colons(self):
      self.assert_extract('18:22:19.123', library.dates_valid_colons)

    def test_handle_time_zone(self):
      self.assert_extract('18:22:19.123', library.dates_valid_colons)


if __name__ == '__main__':
    unittest.main()
