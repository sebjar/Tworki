# -*- coding: utf-8 -*-
"""Diagnostyka posta ze zdjeciami na TikToku: co oddaje strona i ile trwa kazdy krok."""
import http.cookiejar, json, re, sys, time, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/141.0.0.0 Safari/537.36")
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
t0 = time.time()
link = "https://www.tiktok.com/@anaboliczny.darek/video/7678743478884404512"
html = op.open(urllib.request.Request(link, headers={"User-Agent": UA}), timeout=30).read().decode("utf-8", "ignore")
print("strona", len(html), "%.1fs" % (time.time() - t0), flush=True)
m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
print("json", bool(m), flush=True)
if m:
    z = json.loads(m.group(1))["__DEFAULT_SCOPE__"]
    print("klucze", list(z.keys()), flush=True)
    for k, v in z.items():
        if isinstance(v, dict) and "itemInfo" in v:
            print(k, "status", v.get("statusCode"), "item", bool((v.get("itemInfo") or {}).get("itemStruct")))
            it = v["itemInfo"]["itemStruct"]
            ip = it.get("imagePost") or {}
            print("obrazow", len(ip.get("images", [])), "cover", bool(ip.get("cover")))
            for i, img in enumerate(ip.get("images", [])[:12]):
                u = img["imageURL"]["urlList"][0]
                t1 = time.time()
                try:
                    b = op.open(urllib.request.Request(u, headers={"User-Agent": UA, "Referer": "https://www.tiktok.com/"}), timeout=20).read()
                    print(i, len(b), "%.1fs" % (time.time() - t1), u[:80], flush=True)
                except Exception as e:
                    print(i, "BLAD", e, u[:80], flush=True)
