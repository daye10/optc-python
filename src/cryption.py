import ctypes

# Load the DLL
libc = ctypes.cdll.LoadLibrary("./src/bisque/BisquseDLL.dll")

# Function type declarations
libc.CreateFromKey.argtypes = [ctypes.c_char_p]
libc.CreateFromKey.restype = ctypes.c_void_p
libc.Decrypt.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
libc.Decrypt.restype = ctypes.c_int
libc.Encrypt.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
libc.Encrypt.restype = ctypes.c_char_p
libc.ReleaseBuffer.argtypes = [ctypes.c_char_p]
libc.ReleaseInst.argtypes = [ctypes.c_void_p]
libc.DecryptNTY.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_char_p), ctypes.c_bool]
libc.DecryptNTY.restype = ctypes.c_int

def create_from_key(key):
    """
    Return a pointer to a MD159 ("inst" used in all functions below)
    """
    try:
        return libc.CreateFromKey(key.encode('utf-8'))
    except Exception as e:
        print(f"Error in create_from_key: {e}")
        return None

def decrypt(key, data_to_decrypt):
    """
    Decrypt the given data using the provided key.
    """
    try:
        decrypted = ctypes.c_char_p()
        libc.Decrypt(key, data_to_decrypt.encode('utf-8'),  ctypes.byref(decrypted))
        
        return decrypted
    except Exception as e:
        print(f"Error in decrypt: {e}")
        return None
    finally:
        if decrypted:
            release_buffer(decrypted)


def encrypt(key, data_to_encrypt):
    """
    Encrypt the given data using the provided key.
    """
    try:
        data_to_encrypt_utf8 = data_to_encrypt.encode('utf-8')
        encrypted = libc.Encrypt(key, data_to_encrypt.encode('utf-8'), len(data_to_encrypt_utf8))
        return encrypted
    except Exception as e:
        print(f"Error in encrypt: {e}")
        return None

def release_buffer(buffer):
    """
    Release the buffer given by the Decrypt or Encrypt function.
    """
    try:
        libc.ReleaseBuffer(buffer)
    except Exception as e:
        print(f"Error in release_buffer: {e}")

def release_key(key):
    """
    Release an MD159 instance when it is no longer needed.
    """
    try:
        libc.ReleaseInst(key)
    except Exception as e:
        print(f"Error in release_key: {e}")

def nty_decryptor(key, filename, extension=None):
    """
    Decrypt an NTY file and save the decrypted data.
    """
    try:
        with open(f"./{filename}", "rb") as file:
            encrypted = file.read()
        encryptedLength = len(encrypted)

        decrypted = ctypes.c_char_p(None)  # 
        decryptedLength = libc.DecryptNTY(key, encrypted, encryptedLength, ctypes.byref(decrypted), True)
        if extension == None:
            name = f"{filename}"
        else:
            name = f"{filename}{extension}"
        output_file_path = f"./{name}"
        with open(output_file_path, "wb") as output_file:
            output_file.write(ctypes.string_at(decrypted, decryptedLength))
        return name
    except Exception as e:
        print(f"Error in nty_decryptor: {e}")
        return None
    finally:
        if decrypted:
            release_buffer(decrypted)
