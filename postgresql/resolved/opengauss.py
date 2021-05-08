# -*- coding: utf-8 -*-

import binascii
import hmac
from hashlib import md5, pbkdf2_hmac, sha256
from ..python.structlib import ulong_pack


PLAIN_PASSWORD=0
MD5_PASSWORD=1
SHA256_PASSWORD=2


def sha256_pw(user, password, salt):
	password_stored_method, salt = int(ulong_pack(salt[:4])), salt[4:]
	if password_stored_method in (PLAIN_PASSWORD, SHA256_PASSWORD):
		random64_code, salt = salt[:64].decode(), salt[64:]
		token, salt = salt[:8].decode(), salt[8:]
		server_iteration, salt = ulong_pack(salt[:4]), salt[4:]
		return rfc5802_algorithm(password, random64_code, token, "", server_iteration)
	elif password_stored_method == 1:
		# MD5
		pw = md5(password + user).hexdigest().encode('ascii')
		return b'md5' + md5(pw + salt[:4]).hexdigest().encode('ascii')
	else:
		raise Exception("pq: the password-stored method is not supported, must be plain, md5 or sha256.")


def rfc5802_algorithm(password, random64_code, token,
					 server_signature, server_iteration):
	k = generate_k_from_pbkdf2(password, random64_code, server_iteration)
	server_key = get_key_from_hmac(k, b'Sever Key')
	client_key = get_key_from_hmac(k, b'Client Key')
	stored_key = get_sha256(client_key)
	token_bytes = hex_string_to_bytes(token)
	client_signature = get_key_from_hmac(server_key, token_bytes)
	if server_signature != "" and server_signature != bytes_to_hex_string(client_signature):
		return b''
	hmac_result = get_key_from_hmac(stored_key, token_bytes)
	res = XOR_between_password(hmac_result, client_key, len(client_key))
	return res


def XOR_between_password(password1, password2, length):
	arr = bytearray()
	for i in range(length):
		arr.append(password1[i]^password2[i])
	return bytes.fromhex(arr.hex())


def get_key_from_hmac(k, key):
	h = hmac.new(k, digestmod=sha256)
	h.update(key)
	return h.digest()


def get_sha256(key):
	h = sha256()
	h.update(key)
	return h.digest()


def generate_k_from_pbkdf2(password, random64_code, iterations):
	random32_code = hex_string_to_bytes(random64_code)
	dk = pbkdf2_hmac('sha1', password, random32_code, iterations, dklen=32)
	return binascii.hexlify(dk)


def hex_string_to_bytes(s):
	return bytes.fromhex(s)


def bytes_to_hex_string(bs):
	return ''.join(['%02X' % b for b in bs])
