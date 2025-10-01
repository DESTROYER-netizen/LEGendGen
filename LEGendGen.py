#!/usr/bin/env python3
# 12.py
# LEGENDGEN Termux-ready Nodeps
# Animated ANSI banner + One-shot wordlist generator
# Works with plain python3 (no pip installs)

import sys, time, os, random, shutil
from itertools import product, chain
from typing import List, Iterable

# ------------------------
# Config / Defaults
# ------------------------
TARGET_COUNT = 1_000_000
OUTPUT_FILE = "targeted_wordlist.txt"

DEFAULTS = {
    "separators": ["", ".", "_", "-", "@", "#", "~", "/", "|", ":"],
    "special_chars": ["!", "@", "#", "$", "%", "^", "&", "*"],
    "special_repeat_max": 3,
    "include_special_only": True,
    "include_numeric_only": True,
    "leet_subs": True,
    "min_length": 4,
    "max_length": 12,
}

FIELDS = [
    ("Name", "NAME"),
    ("Nickname", "NICKNAME"),
    ("Username", "USERNAME"),
    ("Dob (e.g. 11122096)", "DOB"),
    ("Year(s) comma-separated (e.g. 1996,96)", "YEARS"),
    ("Phone (fragment)", "PHONE"),
    ("Lover", "LOVER"),
    ("Ex", "EX"),
    ("Spouse", "SPOUSE"),
    ("Mom", "MOM"),
    ("Dad", "DAD"),
    ("Sister", "SISTER"),
    ("Brother", "BROTHER"),
    ("Pet name", "PET"),
    ("Hobby", "HOBBY"),
    ("Favorite team", "FAVORITE_TEAM"),
    ("Favorite brand", "FAVORITE_BRAND"),
]

# ------------------------
# Banner
# ------------------------
BANNER_LINES = [
"================================================================================",
"=                                                                              =",
"=   _      ______  ______  ______  _____   ____   _____   _____  ______  _____  =",
"=  | |    |  ____||  ____||  ____||  __ \\ / __ \\ / ____| / ____||  ____||  __ \\ =",
"=  | |    | |__   | |__   | |__   | |__) | |  | || |  __ | |  __ | |__   | |__) |",
"=  | |    |  __|  |  __|  |  __|  |  _  /| |  | || | |_ || | |_ ||  __|  |  _  / ",
"=  | |____| |____ | |____ | |____ | | \\ \\| |__| || |__| || |__| || |____ | | \\ \\ ",
"=  |______|______||______||______||_|  \\_\\\\____/  \\_____| \\_____| |______||_|  \\_\\",
"=                                                                              =",
"=                      WORDLIST GEN - Powerful & Fast                          =",
"=                          Education purposes only                            =",
"=                               TG - @Legend11587                             =",
"================================================================================",
]

ANSI_RESET = "\033[0m"
ANSI_CLEAR = "\033[2J\033[H"

COLOR_POOL = [22, 28, 34, 40, 46, 47, 82, 83, 118, 154, 190, 191]

def ansi_fg_256(code: int, bold: bool=False, dim: bool=False) -> str:
    seq = f"\033[38;5;{code}m"
    if bold: seq = "\033[1m" + seq
    if dim: seq = "\033[2m" + seq
    return seq

def center_line_for_cols(line: str, cols: int) -> str:
    if len(line) < cols:
        pad = (cols - len(line)) // 2
        return " " * pad + line
    return line

