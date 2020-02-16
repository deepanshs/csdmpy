# -*- coding: utf-8 -*-
from csdmpy.units import ScalarQuantity


def test_unit():
    a = ScalarQuantity("1 tr").quantity
    assert str(a) == "1.0 tr"
    assert str(a.to("cycle")) == "1.0 cycle"
    # assert ScalarQuantity(a).format() == '1.0 tr'

    a = ScalarQuantity("10 cm^-1/s")
    assert str(a) == "10.0 cm^-1 * s^-1"
    assert ScalarQuantity(a).quantity == a.quantity

    a = ScalarQuantity("1 deg").quantity
    assert str(a) == "1.0 deg"
    assert str(ScalarQuantity(a)) == "1.0 °"
    assert str(ScalarQuantity("1 deg")) == "1.0 °"

    a = ScalarQuantity("(54.3/2) ppm").quantity
    assert str(a) == "27.15 ppm"
    assert str(ScalarQuantity(a)) == "27.15 ppm"

    a = ScalarQuantity("(54.3/2) (µHz/Hz)").quantity
    assert str(a) == "27.15 uHz / Hz"
    assert str(ScalarQuantity(a)) == "27.15 Hz^-1 * µHz"
    assert str(a.to("ppm")) == "27.15 ppm"

    a = ScalarQuantity("5 kg * m / s").quantity
    b = a * ScalarQuantity("1 m / s").quantity
    assert str(a) == "5.0 kg m / s"
    assert str(ScalarQuantity(a)) == "5.0 kg * m * s^-1"
    assert str(ScalarQuantity(b)) == "5.0 kg * m^2 * s^-2"
    assert ScalarQuantity(b).__format__("unit") == "kg * m^2 * s^-2"
    assert str(b.to("J")) == "5.0 J"

    a = ScalarQuantity("5e-7 s").quantity
    assert str(a) == "5e-07 s"
    assert str(ScalarQuantity(a)) == "5e-07 s"
    assert str(ScalarQuantity(a.to("us"))) == "0.5 µs"
    assert ScalarQuantity(a.to("us")).__format__("unit") == "µs"

    a = ScalarQuantity("5e-7 * 2 s").quantity
    assert str(a) == "1e-06 s"
    assert str(ScalarQuantity(a)) == "1e-06 s"
    assert str(ScalarQuantity(a.to("us"))) == "1.0 µs"
