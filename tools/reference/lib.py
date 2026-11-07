import re, struct
from opencc import OpenCC
PAT = re.compile(rb'[\x00-\xff][\xF8-\xff]\xff\xff')
_cc = OpenCC('s2tw')
MAP = {}
for c in range(0x4E00, 0xA000):
    ch = chr(c); r = _cc.convert(ch)
    if len(r)==1 and r!=ch: MAP[c]=ord(r)

def iter_strings(d):
    """产出 (起, 止, 原文, 结尾是否含nul)"""
    for m in PAT.finditer(d):
        off = m.start()
        if off < 4: continue
        v = struct.unpack_from("<i", d, off)[0]
        if not (-4000 <= v <= -2): continue
        cnt = -v; s = off+4; e = s + cnt*2
        if e > len(d): continue
        try: t = bytes(d[s:e]).decode('utf-16-le')
        except UnicodeDecodeError: continue
        body = t[:-1] if t.endswith('\x00') else t
        if len(body) < 4: continue
        bad = False; cjk = 0
        for ch in body:
            o = ord(ch)
            if 0x4E00 <= o <= 0x9FFF: cjk += 1
            elif not (0x20 <= o <= 0x7E or o in (0x3000,0x3001,0x3002,0xFF01,0xFF08,0xFF09,0xFF0C,0xFF1A,0xFF1F,0x2026,0x00B7,0x2022,0x300C,0x300D,0xFF5E,0x2018,0x2019,0x201C,0x201D,0x300A,0x300B,0x3010,0x3011,0x2015,0xFF0B,0xFF0F,0xFF1D)):
                bad = True; break
        if bad or cjk < 2 or cjk < len(body)*0.5: continue
        yield s, e, body, t.endswith('\x00')

def convert(d):
    changed=0; hits=0
    for s,e,body,nul in iter_strings(d):
        hits += 1
        new = ''.join(chr(MAP.get(ord(ch), ord(ch))) for ch in body)
        if new != body:
            nb = (new + ('\x00' if nul else '')).encode('utf-16-le')
            if len(nb) == e-s:
                d[s:e] = nb; changed += 1
    return hits, changed
