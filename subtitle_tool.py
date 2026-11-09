import argparse, re
from pathlib import Path
BLOCK_RE = re.compile(r"^\s*(\d+)\s*\n(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*\n(.*)$", re.S)

def to_ms(h,m,s,ms): return (((int(h)*60+int(m))*60+int(s))*1000+int(ms))
def stamp(value):
    value=max(0, int(value))
    h, rem=divmod(value,3600000); m, rem=divmod(rem,60000); s, ms=divmod(rem,1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def parse_srt(text):
    cues=[]
    for block in re.split(r"\n\s*\n", text.strip()):
        if not block.strip(): continue
        match=BLOCK_RE.match(block.strip())
        if not match: raise ValueError(f"Invalid SRT cue: {block[:60]!r}")
        g=match.groups()
        start=to_ms(*g[1:5]); end=to_ms(*g[5:9])
        if end <= start: raise ValueError(f"Cue {g[0]} has end time before/equal to start")
        cues.append({"number":int(g[0]),"start":start,"end":end,"text":g[9].strip()})
    return cues

def write_srt(cues):
    out=[]
    for i,c in enumerate(cues,1):
        if not c["text"].strip(): continue
        out += [str(i), f'{stamp(c["start"])} --> {stamp(c["end"])}', c["text"], ""]
    return "\n".join(out).rstrip()+"\n"

def shift_srt(text, milliseconds):
    cues=parse_srt(text)
    for c in cues:
        c["start"]=max(0,c["start"]+milliseconds)
        c["end"]=max(c["start"]+1,c["end"]+milliseconds)
    return write_srt(cues)

def clean_srt(text):
    cues=[c for c in parse_srt(text) if c["text"].strip()]
    return write_srt(cues)

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    for name in ("validate","clean","shift"):
        q=sub.add_parser(name); q.add_argument("input",type=Path)
        if name!="validate": q.add_argument("--output",type=Path,required=True)
        if name=="shift": q.add_argument("--milliseconds",type=int,required=True)
    a=p.parse_args(); text=a.input.read_text(encoding="utf-8-sig")
    if a.cmd=="validate":
        cues=parse_srt(text); print(f"Valid: {len(cues)} cues")
    else:
        result=clean_srt(text) if a.cmd=="clean" else shift_srt(text,a.milliseconds)
        a.output.write_text(result,encoding="utf-8"); print(f"Wrote {a.output}")
if __name__=="__main__": main()
