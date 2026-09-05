import sys, yaml

sciezka = sys.argv[1]
tekst = open(sciezka, encoding='utf-8').read()

if not tekst.startswith('---'):
    print(f"[{sciezka}] BRAK Front Mattera - plik nie zaczyna sie od ---")
    sys.exit(1)

czesci = tekst.split('---', 2)
if len(czesci) < 3:
    print(f"[{sciezka}] BLAD - brak domykajacego ---")
    sys.exit(1)

try:
    meta = yaml.safe_load(czesci[1])
except yaml.YAMLError as e:
    print(f"[{sciezka}] BLAD YAML:\n{e}")
    sys.exit(1)

print(f"[{sciezka}] Front Matter OK:")
for k, v in meta.items():
    print(f"  {k:15} = {v!r}")
print(f"  --- dlugosc body: {len(czesci[2].strip())} znakow")