def animate_banner(frames: int=14, sleep: float=0.08, flicker_prob: float=0.20):
    """Animated banner (no duplicates, handles terminal width)"""
    try:
        cols = shutil.get_terminal_size((80, 24)).columns
    except:
        cols = 80

    max_line_len = max(len(l) for l in BANNER_LINES)
    need_truncate = cols < max_line_len

    sys.stdout.write(ANSI_CLEAR)
    sys.stdout.flush()
    base_color = random.choice(COLOR_POOL)

    for f in range(frames):
        buf_lines = []
        frame_color = (base_color + (f % 6)) % 256
        bold_frame = (f % 4 == 0)
        for i, line in enumerate(BANNER_LINES):
            if need_truncate and len(line) > cols:
                keep = max(0, (cols - 4)//2)
                left = line[:keep]
                right = line[-keep:] if keep>0 else ""
                disp = left + ".." + right
            else:
                pad = (cols - len(line)) //2 if len(line)<cols else 0
                disp = (" "*pad)+line
            flick = (random.random() < flicker_prob)
            dim = flick and (random.random()<0.6)
            if 2<=i<=6:
                buf_lines.append(ansi_fg_256(frame_color,bold=bold_frame,dim=dim)+disp+ANSI_RESET)
            else:
                buf_lines.append(ansi_fg_256(22)+disp+ANSI_RESET)
        sys.stdout.write("\033[H")
        sys.stdout.write("\n".join(buf_lines))
        sys.stdout.flush()
        time.sleep(sleep)

    # Final stable banner
    final_color = random.choice(COLOR_POOL)
    final_lines=[]
    for i, line in enumerate(BANNER_LINES):
        if need_truncate and len(line) > cols:
            keep = max(0,(cols-4)//2)
            left=line[:keep]
            right=line[-keep:] if keep>0 else ""
            disp=left+".."+right
        else:
            pad=(cols-len(line))//2 if len(line)<cols else 0
            disp=(" "*pad)+line
        if 2<=i<=6:
            final_lines.append(ansi_fg_256(final_color,bold=True)+disp+ANSI_RESET)
        else:
            final_lines.append(ansi_fg_256(22)+disp+ANSI_RESET)
    sys.stdout.write("\033[H")
    sys.stdout.write("\n".join(final_lines)+"\n")
    sys.stdout.flush()

# ------------------------
# Wordlist logic (same as original)
# ------------------------
LEET_MAP = str.maketrans({
    "a":"@","A":"@","s":"$","S":"$","i":"1","I":"1","o":"0","O":"0","e":"3","E":"3","t":"7","T":"7"
})

def reverse_str(s): return s[::-1]
def apply_leet(word): return word.translate(LEET_MAP)
def case_variants(word): return list({word.lower(),word.title(),word.upper()})
def short_case_permutations(word):
    if len(word)==0 or len(word)>4: return []
    letters=[(c.lower(),c.upper()) if c.isalpha() else (c,) for c in word]
    return [''.join(p) for p in product(*letters)]

def generate_numeric_pools():
    nums1=[str(i) for i in range(100)]
    nums2=[f"{i:02d}" for i in range(100)]
    nums3=[f"{i:03d}" for i in range(1000)]
    seen=set()
    out=[]
    for n in chain(nums1,nums2,nums3):
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out

def generate_special_sequences(specials,repeat_max):
    seqs=[]
    for r in range(1,repeat_max+1):
        for c in specials:
            seqs.append(c*r)
    return seqs

def collect_tokens_one_shot(responses,defaults):
    tokens=[]
    order=["NAME","NICKNAME","USERNAME","DOB","YEARS","PHONE",
           "LOVER","EX","SPOUSE","MOM","DAD","SISTER","BROTHER",
           "PET","HOBBY","FAVORITE_TEAM","FAVORITE_BRAND"]
    for key in order:
        v=responses.get(key,"") or ""
        if not v: continue
        if key=="YEARS" and "," in v:
            parts=[p.strip() for p in v.split(",") if p.strip()]
            for p in parts:
                tokens.append(p)
                rev=reverse_str(p)
                if rev!=p: tokens.append(rev)
            continue
        if key=="DOB":
            tokens.append(v)
            digits="".join(ch for ch in v if ch.isdigit())
            if digits and digits!=v: tokens.append(digits)
        else:
            tokens.append(v)
        rev=reverse_str(v)
        if rev!=v: tokens.append(rev)
    expanded=[]
    for t in tokens:
        if not t: continue
        expanded.append(t)
        expanded.extend(case_variants(t))
        expanded.extend(short_case_permutations(t))
        lt=apply_leet(t)
        if lt!=t: expanded.append(lt)
        for v in case_variants(t):
            l2=apply_leet(v)
            if l2!=v: expanded.append(l2)
    seen=set()
    out=[]
    for x in expanded:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out

def candidate_generator(tokens,suffixes,defaults):
    specials=defaults["special_chars"]
    special_seqs=generate_special_sequences(specials,defaults["special_repeat_max"])
    numeric_pool=generate_numeric_pools()
    separators=defaults["separators"]
    minlen=defaults["min_length"]
    maxlen=defaults["max_length"]

    if defaults["include_special_only"]:
        for s in special_seqs:
            if minlen<=len(s)<=maxlen: yield s

    if defaults["include_numeric_only"]:
        for n in numeric_pool:
            if minlen<=len(n)<=maxlen: yield n

    for base in tokens:
        if minlen<=len(base)<=maxlen: yield base
        for sep in separators:
            for suf in ([""]+suffixes):
                combo=f"{base}{sep}{suf}" if suf else base
                if minlen<=len(combo)<=maxlen: yield combo
                for pre in ([""]+suffixes):
                    combo2=f"{pre}{sep}{base}" if pre else base
                    if minlen<=len(combo2)<=maxlen: yield combo2
                for sc in special_seqs:
                    combo3=combo+sc
                    if minlen<=len(combo3)<=maxlen: yield combo3
        for sc in special_seqs:
            combo=base+sc
            if minlen<=len(combo)<=maxlen: yield combo
        for n in numeric_pool:
            combo=base+n
            if minlen<=len(combo)<=maxlen: yield combo

def write_wordlist_all(tokens,suffixes,defaults,target=TARGET_COUNT,out_file=OUTPUT_FILE):
    gen=candidate_generator(tokens,suffixes,defaults)
    seen=set()
    written=0
    start=time.time()
    try:
        with open(out_file,"w",encoding="utf-8") as f:
            for s in gen:
                if s in seen: continue
                seen.add(s)
                f.write(s+"\n")
                written+=1
                if written%100000==0 and written>0:
                    sys.stderr.write(f"[{written:,}] entries written...\n")
                if written>=target: break
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Partial file written.")
    end=time.time()
    elapsed=end-start
    try:
        size_bytes=os.path.getsize(out_file)
        size_mb=size_bytes/1_000_000.0
        size_mib=size_bytes/1024.0/1024.0
    except:
        size_bytes=size_mb=size_mib=None

    print("\n=== Completed ===")
    print(f"Unique entries written: {written:,}")
    print(f"Target requested       : {target:,}")
    print(f"Time taken (sec)      : {elapsed:.2f}")
    if size_bytes is not None:
        print(f"Output file            : {out_file} ({size_bytes:,} bytes — {size_mb:.2f} MB ≈ {size_mib:.2f} MiB)")
    else:
        print(f"Output file            : {out_file} (size unknown)")
    approx_mem_mb=(len(seen)*300)/(1024.0*1024.0) if seen else 0
    print(f"Approx RAM used for dedupe set: ~{approx_mem_mb:.0f} MB (rough estimate)")
    print("=================\n")

# ------------------------
# CLI + main
# ------------------------
def input_single(prompt_label: str) -> str:
    try:
        return input(f"{prompt_label} - ").strip()
    except EOFError:
        return ""

def main():
    # animate banner (or static if terminal can't handle)
    try:
        animate_banner()
    except Exception:
        print("\n".join(BANNER_LINES))
    print("\n=== ONE-SHOT DETAILS ENTRY (press Enter to skip a field) ===")
    responses={}
    for label,key in FIELDS:
        val=input_single(label)
        responses[key]=val

    tokens=collect_tokens_one_shot(responses,DEFAULTS)
    suffixes=[]
    years_raw=responses.get("YEARS","") or ""
    if years_raw:
        suffixes.extend([p.strip() for p in years_raw.split(",") if p.strip()])
    phone_raw=responses.get("PHONE","") or ""
    if phone_raw:
        suffixes.append(phone_raw.strip())
    suffixes.extend(generate_numeric_pools())

    if not tokens and not suffixes:
        print("[error] No tokens provided. Exiting.")
        return

    print("[info] Starting generation automatically (no more prompts).")
    print("[warning] This will generate many variants and may use significant memory for dedupe set.")
    write_wordlist_all(tokens,suffixes,DEFAULTS,target=TARGET_COUNT,out_file=OUTPUT_FILE)

if __name__ == "__main__":
    main()
