import ctypes

libc = ctypes.cdll.LoadLibrary("./BisquseDLL.dll")

# Define argument and return types for the loaded functions to ensure correct data handling
libc.CreateFromKey.argtypes = [ctypes.c_char_p]
libc.CreateFromKey.restype = ctypes.c_void_p

libc.Decrypt.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
libc.Decrypt.restype = ctypes.c_int

libc.Encrypt.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
libc.Encrypt.restype = ctypes.c_char_p

libc.ReleaseBuffer.argtypes = [ctypes.c_char_p]
libc.ReleaseInst.argtypes = [ctypes.c_void_p]

key = libc.CreateFromKey("vuyWQSjlknpJF54ib36txVse".encode('utf-8'))
print("Key handle:", key)

# Example data to decrypt
data_to_decrypt = "IbiObF5TlhPOGuMjZI,ukyvc9ZAshH..c6HTU2UeTuPBwAQNx6hUwx4HHAcS.7PHFdDn4dYUsBdPIHLQDDpdZ3oVWjdvFnes3Xy3sp9eb7JEBgXtRgzg.yotD22sDDnF2BiRtfE1LIRWXgj8uPKs63g2XAxNenLcrIZzVcbIv2R5a3Q1N7UYwAtAkm0cKq.lgJS3RFdTQ3RkuxEIxUM3sw__"
decrypted = ctypes.c_char_p()
libc.Decrypt(key, data_to_decrypt.encode('utf-8'), ctypes.byref(decrypted))
print("\nDecrypted string:", decrypted.value.decode('utf-8'))

libc.ReleaseBuffer(decrypted)

data_to_encrypt = "Data to encrypt"
encrypted = libc.Encrypt(key, data_to_encrypt.encode('utf-8'), len(data_to_encrypt))
print("\nEncrypted string:", ctypes.string_at(encrypted).decode('utf-8'))

libc.ReleaseBuffer(encrypted)

libc.ReleaseInst(key)

# Instructions and Documentation
print("""
Instructions:
1. Ensure all function calls have proper ctypes argument and return types defined.
2. Handle resource management carefully to avoid memory leaks, using functions like ReleaseBuffer and ReleaseInst.
3. Use the provided examples to understand how to interact with the Bisque encryption library.
""")