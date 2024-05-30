import os
import requests
import json
import sqlite3
import struct
import base64
import ctypes
import src.config as config
import src.cryption as cryption

output_dir = "./"
libc = ctypes.cdll.LoadLibrary("./src/bisque/BisquseDLL.dll")
libc.CreateFromKey.argtypes = [ctypes.c_char_p]
libc.CreateFromKey.restype = ctypes.c_void_p
libc.Decrypt.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_char))]
libc.Decrypt.restype = ctypes.c_int
libc.Encrypt.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
libc.Encrypt.restype = ctypes.c_char_p
libc.ReleaseBuffer.argtypes = [ctypes.c_char_p]
libc.ReleaseInst.argtypes = [ctypes.c_void_p]

def check_resources():
    try:
        url = f"{config.get_api_url()}/resources/resource_list_path.json"
        r = config.SESSION.get(url, headers=config.SESSION.headers)
        decoded = cryption.decrypt(config.USER_INFO['session_key'], r.json()['data'])
        decoded = json.loads(decoded.value.decode('utf-8'))

        database_url = decoded['resource_list_uri']
        filename = database_url.split('/')[-1]
        version = filename.split("_")[0]

        if not os.path.isfile("./sakura.db"):
            decrypted_filename = download_resource_file(database_url, filename)  # Get the decrypted filename
            urls = extract_resource_urls(decrypted_filename)  # Pass the decrypted filename
            return urls
        else:
            return check_database_version(version)
    except Exception as e:
        print(f"Error in check_resources: {e}")
        return None


def download_resource_file(database_url, filename):
    try:
        response = requests.get(database_url)
        if response.status_code == 200:
            with open(filename, "wb") as resource:
                resource.write(response.content)
            k = cryption.create_from_key("J6oxF6iN")
            decrypted_filename = cryption.nty_decryptor(k, filename, ".json")  # Ensure this generates the correct output file
            return decrypted_filename  # Return the name of the decrypted file
        else:
            print(f"Failed to download resource file: {filename}")
    except Exception as e:
        print(f"Error in download_resource_file: {e}")


def extract_resource_urls(json_filename):
    try:
        with open(json_filename, 'r', encoding='utf-8') as input_file:
            data = json.load(input_file)
            urls = [
                f"{resource.get('url')}/{resource.get('name')}"
                for resource in data['resources']
                if resource.get('type') == "sqlite_database"
            ]
        os.remove(json_filename)  # Clean up the decrypted file after use
        return urls
    except Exception as e:
        print(f"Error in extract_resource_urls: {e}")
        return []

