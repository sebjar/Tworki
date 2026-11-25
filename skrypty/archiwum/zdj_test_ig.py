# -*- coding: utf-8 -*-
"""Proba: czy publiczna strona embed Instagrama oddaje okladke i adres filmu bez logowania."""
import html, re, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/141.0.0.0 Safari/537.36")
for code in sys.argv[1:]:
    u = "https://www.instagram.com/p/%s/embed/captioned/" % code
    t = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}),
                               timeout=30).read().decode("utf-8", "ignore")
    imgs = re.findall(r'class="EmbeddedMediaImage"[^>]*src="([^"]+)"', t)
    print(code, len(t), "img:", len(imgs), html.unescape(imgs[0])[:90] if imgs else None)
    print("   video_url:", t.count("video_url"), "mp4:", t.count(".mp4"), "contextJSON:", t.count("contextJSON"))
    i = t.find(".mp4")
    if i > 0:
        print("   ...", t[i - 200:i + 20].replace("\n", " "))
