#!/usr/bin/env vpython3
# *-* coding: utf-8 *-*
import sys
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

from endesive.pdf import cms

# from endesive.pdf import cmsn as cms

# import logging
# logging.basicConfig(level=logging.DEBUG)


def main():
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": 0,
        "sigbutton": True,
        "sigfield": "Signature1",
        "auto_sigfield": True,
        "sigandcertify": True,
        "signaturebox": (100, 140, 370, 240),
        "signature": "José Luis Bautista Cabrera",
#        "signature_img": "firma_JL.png",
        "contact": "digital@ujed.mx",
        "location": "Durango, MX",
        "signingdate": date,
        "reason": "Firma de documento",
        "password": "dtd2021",
    }
    with open("ujed.p12", "rb") as fp:
        p12 = pkcs12.load_key_and_certificates(
            fp.read(), b"dtd2021", backends.default_backend()
        )
    fname = "oficio_firma.pdf"
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    datau = open(fname, "rb").read()
    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
    fname = fname.replace(".pdf", "-firmado.pdf")
    with open(fname, "wb") as fp:
        fp.write(datau)
        fp.write(datas)


main()