import requests
from random import choice
from time import sleep
from json import load, loads, dump
from os import system, remove
from sys import exit
from telethon.sync import TelegramClient
from telethon.errors import rpcerrorlist, SessionPasswordNeededError, PhoneNumberUnoccupiedError
from configparser import ConfigParser, NoSectionError, NoOptionError

# Country codes dictionary remains the same
countrys = {
    "Russia": "0",
    "Ukraine": "1",
    "Kazakhstan": "2",
    "China": "3",
    "Philippines": "4",
    "Myanmar": "5",
    "Indonesia": "6",
    "Malaysia": "7",
    "Vietnam": "10",
    "Kyrgyzstan": "11",
    "Usa": "12 ",
    "Israel": "13",
    "HongKong": "14",
    "Poland": "15",
    "England": "16",
    "DCongo": "18",
    "Nigeria": "19",
    "Macao": "20",
    "Egypt": "21",
    "India": "22",
    "Ireland": "23",
    "Cambodia": "24",
    "Laos": "25",
    "Haiti": "26",
    "Ivory": "27",
    "Gambia": "28",
    "Serbia": "29",
    "Yemen": "30",
    "Southafrica": "31",
    "Romania": "32",
    "Colombia": "33",
    "Estonia": "34",
    "Canada": "36",
    "Morocco": "37",
    "Ghana": "38",
    "Argentina": "39",
    "Uzbekistan": "40",
    "Cameroon": "41",
    "Chad": "42",
    "Germany": "43",
    "Lithuania": "44",
    "Croatia": "45",
    "Sweden": "46",
    "Iraq": "47",
    "Netherlands": "48",
    "Latvia": "49",
    "Austria": "50",
    "Belarus": "51",
    "Thailand": "52",
    "Saudiarabia": "53",
    "Mexico": "54",
    "Taiwan": "55",
    "Spain": "56",
    "Algeria": "58",
    "Slovenia": "59",
    "Bangladesh": "60",
    "Senegal": "61",
    "Turkey": "62",
    "Czech": "63",
    "Srilanka": "64",
    "Peru": "65",
    "Pakistan": "66",
    "Newzealand": "67",
    "Guinea": "68",
    "Mali": "69",
    "Venezuela": "70",
    "Ethiopia": "71",
    "Mongolia": "72",
    "Brazil": "73",
    "Afghanistan": "74",
    "Uganda": "75",
    "Angola": "76",
    "Cyprus": "77",
    "France": "78",
    "Papua": "79",
    "Mozambique": "80",
    "Nepal": "81",
    "Belgium": "82",
    "Bulgaria": "83",
    "Hungary": "84",
    "Moldova": "85",
    "Italy": "86",
    "Paraguay": "87",
    "Honduras": "88",
    "Tunisia": "89",
    "Nicaragua": "90",
    "Timorleste": "91",
    "Bolivia": "92",
    "Costarica": "93",
    "Guatemala": "94",
    "Uae": "95",
    "Zimbabwe": "96",
    "Puertorico": "97",
    "Togo": "99",
    "Kuwait": "100",
    "Salvador": "101",
    "Libyan": "102",
    "Jamaica": "103",
    "Trinidad": "104",
    "Ecuador": "105",
    "Swaziland": "106",
    "Oman": "107",
    "Bosnia": "108",
    "Dominican": "109",
    "Qatar": "111",
    "Panama": "112",
    "Mauritania": "114",
    "Sierraleone": "115",
    "Jordan": "116",
    "Portugal": "117",
    "Barbados": "118",
    "Burundi": "119",
    "Benin": "120",
    "Brunei": "121",
    "Bahamas": "122",
    "Botswana": "123",
    "Belize": "124",
    "Caf": "125",
    "Dominica": "126",
    "Grenada": "127",
    "Georgia": "128",
    "Greece": "129",
    "Guineabissau": "130",
    "Guyana": "131",
    "Iceland": "132",
    "Comoros": "133",
    "Saintkitts": "134",
    "Liberia": "135",
    "Lesotho": "136",
    "Malawi": "137",
    "Namibia": "138",
    "Niger": "139",
    "Rwanda": "140",
    "Slovakia": "141",
    "Suriname": "142",
    "Tajikistan": "143",
    "Monaco": "144",
    "Bahrain": "145",
    "Reunion": "146",
    "Zambia": "147",
    "Armenia": "148",
    "Somalia": "149",
    "Congo": "150",
    "Chile": "151",
    "Furkinafaso": "152",
    "Lebanon": "153",
    "Gabon": "154",
    "Albania": "155",
    "Uruguay": "156",
    "Mauritius": "157",
    "Bhutan": "158",
    "Maldives": "159",
    "Guadeloupe": "160",
    "Turkmenistan": "161",
    "Frenchguiana": "162",
    "Finland": "163",
    "Saintlucia": "164",
    "Luxembourg": "165",
    "Saintvincentgrenadines": "166",
    "Equatorialguinea": "167",
    "Djibouti": "168",
    "Antiguabarbuda": "169",
    "Caymanislands": "170",
    "Montenegro": "171",
    "Denmark": "172",
    "Switzerland": "173",
    "Norway": "174",
    "Australia": "175",
    "Eritrea": "176",
    "Southsudan": "177",
    "Saotomeandprincipe": "178",
    "Aruba": "179",
    "Montserrat": "180",
    "Anguilla": "181",
    "Japan": "182",
    "Northmacedonia": "183",
    "Seychelles": "184",
    "Newcaledonia": "185",
    "Capeverde": "186",
    "Southkorea": "190"
}

