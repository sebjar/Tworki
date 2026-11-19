# -*- coding: utf-8 -*-
"""Jednorazowy odbiornik na 127.0.0.1: przyjmuje jeden formularz POST z Chrome'a (adresy
okladek i filmow z Instagrama), zapisuje pole "d" do pliku i sie wylacza."""
import http.server, sys, urllib.parse

PORT, PLIK = int(sys.argv[1]), sys.argv[2]


class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        dane = urllib.parse.parse_qs(self.rfile.read(n).decode("utf-8"))
        tekst = dane.get("d", [""])[0]
        open(PLIK, "w", encoding="utf-8").write(tekst)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(("zapisano %d znakow" % len(tekst)).encode("utf-8"))
        print("zapisano", len(tekst), flush=True)
        self.server.koniec = True

    def log_message(self, *a):
        pass


srv = http.server.HTTPServer(("127.0.0.1", PORT), H)
srv.koniec = False
srv.timeout = 600
while not srv.koniec:
    srv.handle_request()
