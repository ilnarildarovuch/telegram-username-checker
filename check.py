from telethon import TelegramClient, sync, functions, types, errors
import configparser
import time
import os

config = configparser.ConfigParser()
config.read('config.ini')

id = config.get('default', 'api_id')
hash = config.get('default', 'api_hash')

if id == 'UPDATE ME' or hash == 'UPDATE ME':
    print("Please read the config.ini and README.md")
    input()
    exit()
else:
    id = int(id)
    client = TelegramClient("Checker", id, hash, device_model="iPhone 15 Pro", system_version="IOS 18.1") 
    client.start()

def userLookup(account):
    try:
        result = client(functions.account.CheckUsernameRequest(username=account))
        if result == True:
            print("The telegram", account, "is available")
            file = open(output(), 'a')
            file.write("%s\n" % (account))
            file.close()
            create_channel(account)
        else:
            print("The telegram", account, "is not available")
    except errors.FloodWaitError as fW:
        print("Hit the rate limit, waiting", fW.seconds, "seconds")
        time.sleep(fW.seconds)
    except errors.UsernameInvalidError as uI:
        print("Username is invalid")
    except errors.rpcbaseerrors.BadRequestError as bR:
        print("Error:", bR.message)
    except Exception as e:
        print(f"Unexpected error while checking username '{account}': {e}")

def create_channel(username):
    try:
        result = client(functions.channels.CreateChannelRequest(
            title=username,
            about=username.upper(),
            megagroup=True
        ))

        client(functions.channels.EditUsernameRequest(
            channel=result.chats[0],
            username=username
        ))

        print(f"Канал '{username}' успешно создан с username '@{username}'.")
    except errors.FloodWaitError as fW:
        print("Hit the rate limit while creating channel, waiting", fW.seconds, "seconds")
        time.sleep(fW.seconds)
    except errors.UsernameInvalidError as uI:
        print(f"Invalid username '{username}' for channel creation.")
    except errors.rpcbaseerrors.BadRequestError as bR:
        print(f"Error while creating channel '{username}': {bR.message}")
    except Exception as e:
        print(f"Unexpected error while creating channel '{username}': {e}")

def getWords():
    words = []
    delay = config.get('default', 'delay')
    path = os.path.join("word_lists", config.get('default', 'wordList'))
    if path is not None:
        file = open(path, 'r', encoding='utf-8-sig')
        words = file.read().split('\n')
        file.close()
    else:
        print("Word list not found.")

    for i in range(len(words)):
        name = words[i]
        userLookup(name)
        time.sleep(int(delay))
    print("All done")
    input("Press enter to exit...")

def output():
    return config.get('default', 'outPut', fallback="AVAILABLE.txt")

def main():
    print('''
▄▄▄█████▓▓█████  ██▓    ▓█████   ▄████  ██▀███   ▄▄▄       ███▄ ▄███▓
▓  ██▒ ▓▒▓█   ▀ ▓██▒    ▓█   ▀  ██▒ ▀█▒▓██ ▒ ██▒▒████▄    ▓██▒▀█▀ ██▒
▒ ▓██░ ▒░▒███   ▒██░    ▒███   ▒██░▄▄▄░▓██ ░▄█ ▒▒██  ▀█▄  ▓██    ▓██░
░ ▓██▓ ░ ▒▓█  ▄ ▒██░    ▒▓█  ▄ ░▓█  ██▓▒██▀▀█▄  ░██▄▄▄▄██ ▒██    ▒██ 
  ▒██▒ ░ ░▒████▒░██████▒░▒████▒░▒▓███▀▒░██▓ ▒██▒ ▓█   ▓██▒▒██▒  
  ▒██▒ ░ ░▒████▒░██████▒░▒████▒░▒▓███▀▒░██▓ ▒██▒ ▓█   ▓██▒▒██▒   ░██▒
  ▒ ░░   ░░ ▒░ ░░ ▒░▓  ░░░ ▒░ ░ ░▒   ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░ ▒░   ░  ░
    ░     ░ ░  ░░ ░ ▒  ░ ░ ░  ░  ░   ░   ░▒ ░ ▒░  ▒   ▒▒ ░░  ░      ░
  ░         ░     ░ ░      ░   ░ ░   ░   ░░   ░   ░   ▒   ░      ░   
            ░  ░    ░  ░   ░  ░      ░    ░           ░  ░       ░   
                                                                     
                        - Username Checker -
        Make sure to read the config.ini and README.md on github
    bulk checking may result in false positives and longer wait times
    ''')
    
    print("1 = Enter username manually\n2 = Read a list of usernames from the word_lists folder")
    set = ["1", "2"]
    option = input("Select your option: ")
    
    while True:
        if str(option) in set:
            if option == set[0]:
                name = input("Enter a username: ")
                userLookup(name)
            else:
                getWords()
                break
        else:
            option = input("1 or 2 ... Please!: ")

if __name__ == "__main__":
    main()
