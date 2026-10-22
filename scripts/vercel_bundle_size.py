"""Stvarna veličina Vercelove funkcije nakon `vercel build` (Korak 5V2).

`.vercel/output/functions/*.func` sadrži samo pokretač; ostale datoteke funkcije su navedene u `.vc-config.json`
(`filePathMap`) i čitaju se s izvornih putanja, pa `du` na izlaznoj mapi pokazuje ~1 MB. Ova skripta zbraja sve.

    python scripts/vercel_bundle_size.py [--max-mb 220] [--max-file-mb 95]

Izlazni kod 1 ako je neka funkcija veća od --max-mb ili ako je neka datoteka u njoj veća od --max-file-mb
(`vercel deploy` na Hobby planu odbija datoteke veće od 100 MB: "File size limit exceeded (100 MB)").
"""

import argparse
import json
import os
import sys
from collections import Counter


def sizes(root: str = ".vercel/output/functions") -> dict[str, tuple[int, Counter, list]]:
    """{funkcija: (ukupno bajtova, bajtovi po dijelu, [(bajtovi, putanja u paketu)] najvećih datoteka)}."""
    out = {}
    for func in sorted(os.listdir(root)):
        d = os.path.join(root, func)
        cfg = json.load(open(os.path.join(d, ".vc-config.json"), encoding="utf-8"))
        total, parts, files_by_size = 0, Counter(), []
        for dp, _, files in os.walk(d):
            for f in files:
                path = os.path.join(dp, f)
                n = os.path.getsize(path)
                total += n
                parts["(pokretač)"] += n
                files_by_size.append((n, os.path.relpath(path, d)))
        for dst, src in (cfg.get("filePathMap") or {}).items():
            n = os.path.getsize(src) if os.path.exists(src) else 0
            total += n
            p = dst.split("/")
            parts["/".join(p[:2]) if p[0] in ("_vendor", "data", "_uv") and len(p) > 1 else p[0]] += n
            files_by_size.append((n, dst))
        out[func] = (total, parts, sorted(files_by_size, reverse=True))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-mb", type=float, default=220.0, help="granica (Vercel builder: 225 MB)")
    ap.add_argument("--max-file-mb", type=float, default=95.0, help="najveća datoteka (Hobby upload: 100 MB)")
    ap.add_argument("--root", default=".vercel/output/functions")
    args = ap.parse_args()
    bad = 0
    for func, (total, parts, files) in sizes(args.root).items():
        mb = total / 2**20
        print(f"{func}: {mb:.1f} MB (najveća datoteka {files[0][0] / 2**20:.1f} MB: {files[0][1]})")
        for k, v in parts.most_common(6):
            print(f"   {v / 2**20:7.1f} MB  {k}")
        if mb > args.max_mb:
            print(f"GREŠKA: {func} ima {mb:.1f} MB, više od {args.max_mb:g} MB")
            bad += 1
        for n, path in files:
            if n / 2**20 > args.max_file_mb:
                print(f"GREŠKA: {path} ima {n / 2**20:.1f} MB, više od {args.max_file_mb:g} MB po datoteci")
                bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
