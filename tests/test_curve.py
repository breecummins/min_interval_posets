from ..libposets.curve import Curve

def test():
    curve = Curve({0:-2, 1:2, 2:0, 3:1, 4:-2, 5:1, 6:-7})
    assert(curve.curve == Curve(curve.reflect()).reflect())
    assert(curve.normalize() == Curve(curve.normalize()).normalize())
    assert(curve.normalize_reflect() == Curve(curve.normalize()).reflect())
    assert(min([c for k,c in curve.normalize().items()])==-0.5)
    assert(max([c for k,c in curve.normalize().items()])==0.5)
