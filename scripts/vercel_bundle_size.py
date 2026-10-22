"""Stvarna veličina Vercelove funkcije nakon `vercel build` (Korak 5V2).

`.vercel/output/functions/*.func` sadrži samo pokretač; ostale datoteke funkcije su navedene u `.vc-config.json`
(`filePathMap`) i čitaju se s izvornih putanja, pa `du` na izlaznoj mapi pokazuje ~1 MB. Ova skripta zbraja sve.

    python scripts/vercel_bundle_size.py [--max-mb 220]   # izlazni kod 1 ako je neka funkcija veća
"""

import argparse
import json
import os
import sys
from collections import Counter


def sizes(root: str = ".vercel/output/functions") -> dict[str, tuple[int, Counter]]:
    out = {}
    for func in sorted(os.listdir(root)):
        d = os.path.join(root, func)
        cfg = json.load(open(os.path.join(d, ".vc-config.json"), encoding="utf-8"))
        total, parts = 0, Counter()
        for dp, _, files in os.walk(d):
            for f in files:
                n = os.path.getsize(os.path.join(dp, f))
                total += n
                parts["(pokretač)"] += n
        for dst, src in (cfg.get("filePathMap") or {}).items():
            n = os.path.getsize(src) if os.path.exists(src) else 0
            total += n
            p = dst.split("/")
            parts["/".join(p[:2]) if p[0] in ("_vendor", "data", "_uv") and len(p) > 1 else p[0]] += n
        out[func] = (total, parts)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-mb", type=float, default=220.0, help="granica (Vercel builder: 225 MB)")
    ap.add_argument("--root", default=".vercel/output/functions")
    args = ap.parse_args()
    bad = 0
    for func, (total, parts) in sizes(args.root).items():
        mb = total / 2**20
        print(f"{func}: {mb:.1f} MB")
        for k, v in parts.most_common(6):
            print(f"   {v / 2**20:7.1f} MB  {k}")
        bad += mb > args.max_mb
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
