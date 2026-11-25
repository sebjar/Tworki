# -*- coding: utf-8 -*-
"""Proba: czy TikTok oddaje dane filmu (okladka, adres mp4) zwyklemu zapytaniu z Pythona."""
import http.cookiejar, json, re, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/141.0.0.0 Safari/537.36")
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
url = sys.argv[1]
req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8"})
html = op.open(req, timeout=30).read().decode("utf-8", "ignore")
m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
print("html", len(html), "json", bool(m), "cookies", [c.name for c in cj])
if m:
    d = json.loads(m.group(1))
    vd = d["__DEFAULT_SCOPE__"].get("webapp.video-detail", {})
    print("status", vd.get("statusCode"))
    it = (vd.get("itemInfo") or {}).get("itemStruct") or {}
    v = it.get("video", {})
    print("duration", v.get("duration"), "size", v.get("width"), v.get("height"))
    for k in ("cover", "originCover", "dynamicCover", "playAddr", "downloadAddr"):
        print(k, (v.get(k) or "")[:120])
    print("imagePost", bool(it.get("imagePost")))
    if v.get("playAddr"):
        r2 = urllib.request.Request(v["playAddr"], headers={"User-Agent": UA, "Referer": "https://www.tiktok.com/",
                                                            "Range": "bytes=0-1023"})
        try:
            resp = op.open(r2, timeout=30)
            print("play status", resp.status, resp.headers.get("Content-Range"), resp.headers.get("Content-Type"))
        except Exception as e:
            print("play err", e)
