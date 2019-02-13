from min_interval_posets.curve import Curve

def test():
    curve = Curve({0:-2, 1:2, 2:0, 3:1, 4:-2, 5:1, 6:-7})
    assert(curve.curve == Curve(curve.reflect()).reflect())
    assert(curve.normalize() == Curve(curve.normalize()).normalize())
    assert(curve.normalize_reflect() == Curve(curve.normalize()).reflect())
    assert(min([c for k,c in curve.normalize().items()])==-0.5)
    assert(max([c for k,c in curve.normalize().items()])==0.5)
    curve = Curve({7:-2, 8:2, 9:0, 10:1, 11:-2, 12:1, 13:-7})
    tcurve = curve.trim(8.5,11)
    assert(min(tcurve.keys())==9)
    assert(max(tcurve.keys())==11)


if __name__ == "__main__":
    test()