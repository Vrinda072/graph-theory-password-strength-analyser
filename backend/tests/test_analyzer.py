# test_analyzer.py
from ..app.password_analyzer import PasswordAnalyzer

pa = PasswordAnalyzer()

def test_qwerty_low_score():
    r = pa.analyze('qwerty')
    assert r['final_score'] < 40

def test_long_varied_high_score():
    r = pa.analyze('correcthorsebatterystaple')
    assert r['final_score'] > 70

def test_mixed_chars():
    r = pa.analyze('P@ssw0rd!')
    assert 'final_score' in r