def check_database_version(version):
    try:
        conn = sqlite3.connect('./sakura.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Version'")
        table_exists = cursor.fetchone()
        if not table_exists:
            print("Database outdated! Updating database...")
            conn.close()
            os.remove("sakura.db")
            return check_database()
        else:
            cursor.execute("SELECT * FROM Version")
            rows = cursor.fetchall()
            for row in rows:
                if row[0] == version:
                    print("Database is up to date!")
                    return None
                else:
                    print("Updating database...")
                    conn.close()
                    os.remove("sakura.db")
                    return check_database()
    except Exception as e:
        print(f"Error in check_database_version: {e}")
        return None

def check_database():
    urls = check_resources()
    if urls is None:
        return
    for url in urls:
        download_and_decrypt_database(url)
    process_files()

def download_and_decrypt_database(url):
    try:
        filename = url.split('/')[-1]
        name = filename.split("-")[0] + ".nty"
        filepath = os.path.join(output_dir, name)
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(response.content)
            k = cryption.create_from_key("J6oxF6iN")
            cryption.nty_decryptor(k, name, None)
        else:
            print(f"Failed to download the file {name}.")
    except Exception as e:
        print(f"Error in download_and_decrypt_database: {e}")

def process_files():
    try:
        key = "JGcu2DjohFm84viZHe1Et5Qt"
        keydata = libc.CreateFromKey(key.encode('utf-8'))

        def read_header(fh):
            magic, rest_of_header = struct.unpack('<4s12s', fh.read(16))
            assert magic == b'IKMN'

        def read_map_tables(fh):
            tables_crypted, = struct.unpack('<512s', fh.read(512))
            tables_crypted_b64 = base64.b64encode(tables_crypted)
            tables = ctypes.pointer(ctypes.c_char())
            decrypted_len = libc.Decrypt(keydata, tables_crypted_b64, ctypes.byref(tables))
            assert decrypted_len == 512

            enc_map = bytearray(256)
            dec_map = bytearray(256)
            enc_map[:] = tables[  0:256]
            dec_map[:] = tables[256:512]
            libc.ReleaseBuffer(tables)
            return enc_map, dec_map

        def remap_block(the_map, original):
            mapped = bytearray(len(original))
            for i in range(len(original)):
                mapped[i] = the_map[original[i]]
            return mapped

        def dec_db(db_encrypted, db_decrypted):
            with open(db_encrypted, mode="rb") as fh_encrypted, open(db_decrypted, mode="wb") as fh_decrypted:
                read_header(fh_encrypted)
                enc_map, dec_map = read_map_tables(fh_encrypted)
                while True:
                    coded = fh_encrypted.read(8192)
                    if not coded:
                        break
                    decoded = remap_block(dec_map, coded)
                    fh_decrypted.write(decoded)

            new_file_name = generate_new_filename(db_encrypted)
            os.rename(db_decrypted, new_file_name)

        def generate_new_filename(db_encrypted):
            dir_name = os.path.dirname(db_encrypted)
            file_name = os.path.basename(db_encrypted).replace('.nty', '.db')
            new_file_name = os.path.join(dir_name, file_name)

            index = 1
            while os.path.exists(new_file_name):
                index += 1
                new_file_name = os.path.join(dir_name, f'sakura_master_db_{index:03}.db')

            return new_file_name

        files = [file for file in os.listdir('.') if file.startswith('Sakura') and file.endswith('.nty')]

        for file in files:
            db_encrypted = file
            db_decrypted = db_encrypted.replace('.nty', '.db')
            dec_db(db_encrypted, db_decrypted)
            os.remove(db_encrypted)
        
        migrate_databases()
    except Exception as e:
        print(f"Error in process_files: {e}")

def migrate_databases():
    try:
        destination_db_path = './sakura.db'
        source_db_paths = [
            './sakura_master_db_002.db', './sakura_master_db_003.db', './sakura_master_db_004.db',
            './sakura_master_db_005.db', './sakura_master_db_006.db', './sakura_master_db_007.db',
            './sakura_master_db_008.db', './sakura_master_db_009.db', './sakura_master_db_010.db',
            './sakura_master_db_011.db'
        ]

        destination_conn = sqlite3.connect(destination_db_path)
        destination_cursor = destination_conn.cursor()

        for source_db_path in source_db_paths:
            migrate_database(source_db_path, destination_cursor)

        destination_conn.commit()
        destination_conn.close()

        for delete in source_db_paths:
            os.remove(delete)

        for file in os.listdir('.'):
            if file.endswith('.nty'):
                insert_version_into_db(file)

    except Exception as e:
        print(f"Error in migrate_databases: {e}")

def migrate_database(source_db_path, destination_cursor):
    try:
        source_conn = sqlite3.connect(source_db_path)
        source_cursor = source_conn.cursor()

        source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = source_cursor.fetchall()

        for table in tables:
            table_name = table[0]

            destination_cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            source_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            create_table_query = source_cursor.fetchone()[0]
            destination_cursor.execute(create_table_query)

            source_cursor.execute(f"SELECT * FROM {table_name};")
            rows = source_cursor.fetchall()
            for row in rows:
                placeholders = ', '.join(['?'] * len(row))
                insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
                destination_cursor.execute(insert_query, row)

            source_cursor.execute(f"SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='{table_name}';")
            indexes = source_cursor.fetchall()
            for index in indexes:
                create_index_query = index[1]
                destination_cursor.execute(create_index_query)

        source_conn.close()
    except Exception as e:
        print(f"Error in migrate_database: {e}")

def insert_version_into_db(file):
    try:
        ver = ''.join(filter(str.isdigit, file))
        conn = sqlite3.connect('./sakura.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Version (Version TEXT)''')
        cursor.execute("INSERT INTO Version VALUES (?)", (ver,))
        conn.commit()
        conn.close()
        os.remove(file)
    except Exception as e:
        print(f"Error in insert_version_into_db: {e}")

if __name__ == "__main__":
    check_database()
