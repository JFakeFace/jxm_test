# Copyright (c) 2021 The Regents of The University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from datetime import datetime
from typing import (
    Dict,
    List,
    Optional,
    Union,
)

from .abstract_stat import AbstractStat
from .group import Group
from .statistic import Statistic
from .timeconversion import TimeConversion


class SimStat(AbstractStat):
    """
    Contains all the statistics for a given simulation.
    """

    creation_time: Optional[datetime]
    time_conversion: Optional[TimeConversion]
    simulated_begin_time: Optional[Union[int, float]]
    simulated_end_time: Optional[Union[int, float]]

    def __init__(
        self,
        creation_time: Optional[datetime] = None,
        time_conversion: Optional[TimeConversion] = None,
        simulated_begin_time: Optional[Union[int, float]] = None,
        simulated_end_time: Optional[Union[int, float]] = None,
        **kwargs: Dict[str, Union[Group, Statistic, List[Group]]]
    ):
        self.creation_time = creation_time
        self.time_conversion = time_conversion
        self.simulated_begin_time = simulated_begin_time
        self.simulated_end_time = simulated_end_time

        for key, value in kwargs.items():
            setattr(self, key, value)
