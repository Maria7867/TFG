from cryptography.fernet import Fernet
import configparser

def decrypt(filename, key_path):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # opening the key
    with open(key_path, 'rb') as filekey:
        key = filekey.read()
    f = Fernet(key)
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)
    print("encrypted", file)

def dcy_main():
    '''
    print("key path: ")
    path=input() #D:\Code\decrypt\filekey.key
    print("path of the file you want to decrypt: ")
    filename=input() #D:\Code\decrypt\filekey.key
    '''
    config = configparser.ConfigParser()
    config.read('config.ini')
    path = config['DECRYPT']['KEY_PATH']
    filename = config['DECRYPT']['FILE_PATH']
    decrypt(filename,path)

#if __name__ == '__main__':
#    main()
