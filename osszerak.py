"""Nyomtass te is! lapszámok összerakása fekvő A4-es "kinyitott újság" kötetekbe.

Minden forrás-PDF füzetnyomtatásra kirakott fekvő A4 (pl. 1. lap: 4|1, 2. lap: 2|3).
Szétvágjuk A5-ös oldalakra olvasási sorrendben, majd folyamatos sorban
párokba rakjuk: üres|1, 2|3, 4|következő 1, ...
Használat: python3 osszerak.py PDF_MAPPA KIMENET.pdf ELSO UTOLSO [cím]
"""
import sys
import pymupdf

W, H = 842, 595  # fekvő A4 pontban
HALF = W / 2


def a5_oldalak(src):
    """(page_no, clip_rect) lista olvasási sorrendben."""
    pages = []
    fordított = set()
    for p in src:
        if p.rotation:
            if p.rotation == 180:
                fordított.add(p.number)
            p.remove_rotation()
        pages.append(p)
    land = [p for p in pages if p.rect.width > p.rect.height]
    if len(land) != len(pages):
        # álló oldalak: mindegyik egy-egy A5 oldal, ahogy van
        return [(p.number, p.rect) for p in pages]
    halves = []
    for p in pages:
        r = p.rect
        mid = r.x0 + r.width / 2
        bal, jobb = pymupdf.Rect(r.x0, r.y0, mid, r.y1), pymupdf.Rect(mid, r.y0, r.x1, r.y1)
        if p.number in fordított and fejjel_lefele(p, r):  # fejjel lefelé álló ív: a felek helyet cserélnek
            bal, jobb = jobb, bal
        halves.append((bal, jobb))
    n = 2 * len(pages)  # összes A5 oldal
    order = [None] * n
    # füzetkirakás: i-edik ív (2 forrásoldal): előlap [n-2i | 2i+1], hátlap [2i+2 | n-2i-1]
    for k, p in enumerate(pages):
        sheet, back = divmod(k, 2)
        L, R = halves[k]
        if not back:
            left_no, right_no = n - 2 * sheet, 2 * sheet + 1
        else:
            left_no, right_no = 2 * sheet + 2, n - 2 * sheet - 1
        order[left_no - 1] = (p.number, L)
        order[right_no - 1] = (p.number, R)
    if len(pages) % 2:  # páratlan számú lap: nem szabályos füzet, egyszerű sorrend
        order = [x for k in range(len(pages)) for x in ((k, halves[k][0]), (k, halves[k][1]))]
    return order


FORDITOTT = []


def fejjel_lefele(page, clip):
    """Igaz, ha a szöveg többsége fejjel lefelé áll ezen az oldalfélen."""
    fel = le = 0
    for b in page.get_text("dict", clip=clip)["blocks"]:
        for l in b.get("lines", []):
            k = sum(len(sp["text"]) for sp in l["spans"])
            if l["dir"][0] < -0.9:
                le += k
            elif l["dir"][0] > 0.9:
                fel += k
    return le > fel


def main(mappa, kimenet, elso, utolso, cim=None):
    out = pymupdf.open()
    stream = [None]  # bal oldal üres
    toc = []
    srcs = {}
    for n in range(elso, utolso + 1):
        path = f"{mappa}/{n:03d}.pdf"
        try:
            src = pymupdf.open(path)
        except Exception as e:
            print("HIÁNYZIK/HIBÁS:", n, e)
            continue
        srcs[n] = src
        oldalak = a5_oldalak(src)
        toc.append((n, len(stream)))
        stream += [(n, pno, clip) for pno, clip in oldalak]
    if len(stream) % 2:
        stream.append(None)
    for i in range(0, len(stream), 2):
        page = out.new_page(width=W, height=H)
        for j, item in enumerate(stream[i:i + 2]):
            if item is None:
                continue
            n, pno, clip = item
            target = pymupdf.Rect(j * HALF, 0, (j + 1) * HALF, H)
            rot = 180 if fejjel_lefele(srcs[n][pno], clip) else 0
            if rot:
                FORDITOTT.append(n)
            page.show_pdf_page(target, srcs[n], pno, clip=clip, keep_proportion=True, rotate=rot)
    out.set_toc([[1, f"Nyomtass te is! #{n}", idx // 2 + 1] for n, idx in toc])
    out.set_metadata({"title": cim or f"Nyomtass te is! {elso}–{utolso}. szám"})
    out.save(kimenet, garbage=4, deflate=True)
    print(kimenet, out.page_count, "oldal; megfordított oldalfelek:", sorted(set(FORDITOTT)), len(FORDITOTT))


if __name__ == "__main__":
    a = sys.argv
    main(a[1], a[2], int(a[3]), int(a[4]), a[5] if len(a) > 5 else None)
