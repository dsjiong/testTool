from gmssl import sm2, func

# 加载公钥
public_key_hex = "048c56ddc295a9feadd060d6f5850b47596e3c0360b3e6dfe24ef0def71c64c5d5341147820b98ec9f42e9560b2ffaabe315d109ac05a5f20244b41f3d66a4eb6b"
public_key = sm2.SM2PublicKey.from_hex(public_key_hex)

# 加密
plaintext = b'a!123456'
ciphertext = public_key.encrypt(plaintext)

print("加密后的结果（十六进制）:", ciphertext.hex())
