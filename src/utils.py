import uuid

def generate_idfa():
    """
    Return Identifier for Advertiser (IDFA) for iOS account creation. (UDID)
    """
    return str(uuid.uuid4()).upper()

def generate_gaid():
    """
    Return Google Advertising ID (GAID) for Android account creation. (ADID)
    """
    return str(uuid.uuid1())

def generate_uuid():
    """
    Generates UniqueID  for account creation. (UUID)
    """
    return str(uuid.uuid4()) 
