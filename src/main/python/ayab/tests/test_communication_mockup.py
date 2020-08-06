# -*- coding: utf-8 -*-
# This file is part of AYAB.
#
#    AYAB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AYAB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AYAB.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner,
#    Andreas Müller, Christian Gerbrandt
#    https://github.com/AllYarnsAreBeautiful/ayab-desktop

import unittest

from ayab.engine.communication import MessageToken
from ayab.engine.communication_mockup import AyabCommunicationMockup
from ayab.machine import Machine


class TestAyabCommunicationMockup(unittest.TestCase):
    def setUp(self):
        self.comm_dummy = AyabCommunicationMockup(delay=False)

    def test_close_serial(self):
        self.comm_dummy.close_serial()
        assert self.comm_dummy.is_open() is False

    def test_open_serial(self):
        assert self.comm_dummy.is_open() is False
        self.comm_dummy.open_serial()
        assert self.comm_dummy.is_open()

    def test_update_API6(self):
        assert self.comm_dummy.update_API6() == (None, MessageToken.none, 0)

    def test_req_start_API6(self):
        machine_val, start_val, end_val, continuous_reporting, crc8 = 0, 0, 10, True, 0xb9
        expected_result = (bytes([MessageToken.cnfStart.value,
                                  1]), MessageToken.cnfStart, 1)
        self.comm_dummy.req_start_API6(machine_val, start_val, end_val,
                                       continuous_reporting)
        bytes_read = self.comm_dummy.update_API6()
        assert bytes_read == expected_result

    def test_req_info(self):
        expected_result = (bytes([MessageToken.cnfInfo.value, 5, 0xff,
                                  0xff]), MessageToken.cnfInfo, 5)
        self.comm_dummy.req_info()
        bytes_read = self.comm_dummy.update_API6()
        assert bytes_read == expected_result

        # indState shall be sent automatically, also
        expected_result = (bytes(
            [MessageToken.indState.value, 1, 0xff, 0xff, 0xff, 0xff, 1,
             0x7f]), MessageToken.indState, 1)
        bytes_read = self.comm_dummy.update_API6()
        assert bytes_read == expected_result

    def test_req_test_API6(self):
        expected_result = (bytes([MessageToken.cnfTest.value,
                                  1]), MessageToken.cnfTest, 1)
        self.comm_dummy.req_test_API6(Machine.KH910_KH950)
        bytes_read = self.comm_dummy.update_API6()
        assert bytes_read == expected_result

    def test_cnf_line_API6(self):
        lineNumber = 13
        color = 0
        flags = 0x12
        lineData = [0x23, 0x24]
        crc8 = 0x24
        assert self.comm_dummy.cnf_line_API6(lineNumber, color, flags,
                                             lineData)

    def test_req_line_API6(self):
        self.comm_dummy.open_serial()
        machine_val, start_val, end_val, continuous_reporting = 0, 0, 10, True
        self.comm_dummy.req_start_API6(machine_val, start_val, end_val,
                                       continuous_reporting)
        self.comm_dummy.update_API6()  # cnfStart

        for i in range(0, 256):
            bytes_read = self.comm_dummy.update_API6()
            assert bytes_read == (bytearray([MessageToken.reqLine.value,
                                             i]), MessageToken.reqLine, i)