# CONFIG
try:
    config = ConfigParser()
    config.read('config.ini')

    # SIM API
    c_country = config.get('sim_api', 'country')
    c_operator = config.get('sim_api', 'operator')
    c_product = config.get('sim_api', 'product')
    c_token = config.get('sim_api', 'smshub_api_key')

    # Telegram
    c_api_id = config.get('telegram', 'api_id')
    c_api_hash = config.get('telegram', 'api_hash')

except NoSectionError as e:
    input(f'Error!! In the config file, {str(e).strip("No section: ")} partition not found')
except NoOptionError as e:
    input(f'Error!! In the config file, {str(e).strip("No option: ")} option not found')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class AccountMaker:
    def __init__(self, token, country, operator, product, api_id, api_hash):
        self.color = bcolors
        self.country = int(countrys[str(country).capitalize()])
        self.token = token
        self.operator = operator
        self.product = product
        self.api_id = api_id
        self.api_hash = api_hash
        self.url = 'https://smshub.org/stubs/handler_api.php'

    def create_account(self):
        balance = self.get_balance()
        try:
            self.counter = 60
            print(self.color.OKGREEN + f"\nBalance : {balance}\n" + self.color.ENDC)
            number = self.get_number()
            if not number:
                print(self.color.FAIL + "Failed to get a number. Retrying..." + self.color.ENDC)
                return self.create_account()
            
            print(self.color.OKCYAN + f"Number: {number['phone']}   |   Number ID: {number['id']}\n" + self.color.ENDC)
            
            try:
                client = TelegramClient(f"sessions/{number['phone']}", self.api_id, self.api_hash)
                client.connect()
                send_code = client.send_code_request(phone=number['phone'])
                self.set_status(number['id'], 1)  # Set status to WAITING_FOR_SMS
                return self.get_code(client, number, send_code)
            except rpcerrorlist.PhoneNumberBannedError:
                self.cancel_order(number, ban=True)
                return self.create_account()
            except rpcerrorlist.FloodWaitError:
                self.cancel_order(number, flood=True)
                return self.create_account()
            except rpcerrorlist.PhoneNumberInvalidError:
                self.cancel_order(number, invalid=True)
                return self.create_account()
        except KeyboardInterrupt:
            print(self.color.FAIL+"\nexiting...\n"+self.color.ENDC)
            sleep(2)
            return main()
        except IndexError:
            input("An error occurred. Please check your configuration and try again.")
            return main()

    def get_balance(self):
        params = {'api_key': self.token, 'action': 'getBalance'}
        response = requests.get(self.url, params=params)
        return float(response.text.split(':')[1])

    def get_number(self):
        params = {
            'api_key': self.token,
            'action': 'getNumber',
            'service': self.product,
            'operator': self.operator,
            'country': self.country
        }
        response = requests.get(self.url, params=params)
        if response.text.startswith('ACCESS_NUMBER'):
            _, phone_id, phone_number = response.text.split(':')
            return {'id': phone_id, 'phone': phone_number}
        return None

    def set_status(self, activation_id, status):
        params = {
            'api_key': self.token,
            'action': 'setStatus',
            'status': status,
            'id': activation_id
        }
        requests.get(self.url, params=params)

    def get_code(self, client, number, send_code):
        while self.counter > 0:
            params = {'api_key': self.token, 'action': 'getStatus', 'id': number['id']}
            response = requests.get(self.url, params=params)
            print(self.color.OKBLUE + "Code Pending....." + self.color.ENDC)
            
            if response.text.startswith('STATUS_OK'):
                code = response.text.split(':')[1]
                print(self.color.OKGREEN + f"\nCode Received: {code}\n" + self.color.ENDC)
                try:
                    client.sign_in(phone=number['phone'], code=code)
                    print(client.is_user_authorized())
                    client.disconnect()
                    self.save_number(number['phone'])
                    self.set_status(number['id'], 6)  # Set status to COMPLETED
                    self.wait()
                    return self.create_account()
                except SessionPasswordNeededError:
                    print(self.color.FAIL + "\nThis account was previously taken by someone else and the password was added, sorry you will not get your money back :(\n" + self.color.ENDC)
                    self.wait()
                    return self.create_account()
                except PhoneNumberUnoccupiedError:
                    with open("data/names.txt") as f:
                        names = str(f.read()).split("\n")
                    client.sign_up(phone_code_hash=send_code.phone_code_hash,
                                   code=code, first_name=choice(names), phone=number['phone'])
                    print(self.color.OKGREEN + f"\nAccount Created!!!\nAccount name: {client.get_me().first_name}\n" + self.color.ENDC)
                    client.disconnect()
                    self.save_number(number['phone'])
                    self.set_status(number['id'], 6)  # Set status to COMPLETED
                    self.wait()
                    return self.create_account()
                except Exception as e:
                    input(e.__class__.__name__)
            else:
                sleep(5)
                self.counter -= 5

        self.cancel_order(number)
        return self.create_account()

    def cancel_order(self, number, ban=False, flood=False, invalid=False):
        if ban:
            print(self.color.FAIL + '\n[*] Number is blocked by Telegram, Number is canceling..' + self.color.ENDC)
        elif flood:
            print(self.color.FAIL + '\n[*] Number has a waiting period, Number is canceling..' + self.color.ENDC)
        elif invalid:
            print(self.color.FAIL + '\n[*] Invalid phone number, Number is canceling..' + self.color.ENDC)
        else:
            print(self.color.FAIL + "\n[*] Couldn't get the code in the specified time, Number canceling.." + self.color.ENDC)
        
        self.set_status(number['id'], 8)  # Set status to CANCEL
        self.wait()
        try:
            remove(f"sessions/{number['phone']}.session")
        except:
            pass
        return

    def save_number(self, number):
        with open("data/phones.json", "r") as f:
            data = load(f)
        data['phone_numbers'].append(number)
        with open("data/phones.json", "w") as f:
            dump(data, f)

    def wait(self):
        print(self.color.WARNING + "\n10 seconds waiting for new account..." + self.color.ENDC)
        sleep(10)

