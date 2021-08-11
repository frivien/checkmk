#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from typing import Sequence, Tuple, Union

import pytest

from testlib import Check

_STRING_TABLE = [
    ["TowerA_InfeedA", "1", "1097"],
    ["TowerA_InfeedB", "1", "261"],
    ["TowerA_InfeedC", "1", "0"],
    ["TowerB_InfeedA", "1", "665"],
    ["TowerB_InfeedB", "1", "203"],
    ["TowerB_InfeedC", "1", "0"],
]


@pytest.mark.usefixtures("config_load_all_checks")
def test_inventory_sentry_pdu() -> None:
    assert list(Check("sentry_pdu").run_discovery(_STRING_TABLE)) == [
        ("TowerA_InfeedA", 1),
        ("TowerA_InfeedB", 1),
        ("TowerA_InfeedC", 1),
        ("TowerB_InfeedA", 1),
        ("TowerB_InfeedB", 1),
        ("TowerB_InfeedC", 1),
    ]


@pytest.mark.parametrize(
    "item, params, expected_result",
    [
        pytest.param(
            "TowerA_InfeedA",
            1,
            [
                (0, "Status: on"),
                (0, "Power: 1097 Watt", [("power", 1097)]),
            ],
            id="discovered params, ok",
        ),
        pytest.param(
            "TowerA_InfeedA",
            0,
            [
                (2, "Status: on"),
                (0, "Power: 1097 Watt", [("power", 1097)]),
            ],
            id="discovered params, not ok",
        ),
        # The following 2 configurations do not work correctly and will be fixed in the following
        # commits
        pytest.param(
            "TowerA_InfeedA",
            {"required_state": "on"},
            [
                (2, "Status: on"),
                (0, "Power: 1097 Watt", [("power", 1097)]),
            ],
            id="checks params, ok",
        ),
        pytest.param(
            "TowerA_InfeedA",
            {"required_state": "off"},
            [
                (2, "Status: on"),
                (0, "Power: 1097 Watt", [("power", 1097)]),
            ],
            id="checks params, not ok",
        ),
    ],
)
@pytest.mark.usefixtures("config_load_all_checks")
def test_check_sentry_pdu(
    item: str,
    params,  # we will type this parameter later
    expected_result: Sequence[Union[Tuple[int, str], Tuple[int, str, Tuple[str, int]]]],
) -> None:
    assert list(Check("sentry_pdu").run_check(
        item,
        params,
        _STRING_TABLE,
    )) == expected_result