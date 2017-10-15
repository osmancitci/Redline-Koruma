# -*- coding: utf-8 -*-
class LineCallback(object):

    def __init__(self, callback):
        self.callback = callback

    def Pinverified(self, pin):
        self.callback("Pin Kodu : '" + pin + "' Kodunuzu Telefonuna Giriniz")

    def QrUrl(self, url):
        self.callback("Lütfen 2 Dakika İçinde Qr Kodu İle Giriş Yapınız.\n" + url)

    def default(self, str):
        self.callback(str)
