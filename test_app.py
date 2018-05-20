import pytest
from app import index, splitAndRemoveSpecialCharacter, definitions


def test_index():
    assert index() == 'This is Synonyms Dictionary.'

def test_splitAndRemoveSpecialCharacter():
    assert splitAndRemoveSpecialCharacter("LINE") == 'LINE'
    assert splitAndRemoveSpecialCharacter("Dog cat elephant") == 'Dog'
    assert splitAndRemoveSpecialCharacter("D!@#og bird") == 'Dog'
    assert splitAndRemoveSpecialCharacter("!@#raul2 dsalw bird") == 'raul2'
    assert splitAndRemoveSpecialCharacter("!@# test dsalw bird") == ''
