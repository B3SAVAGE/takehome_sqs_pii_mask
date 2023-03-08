from cryptography.fernet import Fernet

# generate keys function
def encrypt_val(value, keys_dict):
    return Fernet(keys_dict[value]).encrypt(str(value).encode())


def mask(df):

    # generating keys for the ip column so that duplicates will have the same key
    ip_keys = {}
    for val in df['ip'].unique():
        ip_keys[val] = Fernet.generate_key()

    # generating keys for the device_id column so that duplicates will have the same key
    device_id_keys = {}
    for val in df['device_id'].unique():
        device_id_keys[val] = Fernet.generate_key()

    # apply the encryption to each dataframe column
    df['ip'] = df['ip'].apply(lambda x: encrypt_val(x, ip_keys))
    df['device_id'] = df['device_id'].apply(lambda x: encrypt_val(x, device_id_keys))

    return df
