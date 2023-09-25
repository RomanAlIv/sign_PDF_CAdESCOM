from base64 import b64encode
from typing import Union

import win32com.client as win32

from cadescom_const import CADESCOM_CONTAINER_STORE, CAPICOM_MY_STORE, CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED, \
    CADESCOM_CADES_BES, CADESCOM_BASE64_TO_BINARY, CADESCOM_HASH_ALGORITHM_CP_GOST_3411_2012_256, \
    CADESCOM_XML_SIGNATURE_TYPE_ENVELOPED, CADESCOM_XADES_BES

import pythoncom
import pywintypes
#Сразу перед инициализацией DCOM в run()



def certificate_info(cert):
    """Данные сертификата."""
    pkey = cert.PrivateKey
    algo = cert.PublicKey().Algorithm

    cert_info = {
        'privateKey': {
            'providerName': pkey.ProviderName,
            'uniqueContainerName': pkey.UniqueContainerName,
            'containerName': pkey.ContainerName,
        },
        'algorithm': {
            'name': algo.FriendlyName,
            'val': algo.Value,
        },
        'valid': {
            'from': cert.ValidFromDate,
            'to': cert.ValidToDate,
        },
        'issuer': parse_detail(cert.IssuerName),
        'subject': parse_detail(cert.SubjectName),
        'thumbprint': cert.Thumbprint,
        'serialNumber': cert.SerialNumber,
        'hasPrivateKey': cert.HasPrivateKey()
    }

    return cert_info


def parse_detail(row):
    if row:
        row1 = row.replace(', д.', ' д.').replace(', стр.', ' стр.').replace(', эт.', ' эт.').replace(', пом.',' пом.').replace(', ком.', ' ком.').replace(', ПОМЕЩ', ' ПОМЕЩ').replace(', КОМ', ' КОМ')
        detail = dict(
            key_val.split('=')
            for key_val in row1.split(',')
        )
        detail['row'] = row1
        return detail


def certificates_store():
    pythoncom.CoInitializeEx(0)
    store = win32.Dispatch("CAdESCOM.Store")
    store.Open(
        CADESCOM_CONTAINER_STORE,
        CAPICOM_MY_STORE,
        CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED
    )
    return store.Certificates


def get_signer(cert, pin):
    """Формирование подписи."""
    pythoncom.CoInitializeEx(0)
    signer = win32.Dispatch("CAdESCOM.CPSigner")
    signer.Certificate = cert
    signer.CheckCertificate = True
    signer.KeyPin = pin
    return signer


def get_signature(file, signer):
    """Подпись файла."""
    pythoncom.CoInitializeEx(0)
    signed_data = win32.Dispatch("CAdESCOM.CadesSignedData")
    signed_data.Content = b64encode(file).decode()
    return signed_data.SignCades(signer, CADESCOM_CADES_BES)

def get_signature_XML(content_XML, signer):
    """Подпись content_XML."""
    pythoncom.CoInitializeEx(0)
    signed_data = win32.Dispatch("CAdESCOM.SignedXML")
    signed_data.Content = content_XML
    signed_data.SignatureType = CADESCOM_XML_SIGNATURE_TYPE_ENVELOPED | CADESCOM_XADES_BES
    return signed_data.Sign(signer)

def get_unsigned(signature: bytes) -> str:
    """Разподписать файл."""
    pythoncom.CoInitializeEx(0)
    unsigned_data = win32.Dispatch("CAdESCOM.CadesSignedData")
    signature = b64encode(signature).decode()
    unsigned_data.VerifyCades(signature, CADESCOM_CADES_BES)
    return unsigned_data.Content


def gost_hash(data: Union[str, bytes, bytearray], encoding="utf-8") -> str:
    """Подписать хеш."""
    if isinstance(data, str):
        data = bytes(data.encode(encoding))

    pythoncom.CoInitializeEx(0)
    hashed_data = win32.Dispatch("CAdESCOM.HashedData")
    hashed_data.DataEncoding = CADESCOM_BASE64_TO_BINARY
    hashed_data.Algorithm = (
        CADESCOM_HASH_ALGORITHM_CP_GOST_3411_2012_256
    )
    hashed_data.Hash(b64encode(data).decode())
    byte_hash = bytes.fromhex(hashed_data.Value)
    return b64encode(byte_hash).decode()
