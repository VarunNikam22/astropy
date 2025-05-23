# Licensed under a 3-clause BSD style license - see LICENSE.rst

import copy

import pytest

import astropy.units as u
from astropy.constants import Constant


def test_c():
    from astropy.constants import c

    # c is an exactly defined constant, so it shouldn't be changing
    assert c.value == 2.99792458e8  # default is S.I.
    assert c.si.value == 2.99792458e8
    assert c.cgs.value == 2.99792458e10

    # make sure it has the necessary attributes and they're not blank
    assert c.uncertainty == 0  # c is a *defined* quantity
    assert c.name
    assert c.reference
    assert c.unit


def test_h():
    from astropy.constants import h

    # check that the value is fairly close to what it should be (not exactly
    # checking because this might get updated in the future)
    assert abs(h.value - 6.626e-34) < 1e-38
    assert abs(h.si.value - 6.626e-34) < 1e-38
    assert abs(h.cgs.value - 6.626e-27) < 1e-31

    # make sure it has the necessary attributes and they're not blank
    assert h.uncertainty == 0  # CODATA 2018 set h to exact value
    assert h.name
    assert h.reference
    assert h.unit


def test_e():
    """Tests for #572 demonstrating how EM constants should behave."""

    from astropy.constants import e

    # A test quantity
    E = u.Quantity(100, "V/m")

    # Without specifying a system e should not combine with other quantities
    pytest.raises(TypeError, lambda: e * E)
    # Try it again (as regression test on a minor issue mentioned in #745 where
    # repeated attempts to use e in an expression resulted in UnboundLocalError
    # instead of TypeError)
    pytest.raises(TypeError, lambda: e * E)

    # e.cgs is too ambiguous and should not work at all
    pytest.raises(TypeError, lambda: e.cgs * E)

    assert isinstance(e.si, u.Quantity)
    assert isinstance(e.gauss, u.Quantity)
    assert isinstance(e.esu, u.Quantity)

    assert e.si * E == u.Quantity(100, "eV/m")
    assert e.gauss * E == u.Quantity(e.gauss.value * E.value, "Fr V/m")
    assert e.esu * E == u.Quantity(e.esu.value * E.value, "Fr V/m")


def test_g0():
    """Tests for #1263 demonstrating how g0 constant should behave."""
    from astropy.constants import g0

    # g0 is an exactly defined constant, so it shouldn't be changing
    assert g0.value == 9.80665  # default is S.I.
    assert g0.si.value == 9.80665
    assert g0.cgs.value == 9.80665e2

    # make sure it has the necessary attributes and they're not blank
    assert g0.uncertainty == 0  # g0 is a *defined* quantity
    assert g0.name
    assert g0.reference
    assert g0.unit

    # Check that its unit have the correct physical type
    assert g0.unit.physical_type == "acceleration"


def test_b_wien():
    """b_wien should give the correct peak wavelength for
    given blackbody temperature. The Sun is used in this test.

    """
    from astropy import units as u
    from astropy.constants import b_wien

    t = 5778 * u.K
    w = (b_wien / t).to(u.nm)
    assert round(w.value) == 502


def test_unit():
    from astropy import constants as const
    from astropy import units as u

    for val in vars(const).values():
        if isinstance(val, Constant):
            # Getting the unit forces the unit parser to run.  Confirm
            # that none of the constants defined in astropy have
            # invalid unit.
            assert not isinstance(val.unit, u.UnrecognizedUnit)


def test_copy():
    from astropy import constants as const

    cc = copy.deepcopy(const.c)
    assert cc == const.c

    cc = copy.copy(const.c)
    assert cc == const.c


def test_view():
    """Check that Constant and Quantity views can be taken (#3537, #3538)."""
    from astropy.constants import c

    c2 = c.view(Constant)
    assert c2 == c
    assert c2.value == c.value
    # make sure it has the necessary attributes and they're not blank
    assert c2.uncertainty == 0  # c is a *defined* quantity
    assert c2.name == c.name
    assert c2.reference == c.reference
    assert c2.unit == c.unit

    q1 = c.view(u.Quantity)
    assert q1 == c
    assert q1.value == c.value
    assert type(q1) is u.Quantity
    assert not hasattr(q1, "reference")

    q2 = u.Quantity(c)
    assert q2 == c
    assert q2.value == c.value
    assert type(q2) is u.Quantity
    assert not hasattr(q2, "reference")

    c3 = u.Quantity(c, subok=True)
    assert c3 == c
    assert c3.value == c.value
    # make sure it has the necessary attributes and they're not blank
    assert c3.uncertainty == 0  # c is a *defined* quantity
    assert c3.name == c.name
    assert c3.reference == c.reference
    assert c3.unit == c.unit

    c4 = u.Quantity(c, subok=True, copy=False)
    assert c4 is c
