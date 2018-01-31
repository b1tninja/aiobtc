from unittest import TestCase
from __init__ import VarInt

class TestVarInt(TestCase):
    def test___int__(self):
        examples = [(1, b'\x01'),
                    (515, b'\xFD\x03\x02'),
                    (0x0100, b'\xFD\x00\x01'),
                    (0x01000000, b'\xFE\x00\x00\x00\x01'),
                    (0x0100000000000000, b'\xFF\x00\x00\x00\x00\x00\x00\x00\x01')]

        for n, encoding in examples:
            self.assertEqual(n, VarInt.from_bytes(encoding))
            self.assertEqual(bytes(VarInt(n)), encoding)