def login_accounts():
    with open("data/phones.json", "r") as f:
        data = load(f)
    phone_data = data["phone_numbers"]
    for id, number in enumerate(phone_data):
        print(f"[{id}] {number}")
    id = input("Please enter the Number of the account you want to login :> ")
    if not id:
        print("You have not made a selection, you are being redirected to the menu!!")
        return menu()
    selected_number = phone_data[int(id)]
    print(f"Number of your choice: [{selected_number}]\n")
    print(f"Trying to login please wait..")
    client = TelegramClient("sessions/"+selected_number, c_api_id, c_api_hash)
    client.connect()
    if client.is_user_authorized():
        input("Account created please ask for code to login and press enter (only when you request code)")
        print("Code Pending...")
        while True:
            try:
                message = client.get_messages(777000, limit=1)
                code = message[0].message.split(":")[1].split(".")[0]
                print("Code received!!!!")
                print(f"Code:{code}")
                client.disconnect()
                break
            except IndexError:
                continue

def check_ban():
    list = []
    with open("data/phones.json", "r") as f:
        d = load(f)
    for i in d['phone_numbers']:
        client = TelegramClient(f"sessions/{i}.session", c_api_id, c_api_hash)
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_request(i)
            except rpcerrorlist.PhoneNumberBannedError:
                print(bcolors.FAIL+f"{i}: Banned"+bcolors.ENDC)
                client.disconnect()
                remove(f"sessions/{i}.session")
        else:
            print(bcolors.OKGREEN+f"{i}: Active"+bcolors.ENDC)
            list.append(i)
            client.disconnect()
    d['phone_numbers'] = list
    with open("data/phones.json", "w") as l:
        dump(d, l)
    input(bcolors.OKCYAN+"\nNumber List updated, banned numbers and session files deleted\n"+bcolors.ENDC)
    return main()

def banner():
    print(bcolors.WARNING+"""
[+]               Telegram Tools 
[+]            Producer Emrecan Ayas 
[+]         Translated By @Aloneintokyo
"""+bcolors.ENDC)

def menu():
    print(bcolors.OKCYAN+"""\n
*************************** MENU ******************************
*                                                             *
* [1] Account Builder               [2] Ban Check             *
* [Q|q] Exit                        [3] Login to accounts     *
*                                                             *
***************************************************************
"""+bcolors.ENDC)

def main():
    try:
        system("clear")
        banner()
        menu()
        op = input(bcolors.OKGREEN+"\nMENU :> "+bcolors.ENDC)
        if str(op) == "1":
            maker = AccountMaker(token=c_token, country=c_country, operator=c_operator,
                                 product=c_product, api_id=c_api_id, api_hash=c_api_hash)
            system("clear")
            banner()
            maker.create_account()
        elif str(op) == "2":
            check_ban()
        elif str(op) == "3":
            login_accounts()
        elif str(op).lower() == "q":
            exit()
        else:
            input("Incorrect operation")
            return main()
    except KeyboardInterrupt:
        print("\nexiting...")
        exit()

if __name__ == "__main__":
    try:
        system("clear")
        banner()
        main()
    except KeyboardInterrupt:
        print("\nexiting...")
        exit()
