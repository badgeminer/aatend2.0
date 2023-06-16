from pyshield import PyShield
result = PyShield.obfuscate("main.py",3)
open("obfuscated.py","w",encoding="utf8").write(result)