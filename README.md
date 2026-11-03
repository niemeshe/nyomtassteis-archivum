# Nyomtass te is! – archívum

A [Nyomtass te is!](https://www.nyomtassteis.hu) újság 1–456. lapszáma (2017. augusztus – 2026. április), a honlapról letöltött nyomtatható változatban.

## Tartalom

- `pdf/` – a 456 lapszám külön-külön (`001.pdf` … `456.pdf`), ahogy a honlapon szerepeltek
- `kotetek/` – három összefűzött kötet fekvő A4-es oldalpárokban, könyvszerűen lapozható sorrendben
  (az első oldalpár bal fele üres, utána folyamatosan: 2|3, 4|következő szám 1. oldala …),
  minden lapszámhoz könyvjelzővel:
  - 1. kötet: 1–152. szám
  - 2. kötet: 153–304. szám
  - 3. kötet: 305–456. szám
- `urls.txt` – a lapszámok eredeti letöltési címei
- `osszerak.py` – a köteteket összerakó program (Python, PyMuPDF):
  `python3 osszerak.py pdf kimenet.pdf ELSO UTOLSO "Cím"`

## Megjegyzések

- A 131. számnak csak a nyomdai (vágójeles), a 306.-nak csak az elforgatott változata volt fent; a program ezt visszafordítja.
- A 23. (karácsonyi) szám 8 oldalas.
- A tematikus és választási különszámok még nincsenek benne – ezek összegyűjtése későbbi feladat (4. kötet).
