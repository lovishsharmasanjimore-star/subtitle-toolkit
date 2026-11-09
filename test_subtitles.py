import unittest
from subtitle_tool import parse_srt, shift_srt
SRT="1\n00:00:01,000 --> 00:00:02,000\nHello\n"
class SubtitleTests(unittest.TestCase):
 def test_parse(self): self.assertEqual(len(parse_srt(SRT)),1)
 def test_shift(self): self.assertIn("00:00:02,000",shift_srt(SRT,1000))
 def test_invalid(self):
  with self.assertRaises(ValueError): parse_srt("bad")
if __name__=="__main__": unittest.main()
