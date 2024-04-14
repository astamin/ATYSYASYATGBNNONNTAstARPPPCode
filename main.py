import os,json,shutil,requests
from requests import get, post
import re,string,hashlib,random,time
import requests
from telebot import TeleBot,types
from time import sleep
from random import choice
from json import load,dump
from time import sleep
from datetime import datetime
from threading import Lock, Thread
from uuid import uuid4
with open("AdminSettings.json","r") as reader:
    settings = load(reader)
BotToken = settings["BotToken"]
ADMINID = settings["AdminId"]
MonitorSession = ""
Spam = False
Self = False
Hate = False
Violence = False
Nudity = False
Bullying = False
Drugs = False
Cooldown = 10
url = "https://www.instagram.com/api/v1/web/reports/get_frx_prompt/"
try:
    bot = TeleBot(token=BotToken , exception_handler=None)
except:
    pass

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Successfully deleted folder: {folder_path}")
    except Exception as e:
        print(f"Error deleting folder: {e}")
def RandomStringUpper(n = 10):
    letters = string.ascii_uppercase + '1234567890'
    return ''.join(random.choice(letters) for i in range(n))
def RandomString(n=10):
    letters = string.ascii_lowercase + '1234567890'
    return ''.join(random.choice(letters) for i in range(n))
def RandomStringChars(n=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(n))
def randomStringWithChar(stringLength=10):
    letters = string.ascii_lowercase + '1234567890'
    result = ''.join(random.choice(letters) for i in range(stringLength - 1))
    return RandomStringChars(1) + result
def generate_DeviceId(ID):
        volatile_ID = "12345"
        m = hashlib.md5()
        m.update(ID.encode('utf-8') + volatile_ID.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]
def generateUSER_AGENT():
            Devices_menu = ['HUAWEI', 'Xiaomi', 'samsung', 'OnePlus']
            DPIs = [
                '480', '320', '640', '515', '120', '160', '240', '800'
            ]
            randResolution = random.randrange(2, 9) * 180
            lowerResolution = randResolution - 180
            DEVICE_SETTINTS = {
                'system': "Android",
                'Host': "Instagram",
                'manufacturer': f'{random.choice(Devices_menu)}',
                'model': f'{random.choice(Devices_menu)}-{randomStringWithChar(4).upper()}',
                'android_version': random.randint(18, 25),
                'android_release': f'{random.randint(1, 7)}.{random.randint(0, 7)}',
                "cpu": f"{RandomStringChars(2)}{random.randrange(1000, 9999)}",
                'resolution': f'{randResolution}x{lowerResolution}',
                'randomL': f"{RandomString(6)}",
                'dpi': f"{random.choice(DPIs)}"
            }
            return '{Host} 155.0.0.37.107 {system} ({android_version}/{android_release}; {dpi}dpi; {resolution}; {manufacturer}; {model}; {cpu}; {randomL}; en_US)'.format(
                **DEVICE_SETTINTS)

def headers_login():
        headers = {}
        headers['User-Agent'] = generateUSER_AGENT()
        headers['Host'] = 'i.instagram.com'
        headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        headers['accept-encoding'] = 'gzip, deflate'
        headers['x-fb-http-engine'] = 'Liger'
        headers['Connection'] = 'close'
        return headers
## Start Vanish
USER_AGENT = generateUSER_AGENT()
def Monitor():
    while 1:
        try:
            sleep(10)
            users_file = open("MonitorList.txt","r").read().splitlines()
            for acc in users_file:
                username = acc.split(":")[0]
                Chatid = acc.split(":")[1]
                headers = {
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Cookie": "massing",
                    "Dpr": "0.9",
                    "Origin": "https://www.instagram.com",
                    "Referer": "https://www.instagram.com/{}/".format(username),
                    "Sec-Ch-Prefers-Color-Scheme": "light",
                    "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Model": """""",
                    "Sec-Ch-Ua-Platform": """Windows""",
                    "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Viewport-Width": "238",
                    "X-Asbd-Id": "129477",
                    "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                    "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                    "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                    "X-Ig-App-Id": "936619743392459"}
                data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{username}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                if response.text.__contains__("id"):
                    False
                else:
                    bot.send_message(int(Chatid),f"<b> Banned : @{username}</b>",parse_mode="HTML")
                    users_file.remove(f"{username}:{Chatid}")
                    lines = open(f"./Monitor/{username}.txt",'r').read().splitlines()
                    os.remove(f"./Monitor/{username}.txt")
                    timestamp_match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', lines[1])
                    if timestamp_match:
                        previous_time_str = timestamp_match.group()
                    else:
                        print("Error extracting timestamp from the file.")
                        return

                    try:
                        previous_time = datetime.strptime(previous_time_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError as e:
                        print(f"Error: {e}")
                        previous_time = datetime.now() - datetime.timedelta(days=1)
                    time_difference = datetime.now() - previous_time
                    time_elapsed = f"{time_difference.total_seconds() / 60:.2f}"
                    open("banned.txt","a").write(f"{username}\n")
                    open("MonitorList.txt","w").write("")
                    name = open(f"./Subscribers/{Chatid}/name.txt","r").read().splitlines()[0]
                    webhook = open(f"./Subscribers/{Chatid}/webhook.txt","r").read().splitlines()[0]
                    for ll in users_file:
                        open("MonitorList.txt",'a').write(f"{ll}\n")
                    headers = {
                            'authority': 'discord.com',
                            'accept': 'application/json',
                            'accept-language': 'en',
                            'cache-control': 'no-cache',
                            'content-type': 'application/json',
                            'origin': 'https://discohook.org',
                            'pragma': 'no-cache',
                            'referer': 'https://discohook.org/',
                            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'cross-site',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

                    params = {
                        'wait': 'true',
                    }

                    json_data = {
                        "content": None,
                        "embeds": [
                            {
                            "title": "Success!",
                            "description": f"Banned @{username} ! ❌",
                            "color": 16724736,
                            "fields": [
                                {
                                "name": "Banned in:",
                                "value": f"{time_elapsed}m"
                                }
                            ],
                            "thumbnail": {
                                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/600px-Instagram_icon.png"
                            },
                            "footer": {
                                    "text": f"By : @{name}"
                                }
                            }
                        ],
                        "attachments": []
                        }
                    try:
                        response = requests.post(
                                webhook,
                                params=params,
                                headers=headers,
                                json=json_data,
                            )
                    except:
                        False
        except Exception as gg:
            print(gg)
Thread(None,Monitor).start()
print("> Bot is Online Now !")
def IsMsg(message):
    return True
@bot.message_handler(func=IsMsg)
def starting(message):
        global AdminId,MessageNow,ChatIDNow,editme
        MessageNow = str(message.text)
        ChatIDNow = str(message.chat.id)
        userids = open("Subscribers.txt","r").read().splitlines()
        if userids.__contains__(str(message.chat.id)) or str(message.chat.id) == str(ADMINID):
            user_id = str(message.from_user.id)
            user_directory = f"./Subscribers/{user_id}"
            end_time_file = os.path.join(user_directory, "end.txt")
            if message.text == "/start" or message.text == "Back":
                replymarkup = types.ReplyKeyboardMarkup(True,one_time_keyboard=False)
                banned = types.KeyboardButton("Asv Bans")
                imp = types.KeyboardButton("Imp Bot")
                about = types.KeyboardButton("About")
                replymarkup.row(banned)
                if str(message.chat.id) == str(ADMINID):
                    Controlpanel = types.KeyboardButton("Control Panel")
                    replymarkup.row(Controlpanel)
                replymarkup.row(about)
                m = "<b>Hey , Choice Option ?</b>"
                bot.send_message(message.chat.id,m,reply_markup=replymarkup,parse_mode="HTML")
            elif message.text == "Asv Bans":
                bannedreply = types.ReplyKeyboardMarkup(True,one_time_keyboard=False)
                start = types.KeyboardButton("Run")
                stop = types.KeyboardButton("Stop")
                webhook = types.KeyboardButton("Webhook")
                name = types.KeyboardButton("Name")
                Back = types.KeyboardButton("Back")
                bannedreply.row(start,stop)
                bannedreply.row(webhook,name)
                bannedreply.row(Back)
                bot.send_message(message.chat.id,"<b>Choice Option ?</b>",reply_markup=bannedreply,parse_mode="HTML")
            elif message.text == "Name":
                bot.send_message(message.chat.id, "<b>Give Me Your Nickname ?</b>",parse_mode="HTML")
                bot.register_next_step_handler_by_chat_id(message.chat.id, SaveName)
            elif message.text == "Webhook":
                bot.send_message(message.chat.id,"<b>Give Me Your Webhook ?</b>",parse_mode="HTML")
                bot.register_next_step_handler_by_chat_id(message.chat.id,SaveWebhook)
            elif message.text == "About":
                bot.send_message(message.chat.id,"<b>Leader : AsV\nProgrammer : Trajector\n\nThank You!</b>",parse_mode="HTML")
                ban = types.ReplyKeyboardMarkup(True,one_time_keyboard=False)
                start = types.KeyboardButton("Give Me My Bans")
                Back = types.KeyboardButton("Back")
                ban.row(start)
                ban.row(Back)
                bot.send_message(message.chat.id,"<b>Choice Option ?</b>",reply_markup=ban,parse_mode="HTML")
            elif message.text == "Give Me My Bans":
                BANS_FILE = open("banned.txt","r").read().splitlines()
                counter = len(BANS_FILE)
                if counter == 0:
                    bot.send_message(message.chat.id,"<b>You Havn't Any Bans!</b>",parse_mode="HTML")
                else:
                    count = 0
                    for UU in BANS_FILE:
                        count+=1
                        bot.send_message(message.chat.id,f"<b>{count}.{UU}</b>",parse_mode="HTML")
            elif message.text == "Run":
                bot.send_message(message.chat.id,"<b>Give Me Your Acconts [User:Pass] ? </b>",parse_mode="HTML")
                bot.register_next_step_handler_by_chat_id(message.chat.id,Login)
            elif message.text == "Control Panel":
                ss = types.ReplyKeyboardMarkup(True,one_time_keyboard=False)
                Add = types.KeyboardButton("Add User")
                Remove = types.KeyboardButton("Remove User")
                addpromocode = types.KeyboardButton("Add PromoCode")
                removepromocode = types.KeyboardButton("Remove PromoCode")
                Back = types.KeyboardButton("Back")
                ss.row(Add,Remove)
                ss.row(addpromocode,removepromocode)
                ss.row(Back)
                bot.send_message(message.chat.id, "<b>Hi Admin , Choice Option ?</b>", reply_markup=ss,parse_mode="HTML")
            elif message.text == "Add User":
                bot.send_message(message.chat.id,"<b>Give Me UserID ?</b>",parse_mode="HTML")
                bot.register_next_step_handler_by_chat_id(message.chat.id,AddUser)
            elif message.text == "Remove User":
                bot.send_message(message.chat.id, "<b>Give Me UserID ?</b>",parse_mode="HTML")
                bot.register_next_step_handler_by_chat_id(message.chat.id, RemoveUser)
            elif message.text == "Add PromoCode":
                bot.send_message(message.chat.id,"<b>Give Me PromoCode [Code:count:maxcustmre:type] ?</b>",parse_mode="HTML")
                bot.register_next_step_handler_by_chat_id(message.chat.id,NextStepPromoCode)
            elif message.text == "Remove PromoCode":
                bot.send_message(message.chat.id,"<b>Give Me PromoCode ?</b>",parse_mode="HTML")
                bot.register_next_step_handler_by_chat_id(message.chat.id,NextStepPromoCode)
        elif message.text == "Use Promo Code" :
            bot.send_message(message.chat.id , "<b>Please send the promo code! </b>" , parse_mode="HTML")
            bot.register_next_step_handler_by_chat_id(message.chat.id , PromoCodeUse)
        else:
            editme = bot.send_message(message.chat.id,"<b>Bro You'r Not Subscriber In Bot!\nContact @n1zis</b>",parse_mode="HTML" )
def ChanegSess(message):
    global  IsValid,MonitorSessionID
    timestamp = str(int(time.time()))
    account = str(message.text)
    username = account.split(":")[0]
    password = account.split(":")[1]
    data = {}
    data['guid'] = uuid4()
    data['enc_password'] = f"#PWD_INSTAGRAM:0:{timestamp}:{password}"
    data['username'] = username
    data['device_id'] = generate_DeviceId(username)
    data['login_attempt_count'] = '0'
    req = post('https://i.instagram.com/api/v1/accounts/login/', headers=headers_login(), data=data)
    if "logged_in_user" in req.text:
        if req.text.__contains__("Instagram User"):
            bot.send_message(int(ADMINID),f"<b>Banned : @{username}</b>",parse_mode="HTML")
        else:
            MonitorSessionID = req.cookies["sessionid"]
            with open("AdminSettings.json", "r") as reader:
                json_data = json.load(reader)
            isvalid = json_data["Bot"]["IsValid"]
            if isvalid == "False":
                json_data["Bot"]["IsValid"] == "True"
                Thread(None,Monitor).start()

            json_data["Bot"]["MonitorSessionID"] = MonitorSessionID
            with open("AdminSettings.json", "w") as fout:
                fout.write(json.dumps(json_data))
            bot.send_message(int(ADMINID),f"<b>Logged : @{username}</b>",parse_mode="HTML")
    else:
        error_messge = req.json()["message"]
        bot.send_message(message.chat.id,f"<b>{error_messge} : @{username}</b>",parse_mode="HTML")
def AddUser(message):
    user_id = str(message.text)
    open("Subscribers.txt","a").write(f"{user_id}\n")
    try:
        os.mkdir("./Subscribers/{}/".format(user_id))
        with open(f"./Subscribers/{str(user_id)}/Counter.txt","w") as gg:
            gg.write("0")
    except:
        folder_to_delete = './Subscribers/{}'.format(str(user_id))
        delete_folder(folder_to_delete)
        ff = open("Subscribers.txt",'r').read().splitlines()
        open("Subscribers.txt",'w').write('')
        ff.remove(user_id)
        for m in ff:
            open("Subscribers.txt", 'a').write(f"{m}\n")
        os.mkdir("./Subscribers/{}/".format(user_id))
        with open(f"./Subscribers/{str(user_id)}/Counter.txt","w") as gg:
            gg.write("0")
    bot.send_message(int(ADMINID),"<b>Done Active : {}</b>".format(user_id),parse_mode="HTML")
def RemoVePromo(message):
    promocode = message.text
    file = "./PromoCodes/{}.json".replace(promocode)
    if os.path.exists(file) :
        os.remove(file)
        bot.send_message(int(ADMINID) , f"<b>Done Remove PromoCode {promocode}!</b>" ,parse_mode="HTML")

def RemoveUser(message):
    user_id = str(message.text)
    try:
        folder_to_delete = './Subscribers/{}'.format(str(user_id))
        delete_folder(folder_to_delete)
        ff = open("Subscribers.txt",'r').read().splitlines()
        open("Subscribers.txt",'w').write('')
        ff.remove(user_id)
        for m in ff:
            open("Subscribers.txt", 'a').write(f"{m}\n")
        bot.send_message(int(ADMINID),"<b>Done Remove : {}</b>".format(user_id),parse_mode="HTML")
    except Exception as f:
        print(f)
        bot.send_message(int(ADMINID), "<b>Not Found : {}</b>".format(user_id),parse_mode="HTML")
def Login(message):
    global editme
    editme = bot.send_message(message.chat.id,"<b>Starting...</b>",parse_mode="HTML")
    open(f"./Subscribers/{str(message.chat.id)}/AccountsInfo.txt","w").write("")
    if message.content_type == "text":
        newpath = str(message.text).splitlines()
        for account in newpath:
            try:
                headers = {
                'X-IG-App-Locale': 'en_US',
                'X-IG-Device-Locale': 'en_US',
                'X-IG-Mapped-Locale': 'en_US',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTv10=',
                'User-Agent': USER_AGENT,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com',
            }
                timestamp = str(int(time.time()))
                username = account.split(":")[0]
                password = account.split(":")[1]
                ANDROID_ID = generate_DeviceId(username)
                UUID_OR_DEVICE_ID = str(uuid4())
                FAMILY_ID = str(uuid4())
                ixt_initial_screen_id = str(uuid4())
                shopping_session_id = str(uuid4())
                trigger_session_id = str(uuid4())
                data = {}
                data['guid'] = UUID_OR_DEVICE_ID
                data['enc_password'] = f"#PWD_INSTAGRAM:0:{timestamp}:{password}"
                data['username'] = username
                data['device_id'] = generate_DeviceId(username)
                data['login_attempt_count'] = '0'
                req = post('https://i.instagram.com/api/v1/accounts/login/', headers=headers, data=data)
                if "logged_in_user" in req.text:
                    if req.text.__contains__("Instagram User"):
                        bot.edit_message_text(f"<b>Banned : @{username}</b>", message.chat.id, editme.message_id,parse_mode="HTML")
                    else:
                        SESSIONID = req.cookies["sessionid"]
                        head = {

                                "accept": "*/*",
                                "accept-encoding": "gzip, deflate, br",
                                "accept-language": "en-US,en;q=0.9",
                                "content-length": "76",
                                "content-type": "application/x-www-form-urlencoded",
                                "cookie": f'sessionid={SESSIONID}',
                                "origin": "https://www.instagram.com",
                                "referer": "https://www.instagram.com/terms/unblock/?next=/api/v1/web/fxcal/ig_sso_users/",
                                "sec-ch-prefers-color-scheme": "light",
                                "sec-ch-ua": """Not?A_Brand"";v=""8"", ""Chromium"";v=""108"", ""Google Chrome"";v=""108""",
                                "sec-ch-ua-mobile": "?0",
                                "sec-ch-ua-platform": """Windows""",
                                "sec-fetch-dest": "empty",
                                "sec-fetch-mode": "cors",
                                "sec-fetch-site": "same-origin",
                                "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                                "viewport-width": "453",
                                "x-asbd-id": "198387",
                                "x-csrftoken": "m2kPFuLMBSGix4E8ZbRdIDyh0parUk5r",
                                "x-ig-app-id": "936619743392459",
                                "x-ig-www-claim": "hmac.AR2BpT3Q3cBoHtz_yRH8EvKCYkOb7loHvR4Jah_iP8s8BmTf",
                                "x-instagram-ajax": "9080db6b6a51",
                                "x-requested-with": "XMLHttpRequest",


                            }
                        data1 = "updates=%7B%22existing_user_intro_state%22%3A2%7D&current_screen_key=qp_intro"
                        data = "updates=%7B%22tos_data_policy_consent_state%22%3A2%7D&current_screen_key=tos"
                        requ = post("https://www.instagram.com/web/consent/update/",headers=head,data=data1).text
                        requ1 = post("https://www.instagram.com/web/consent/update/",headers=head,data=data).text
                        if '{"screen_key":"finished","status":"ok"}' in requ or '{"screen_key":"finished","status":"ok"}' in requ1:
                            bot.edit_message_text(f"<b>Term Accepted : @{username}</b>",message.chat.id,editme.message_id,parse_mode="HTML")
                            sleep(0.3)
                            TOKEN = SESSIONID
                            CLAIM_TOKEN =  req.headers["x-ig-set-www-claim"]
                            MID = req.headers["ig-set-x-mid"]
                            USER_ID = req.headers["ig-set-ig-u-ds-user-id"]
                            open(f"./Subscribers/{str(message.chat.id)}/AccountsInfo.txt","a").write(f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{username}\n")
                            bot.edit_message_text(f"<b>Logged : @{username}</b>",message.chat.id,editme.message_id,parse_mode="HTML")
                        elif "checkpoint_required" in requ:
                            bot.edit_message_text(f"<b>Secure : @{username}</b>",message.chat.id,editme.message_id,parse_mode="HTML")
                        else:
                            bot.edit_message_text(f"<b>Can't Accept Terms : @{username}</b>",message.chat.id,editme.message_id,parse_mode="HTML")

                else:
                    error_messge = req.json()["message"]
                    bot.edit_message_text(f"<b>{error_messge} : @{username}</b>",message.chat.id,editme.message_id,parse_mode="HTML")
            except Exception as h:
                print(h)
                bot.edit_message_text(f"<b>Invalid Format : @{account}</b>", message.chat.id, editme.message_id,parse_mode="HTML")
                sleep(1)
    elif message.content_type == "document":
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"./Subscribers/{str(message.chat.id)}/Accounts.txt", 'w') as new_file:
            new_file.write(downloaded_file)
        newpath = open(f"./Subscribers/{str(message.chat.id)}/Accounts.txt","r").read().splitlines()
        for account in newpath:
            try:
                headers = {
                'X-IG-App-Locale': 'en_US',
                'X-IG-Device-Locale': 'en_US',
                'X-IG-Mapped-Locale': 'en_US',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTv10=',
                'User-Agent':USER_AGENT,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com',
            }
                timestamp = str(int(time.time()))
                username = account.split(":")[0]
                password = account.split(":")[1]
                ANDROID_ID = generate_DeviceId(username)
                UUID_OR_DEVICE_ID = str(uuid4())
                FAMILY_ID = str(uuid4())
                ixt_initial_screen_id = str(uuid4())
                shopping_session_id = str(uuid4())
                trigger_session_id = str(uuid4())
                data = {}
                data['guid'] = UUID_OR_DEVICE_ID
                data['enc_password'] = f"#PWD_INSTAGRAM:0:{timestamp}:{password}"
                data['username'] = username
                data['device_id'] = generate_DeviceId(username)
                data['login_attempt_count'] = '0'
                req = post('https://i.instagram.com/api/v1/accounts/login/', headers=headers, data=data)
                if "logged_in_user" in req.text:
                    if req.text.__contains__("Instagram User"):
                        bot.edit_message_text(f"<b>Banned : @{username}</b>", message.chat.id, editme.message_id,parse_mode="HTML")
                    else:
                        SESSIONID = req.cookies["sessionid"]
                        head = {

                                "accept": "*/*",
                                "accept-encoding": "gzip, deflate, br",
                                "accept-language": "en-US,en;q=0.9",
                                "content-length": "76",
                                "content-type": "application/x-www-form-urlencoded",
                                "cookie": f'sessionid={SESSIONID}',
                                "origin": "https://www.instagram.com",
                                "referer": "https://www.instagram.com/terms/unblock/?next=/api/v1/web/fxcal/ig_sso_users/",
                                "sec-ch-prefers-color-scheme": "light",
                                "sec-ch-ua": """Not?A_Brand"";v=""8"", ""Chromium"";v=""108"", ""Google Chrome"";v=""108""",
                                "sec-ch-ua-mobile": "?0",
                                "sec-ch-ua-platform": """Windows""",
                                "sec-fetch-dest": "empty",
                                "sec-fetch-mode": "cors",
                                "sec-fetch-site": "same-origin",
                                "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                                "viewport-width": "453",
                                "x-asbd-id": "198387",
                                "x-csrftoken": "m2kPFuLMBSGix4E8ZbRdIDyh0parUk5r",
                                "x-ig-app-id": "936619743392459",
                                "x-ig-www-claim": "hmac.AR2BpT3Q3cBoHtz_yRH8EvKCYkOb7loHvR4Jah_iP8s8BmTf",
                                "x-instagram-ajax": "9080db6b6a51",
                                "x-requested-with": "XMLHttpRequest",

                            }
                        data1 = "updates=%7B%22existing_user_intro_state%22%3A2%7D&current_screen_key=qp_intro"
                        data = "updates=%7B%22tos_data_policy_consent_state%22%3A2%7D&current_screen_key=tos"
                        requ = post("https://www.instagram.com/web/consent/update/",headers=head,data=data1).text
                        requ1 = post("https://www.instagram.com/web/consent/update/",headers=head,data=data).text

                        if '{"screen_key":"finished","status":"ok"}' in requ or '{"screen_key":"finished","status":"ok"}' in requ1:
                            bot.edit_message_text(f"<b>Term Accepted : @{username}</b>",message.chat.id,editme.message_id,parse_mode="HTML")
                            sleep(0.3)
                            TOKEN = req.headers["ig-set-authorization"]
                            CLAIM_TOKEN =  req.headers["x-ig-set-www-claim"]
                            MID = req.headers["ig-set-x-mid"]
                            USER_ID = req.headers["ig-set-ig-u-ds-user-id"]
                            open(f"./Subscribers/{str(message.chat.id)}/AccountsInfo.txt","a").write(f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{username}\n")
                            bot.edit_message_text(f"<b>Logged : @{username}</b>",message.chat.id,editme.message_id,parse_mode="HTML")
                        elif "checkpoint_required" in requ:
                            bot.edit_message_text(f"<b>Secure : @{username}</b>",message.chat.id,editme.message_id,parse_mode="HTML")
                        else:
                            bot.edit_message_text(f"<b>Can't Accept Terms : @{username}</b>",message.chat.id,editme.message_id,parse_mode="HTML")

                else:
                    error_messge = req.json()["message"]
                    bot.edit_message_text(f"<b>{error_messge} : @{username}</b>",message.chat.id,editme.message_id,parse_mode="HTML")
            except:
                bot.edit_message_text(f"<b>Invalid Format : @{account}</b>", message.chat.id, editme.message_id,parse_mode="HTML")
                sleep(1)
    AccountsLenth = open(f"./Subscribers/{str(message.chat.id)}/AccountsInfo.txt","r").read().splitlines()
    if len(AccountsLenth) == 0:
        bot.edit_message_text(f"<b>No Good Account!</b>",message.chat.id,editme.message_id,parse_mode="HTML")
    else:
        bot.edit_message_text(f"<b>Give Me Your Targets [Accept File] ?</b>", message.chat.id, editme.message_id, parse_mode="HTML")
        bot.register_next_step_handler_by_chat_id(message.chat.id,SaveTargets)


def PromoCodeUse(message):
    promocode = message.text
    main_folder = "./PromoCodes"
    files = [f for f in os.listdir(main_folder) if os.path.isfile(os.path.join(main_folder , f))]
    user_id = message.chat.id
    if promocode not in files : return bot.send_message(user_id , f"<b>Alert! {promocode} is not valid! </b>" , parse_mode="HTML")
    for file in files :
        if file.endswith('.json') and promocode in file :
            user_id = message.chat.id
            open("Subscribers.txt","a").write(f"{message.chat.id}\n")
            try:
                os.mkdir("./Subscribers/{}/".format(user_id))
                with open(f"./Subscribers/{str(user_id)}/Counter.txt","w") as gg:
                    gg.write("0")
            except:
                folder_to_delete = './Subscribers/{}'.format(str(user_id))
                delete_folder(folder_to_delete)
                ff = open("Subscribers.txt",'r').read().splitlines()
                open("Subscribers.txt",'w').write('')
                ff.remove(user_id)
                for m in ff:
                    open("Subscribers.txt", 'a').write(f"{m}\n")
                os.mkdir("./Subscribers/{}/".format(user_id))
                with open(f"./Subscribers/{str(user_id)}/Counter.txt","w") as gg:
                    gg.write("0")
            bot.send_message(int(ADMINID),"<b>Done Active : {}</b>".format(user_id),parse_mode="HTML")
            bot.send_message(user_id,"<b>Done Actived Free Plan </b>",parse_mode="HTML")




@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global editme,Spam,Self,Hate,Violence,Nudity,Bullying,Drugs,mode7,StoreisID,MODE
    if call.data == "hilightmode":
        MODE = 2
        HilightsIds = []
        AccountList = open(f"./Subscribers/{str(call.from_user.id)}/AccountsInfo.txt", "r").read().splitlines()
        targets = open(f"./Subscribers/{str(call.from_user.id)}/Targets.txt", "r").read().splitlines()
        open(f"./Subscribers/{str(call.from_user.id)}/Stoires.txt",'w').write("")
        for Target in targets:
            Account = choice(AccountList)
            Token = Account.split('|')[0]
            Username = Target.split(":")[0]
            user_id = Target.split(':')[1]
            headers = {
                'X-IG-App-Locale': 'en_US',
                'X-IG-Device-Locale': 'en_US',
                'X-IG-Mapped-Locale': 'en_US',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Capabilities': '3brTv10=',
                'Cookie': f'sessionid={Token}',
                'User-Agent': 'Instagram 237.0.0.14.102 Android (28/9; 240dpi; 960x1280; google; G011A; G011A; intel; ar_EG; 373310563)',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'i.instagram.com',
            }
            reques = get(f'https://i.instagram.com/api/v1/highlights/{user_id}/highlights_tray/', headers=headers).json()
            try:
                lenth = len(reques["tray"])
                for i in range(lenth):
                    hilight = reques["tray"][i]["id"]
                    req2 = get(f"https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={hilight}",
                                             headers=headers).json()
                    req = len(req2["reels"][hilight]["items"])
                    for i in range(req):
                        ids = req2["reels"][hilight]["items"][i]["pk"]
                        HilightsIds.append(ids)
                        open(f"./Subscribers/{str(call.from_user.id)}/Stoires.txt", 'a').write(f'{ids}:{Username}\n')
                bot.edit_message_text(f"<b>Done Grapped {str(len(HilightsIds))} highlight/s</b>", call.from_user.id, editme.message_id,parse_mode="HTML")
                time.sleep(3)
                print(HilightsIds)
            except:
                bot.edit_message_text(f"<b>No highlight Found , Or Private Account : @{Username}</b>>", call.from_user.id,
                                      editme.message_id,parse_mode="HTML")
        bot.edit_message_text(f"<b>Finish Grapping!</b>", call.from_user.id, editme.message_id,parse_mode="HTML")
        if len(HilightsIds) == 0:
            bot.edit_message_text(f"<b>Bro , You Don't Have Any highlight ID To Report</b>", call.from_user.id, editme.message_id,parse_mode="HTML")
        else:
            Spam = False
            Self = False
            Hate = False
            Violence = False
            Nudity = False
            Bullying = False
            Drugs = False
            inl = types.InlineKeyboardMarkup(row_width=1)
            mode1 = types.InlineKeyboardButton("Spam [Unselected]", callback_data="Spam")
            mode2 = types.InlineKeyboardButton("Self [Unselected]", callback_data="Self")
            mode3 = types.InlineKeyboardButton("Hate [Unselected]", callback_data="Hate")
            mode4 = types.InlineKeyboardButton("Violence [Unselected]", callback_data="Violence")
            mode5 = types.InlineKeyboardButton("Nudity [Unselected]", callback_data="Nudity")
            mode6 = types.InlineKeyboardButton("Bullying [Unselected]", callback_data="Bullying")
            mode7 = types.InlineKeyboardButton("Drugs [Unselected]", callback_data="Drugs")
            st = types.InlineKeyboardButton("Start Reporting", callback_data="starts")
            inl.add(mode1, mode2, mode3, mode4, mode5, mode6, mode7, st)
            bot.edit_message_text("<b>Choice Reports ?</b>", call.from_user.id, editme.message_id, reply_markup=inl,parse_mode="HTML")
    elif call.data == "storymode":
        MODE = 2
        StoreisID = []
        AccountList  = open(f"./Subscribers/{str(call.from_user.id)}/AccountsInfo.txt","r").read().splitlines()
        targets = open(f"./Subscribers/{str(call.from_user.id)}/Targets.txt","r").read().splitlines()
        open(f"./Subscribers/{str(call.from_user.id)}/Stoires.txt", 'w').write("")
        for Target in targets:
            Account = choice(AccountList)
            Token = Account.split('|')[0]
            Username  = Target.split(":")[0]
            user_id = Target.split(':')[1]
            headers = {
            'X-IG-App-Locale': 'en_US',
            'X-IG-Device-Locale': 'en_US',
            'X-IG-Mapped-Locale': 'en_US',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': '3brTv10=',
            'Cookie': f'sessionid={Token}',
            'User-Agent':'Instagram 237.0.0.14.102 Android (28/9; 240dpi; 960x1280; google; G011A; G011A; intel; ar_EG; 373310563)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'i.instagram.com',
            }
            req = requests.get(f'https://i.instagram.com/api/v1/feed/user/{user_id}/story/',headers=headers)

            try:
                for story in req.json()["reel"]['items']:
                    StoreisID.append(str(story['id']))
                    open(f"./Subscribers/{str(call.from_user.id)}/Stoires.txt", 'a').write(f'{str(story["id"])}:{Username}\n')
                bot.edit_message_text(f"<b>Done Grapped All Storeis : @{Username}</b>",call.from_user.id,editme.message_id,parse_mode="HTML")
            except:
                bot.edit_message_text(f"<b>No Storeis Found , Or Private Account : @{Username}</b>",call.from_user.id,editme.message_id,parse_mode="HTML")
        bot.edit_message_text(f"<b>Finish Grapping!</b>",call.from_user.id,editme.message_id,parse_mode="HTML")
        if len(StoreisID) == 0:
            bot.edit_message_text(f"<b>Bro , You Don't Have Any StoryID To Report</b>",call.from_user.id,editme.message_id,parse_mode="HTML")
        else:
            Spam = False
            Self = False
            Hate = False
            Violence = False
            Nudity = False
            Bullying = False
            Drugs = False
            inl = types.InlineKeyboardMarkup(row_width=1)
            mode1 = types.InlineKeyboardButton("Spam [Unselected]",callback_data="Spam")
            mode2 = types.InlineKeyboardButton("Self [Unselected]",callback_data="Self")
            mode3 = types.InlineKeyboardButton("Hate [Unselected]",callback_data="Hate")
            mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
            mode5 = types.InlineKeyboardButton("Nudity [Unselected]",callback_data="Nudity")
            mode6 = types.InlineKeyboardButton("Bullying [Unselected]",callback_data="Bullying")
            mode7 = types.InlineKeyboardButton("Drugs [Unselected]",callback_data="Drugs")
            st = types.InlineKeyboardButton("Start Reporting",callback_data="starts")
            inl.add(mode1,mode2,mode3,mode4,mode5,mode6,mode7,st)
            bot.edit_message_text("<b>Choice Reports ?</b>",call.from_user.id,editme.message_id,reply_markup=inl,parse_mode="HTML")
    elif call.data == "profilemode":
        MODE = 1
        Spam = False
        Self = False
        Hate = False
        Violence = False
        Nudity = False
        Bullying = False
        Drugs = False
        inl = types.InlineKeyboardMarkup(row_width=1)
        mode1 = types.InlineKeyboardButton("Spam [Unselected]",callback_data="Spam")
        mode2 = types.InlineKeyboardButton("Self [Unselected]",callback_data="Self")
        mode3 = types.InlineKeyboardButton("Hate [Unselected]",callback_data="Hate")
        mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
        mode5 = types.InlineKeyboardButton("Nudity [Unselected]",callback_data="Nudity")
        mode6 = types.InlineKeyboardButton("Bullying [Unselected]",callback_data="Bullying")
        mode7 = types.InlineKeyboardButton("Drugs [Unselected]",callback_data="Drugs")
        st = types.InlineKeyboardButton("Start Reporting",callback_data="startr")
        inl.add(mode1,mode2,mode3,mode4,mode5,mode6,mode7,st)
        bot.edit_message_text("<b>Choice Reports ?</b>",call.from_user.id,editme.message_id,reply_markup=inl,parse_mode="HTML")
    elif call.data == "Spam":
        if Spam == False:
            Spam = True
            mode1 = types.InlineKeyboardButton("Spam [Selected]",callback_data="Spam")
        elif Spam == True:
            Spam = False
            mode1 = types.InlineKeyboardButton("Spam [Unselected]",callback_data="Spam")
        inl = types.InlineKeyboardMarkup(row_width=1)
        if Self == True:
            mode2 = types.InlineKeyboardButton("Self [Selected]",callback_data="Self")
        elif Self == False:
            mode2 = types.InlineKeyboardButton("Self [Unselected]",callback_data="Self")
        if Hate == True:
            mode3 = types.InlineKeyboardButton("Hate [Selected]",callback_data="Hate")
        elif Hate == False:
            mode3 = types.InlineKeyboardButton("Hate [Unselected]",callback_data="Hate")
        if Violence == True:
            mode4 = types.InlineKeyboardButton("Violence [Selected]",callback_data="Violence")
        elif Violence == False:
            mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
        if Nudity == True:
            mode5 = types.InlineKeyboardButton("Nudity [Selected]",callback_data="Nudity")
        elif Nudity == False:
            mode5 = types.InlineKeyboardButton("Nudity [Unselected]",callback_data="Nudity")
        if Bullying == True:
            mode6 = types.InlineKeyboardButton("Bullying [Selected]",callback_data="Bullying")
        elif Bullying == False:
            mode6 = types.InlineKeyboardButton("Bullying [Unselected]",callback_data="Bullying")
        if Drugs == True:
            mode7 = types.InlineKeyboardButton("Drugs [Selected]",callback_data="Drugs")
        elif Drugs == False:
            mode7 = types.InlineKeyboardButton("Drugs [Unselected]",callback_data="Drugs")
        if MODE == 1:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="startr")
        elif MODE == 2:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="starts")
        inl.add(mode1,mode2,mode3,mode4,mode5,mode6,mode7,st)
        bot.edit_message_text("<b>Choice Reports ?</b>",call.from_user.id,editme.message_id,reply_markup=inl,parse_mode="HTML")
    elif call.data == "Self":
        if Self == False:
            Self = True
            mode2 = types.InlineKeyboardButton("Self [Selected]",callback_data="Self")
        elif Self == True:
            Self = False
            mode2 = types.InlineKeyboardButton("Self [Unselected]",callback_data="Self")
        inl = types.InlineKeyboardMarkup(row_width=1)
        if Spam == True:
            mode1 = types.InlineKeyboardButton("Spam [Selected]",callback_data="Spam")
        elif Spam == False:
            mode1 = types.InlineKeyboardButton("Spam [Unselected]",callback_data="Spam")
        if Hate == True:
            mode3 = types.InlineKeyboardButton("Hate [Selected]",callback_data="Hate")
        elif Hate == False:
            mode3 = types.InlineKeyboardButton("Hate [Unselected]",callback_data="Hate")
        if Violence == True:
            mode4 = types.InlineKeyboardButton("Violence [Selected]",callback_data="Violence")
        elif Violence == False:
            mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
        if Nudity == True:
            mode5 = types.InlineKeyboardButton("Nudity [Selected]",callback_data="Nudity")
        elif Nudity == False:
            mode5 = types.InlineKeyboardButton("Nudity [Unselected]",callback_data="Nudity")
        if Bullying == True:
            mode6 = types.InlineKeyboardButton("Bullying [Selected]",callback_data="Bullying")
        elif Bullying == False:
            mode6 = types.InlineKeyboardButton("Bullying [Unselected]",callback_data="Bullying")
        if Drugs == True:
            mode7 = types.InlineKeyboardButton("Drugs [Selected]",callback_data="Drugs")
        elif Drugs == False:
            mode7 = types.InlineKeyboardButton("Drugs [Unselected]",callback_data="Drugs")
        if MODE == 1:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="startr")
        elif MODE == 2:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="starts")
        inl.add(mode1,mode2,mode3,mode4,mode5,mode6,mode7,st)
        bot.edit_message_text("<b>Choice Reports ?</b>",call.from_user.id,editme.message_id,reply_markup=inl,parse_mode="HTML")
    elif call.data == "Hate":
        if Hate == False:
            Hate = True
            mode3 = types.InlineKeyboardButton("Hate [Selected]",callback_data="Hate")
        elif Hate == True:
            Hate = False
            mode3 = types.InlineKeyboardButton("Hate [Unselected]",callback_data="Hate")
        inl = types.InlineKeyboardMarkup(row_width=1)
        if Self == True:
            mode2 = types.InlineKeyboardButton("Self [Selected]",callback_data="Self")
        elif Self == False:
            mode2 = types.InlineKeyboardButton("Self [Unselected]",callback_data="Self")
        if Spam == True:
            mode1 = types.InlineKeyboardButton("Spam [Selected]",callback_data="Spam")
        elif Spam == False:
            mode1 = types.InlineKeyboardButton("Spam [Unselected]",callback_data="Spam")
        if Hate == True:
            mode3 = types.InlineKeyboardButton("Hate [Selected]",callback_data="Hate")
        elif Hate == False:
            mode3 = types.InlineKeyboardButton("Hate [Unselected]",callback_data="Hate")
        if Violence == True:
            mode4 = types.InlineKeyboardButton("Violence [Selected]",callback_data="Violence")
        elif Violence == False:
            mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
        if Nudity == True:
            mode5 = types.InlineKeyboardButton("Nudity [Selected]",callback_data="Nudity")
        elif Nudity == False:
            mode5 = types.InlineKeyboardButton("Nudity [Unselected]",callback_data="Nudity")
        if Bullying == True:
            mode6 = types.InlineKeyboardButton("Bullying [Selected]",callback_data="Bullying")
        elif Bullying == False:
            mode6 = types.InlineKeyboardButton("Bullying [Unselected]",callback_data="Bullying")
        if Drugs == True:
            mode7 = types.InlineKeyboardButton("Drugs [Selected]",callback_data="Drugs")
        elif Drugs == False:
            mode7 = types.InlineKeyboardButton("Drugs [Unselected]",callback_data="Drugs")
        if MODE == 1:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="startr")
        elif MODE == 2:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="starts")
        inl.add(mode1,mode2,mode3,mode4,mode5,mode6,mode7,st)
        bot.edit_message_text("<b>Choice Reports ?</b>",call.from_user.id,editme.message_id,reply_markup=inl,parse_mode="HTML")
    elif call.data == "Violence":
        if Violence == False:
            Violence = True
            mode4 = types.InlineKeyboardButton("Violence [Selected]",callback_data="Violence")
        elif Violence == True:
            Violence = False
            mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
        inl = types.InlineKeyboardMarkup(row_width=1)

        if Self == True:
            mode2 = types.InlineKeyboardButton("Self [Selected]",callback_data="Self")
        elif Self == False:
            mode2 = types.InlineKeyboardButton("Self [Unselected]",callback_data="Self")
        if Spam == True:
            mode1 = types.InlineKeyboardButton("Spam [Selected]",callback_data="Spam")
        elif Spam == False:
            mode1 = types.InlineKeyboardButton("Spam [Unselected]",callback_data="Spam")
        if Hate == True:
            mode3 = types.InlineKeyboardButton("Hate [Selected]",callback_data="Hate")
        elif Hate == False:
            mode3 = types.InlineKeyboardButton("Hate [Unselected]",callback_data="Hate")
        if Violence == True:
            mode4 = types.InlineKeyboardButton("Violence [Selected]",callback_data="Violence")
        elif Violence == False:
            mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
        if Nudity == True:
            mode5 = types.InlineKeyboardButton("Nudity [Selected]",callback_data="Nudity")
        elif Nudity == False:
            mode5 = types.InlineKeyboardButton("Nudity [Unselected]",callback_data="Nudity")
        if Bullying == True:
            mode6 = types.InlineKeyboardButton("Bullying [Selected]",callback_data="Bullying")
        elif Bullying == False:
            mode6 = types.InlineKeyboardButton("Bullying [Unselected]",callback_data="Bullying")
        if Drugs == True:
            mode7 = types.InlineKeyboardButton("Drugs [Selected]",callback_data="Drugs")
        elif Drugs == False:
            mode7 = types.InlineKeyboardButton("Drugs [Unselected]",callback_data="Drugs")
        if MODE == 1:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="startr")
        elif MODE == 2:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="starts")
        inl.add(mode1,mode2,mode3,mode4,mode5,mode6,mode7,st)
        bot.edit_message_text("<b>Choice Reports ?</b>",call.from_user.id,editme.message_id,reply_markup=inl,parse_mode="HTML")
    elif call.data == "Nudity":
        if Nudity == False:
            Nudity = True
            mode5 = types.InlineKeyboardButton("Nudity [Selected]",callback_data="Nudity")
        elif Nudity == True:
            Nudity = False
            mode5 = types.InlineKeyboardButton("Nudity [Unselected]",callback_data="Nudity")
        inl = types.InlineKeyboardMarkup(row_width=1)
        if Violence == True:
            mode4 = types.InlineKeyboardButton("Violence [Selected]",callback_data="Violence")
        elif Violence == False:
            mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
        if Self == True:
            mode2 = types.InlineKeyboardButton("Self [Selected]",callback_data="Self")
        elif Self == False:
            mode2 = types.InlineKeyboardButton("Self [Unselected]",callback_data="Self")
        if Spam == True:
            mode1 = types.InlineKeyboardButton("Spam [Selected]",callback_data="Spam")
        elif Spam == False:
            mode1 = types.InlineKeyboardButton("Spam [Unselected]",callback_data="Spam")
        if Hate == True:
            mode3 = types.InlineKeyboardButton("Hate [Selected]",callback_data="Hate")
        elif Hate == False:
            mode3 = types.InlineKeyboardButton("Hate [Unselected]",callback_data="Hate")
        if Violence == True:
            mode4 = types.InlineKeyboardButton("Violence [Selected]",callback_data="Violence")
        elif Violence == False:
            mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
        if Nudity == True:
            mode5 = types.InlineKeyboardButton("Nudity [Selected]",callback_data="Nudity")
        elif Nudity == False:
            mode5 = types.InlineKeyboardButton("Nudity [Unselected]",callback_data="Nudity")
        if Bullying == True:
            mode6 = types.InlineKeyboardButton("Bullying [Selected]",callback_data="Bullying")
        elif Bullying == False:
            mode6 = types.InlineKeyboardButton("Bullying [Unselected]",callback_data="Bullying")
        if Drugs == True:
            mode7 = types.InlineKeyboardButton("Drugs [Selected]",callback_data="Drugs")
        elif Drugs == False:
            mode7 = types.InlineKeyboardButton("Drugs [Unselected]",callback_data="Drugs")
        if MODE == 1:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="startr")
        elif MODE == 2:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="starts")
        inl.add(mode1,mode2,mode3,mode4,mode5,mode6,mode7,st)
        bot.edit_message_text("<b>Choice Reports ?</b>",call.from_user.id,editme.message_id,reply_markup=inl,parse_mode="HTML")
    elif call.data == "Bullying":
        if Bullying == False:
            Bullying = True
            mode6 = types.InlineKeyboardButton("Bullying [Selected]",callback_data="Bullying")
        elif Bullying == True:
            Bullying = False
            mode6 = types.InlineKeyboardButton("Bullying [Unselected]",callback_data="Bullying")
        if Violence == True:
            mode4 = types.InlineKeyboardButton("Violence [Selected]",callback_data="Violence")
        elif Violence == False:
            mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
        inl = types.InlineKeyboardMarkup(row_width=1)
        if Self == True:
            mode2 = types.InlineKeyboardButton("Self [Selected]",callback_data="Self")
        elif Self == False:
            mode2 = types.InlineKeyboardButton("Self [Unselected]",callback_data="Self")
        if Spam == True:
            mode1 = types.InlineKeyboardButton("Spam [Selected]",callback_data="Spam")
        elif Spam == False:
            mode1 = types.InlineKeyboardButton("Spam [Unselected]",callback_data="Spam")
        if Hate == True:
            mode3 = types.InlineKeyboardButton("Hate [Selected]",callback_data="Hate")
        elif Hate == False:
            mode3 = types.InlineKeyboardButton("Hate [Unselected]",callback_data="Hate")
        if Violence == True:
            mode4 = types.InlineKeyboardButton("Violence [Selected]",callback_data="Violence")
        elif Violence == False:
            mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
        if Nudity == True:
            mode5 = types.InlineKeyboardButton("Nudity [Selected]",callback_data="Nudity")
        elif Nudity == False:
            mode5 = types.InlineKeyboardButton("Nudity [Unselected]",callback_data="Nudity")
        if Bullying == True:
            mode6 = types.InlineKeyboardButton("Bullying [Selected]",callback_data="Bullying")
        elif Bullying == False:
            mode6 = types.InlineKeyboardButton("Bullying [Unselected]",callback_data="Bullying")
        if Drugs == True:
            mode7 = types.InlineKeyboardButton("Drugs [Selected]",callback_data="Drugs")
        elif Drugs == False:
            mode7 = types.InlineKeyboardButton("Drugs [Unselected]",callback_data="Drugs")
        if MODE == 1:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="startr")
        elif MODE == 2:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="starts")
        inl.add(mode1,mode2,mode3,mode4,mode5,mode6,mode7,st)
        bot.edit_message_text("<b>Choice Reports ?</b>",call.from_user.id,editme.message_id,reply_markup=inl,parse_mode="HTML")
    elif call.data == "Drugs":
        if Drugs == False:
            Drugs = True
            mode7 = types.InlineKeyboardButton("Drugs [Selected]",callback_data="Drugs")
        elif Drugs == True:
            Drugs = False
            mode7 = types.InlineKeyboardButton("Drugs [Unselected]",callback_data="Drugs")
        inl = types.InlineKeyboardMarkup(row_width=1)
        if Violence == True:
            mode4 = types.InlineKeyboardButton("Violence [Selected]",callback_data="Violence")
        elif Violence == False:
            mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
        if Self == True:
            mode2 = types.InlineKeyboardButton("Self [Selected]",callback_data="Self")
        elif Self == False:
            mode2 = types.InlineKeyboardButton("Self [Unselected]",callback_data="Self")
        if Spam == True:
            mode1 = types.InlineKeyboardButton("Spam [Selected]",callback_data="Spam")
        elif Spam == False:
            mode1 = types.InlineKeyboardButton("Spam [Unselected]",callback_data="Spam")
        if Hate == True:
            mode3 = types.InlineKeyboardButton("Hate [Selected]",callback_data="Hate")
        elif Hate == False:
            mode3 = types.InlineKeyboardButton("Hate [Unselected]",callback_data="Hate")
        if Violence == True:
            mode4 = types.InlineKeyboardButton("Violence [Selected]",callback_data="Violence")
        elif Violence == False:
            mode4 = types.InlineKeyboardButton("Violence [Unselected]",callback_data="Violence")
        if Nudity == True:
            mode5 = types.InlineKeyboardButton("Nudity [Selected]",callback_data="Nudity")
        elif Nudity == False:
            mode5 = types.InlineKeyboardButton("Nudity [Unselected]",callback_data="Nudity")
        if Bullying == True:
            mode6 = types.InlineKeyboardButton("Bullying [Selected]",callback_data="Bullying")
        elif Bullying == False:
            mode6 = types.InlineKeyboardButton("Bullying [Unselected]",callback_data="Bullying")
        if Drugs == True:
            mode7 = types.InlineKeyboardButton("Drugs [Selected]",callback_data="Drugs")
        elif Drugs == False:
            mode7 = types.InlineKeyboardButton("Drugs [Unselected]",callback_data="Drugs")
        if MODE == 1:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="startr")
        elif MODE == 2:
            st = types.InlineKeyboardButton("Start Reporting",callback_data="starts")
        inl.add(mode1,mode2,mode3,mode4,mode5,mode6,mode7,st)
        bot.edit_message_text("<b>Choice Reports ?</b>",call.from_user.id,editme.message_id,reply_markup=inl,parse_mode="HTML")
    elif call.data == "startr":
        bot.edit_message_text("<b>Starting...</b>",call.from_user.id,editme.message_id,parse_mode="HTML")
        Thread(None,ReportProfile,args=[str(call.from_user.id)]).start()
    elif call.data == "starts":
        bot.edit_message_text("<b>Starting...</b>",call.from_user.id,editme.message_id,parse_mode="HTML")
        Thread(None,ReportStory,args=[str(call.from_user.id)]).start()
def ReportProfile(Userid):
    global url
    print("[+] Start Report Profile : {}".format(Userid))
    Done = 0
    Error = 0
    account = open(f"./Subscribers/{str(Userid)}/AccountsInfo.txt","r").read().splitlines()
    targets = open(f"./Subscribers/{str(Userid)}/Targets.txt","r").read().splitlines()
    sleepnumber =  int(open(f"./Subscribers/{str(Userid)}/Sleep.txt","r").read().splitlines()[0])
    while 1:
        if MessageNow == "Stop":
            if ChatIDNow == Userid:
                print("[+] Stop Report Profile : {}".format(Userid))
                bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                break
        else:
                for targetaccount in targets:
                    TargetUsername = targetaccount.split(":")[0]
                    TargetID = targetaccount.split(":")[1]
                    if Spam == True:
                            if MessageNow == "Stop":
                                if ChatIDNow == Userid:
                                    print("[+] Stop Report Profile : {}".format(Userid))
                                    bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                    break
                            else:
                                for AccountInfo in account:
                                    AccountInfo = str(AccountInfo)
                                    TOKEN = AccountInfo.split("|")[0]
                                    CLAIM_TOKEN = AccountInfo.split("|")[1]
                                    ANDROID_ID = AccountInfo.split("|")[2]
                                    UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                    MID = AccountInfo.split("|")[4]
                                    USER_ID = AccountInfo.split("|")[5]
                                    FAMILY_ID = AccountInfo.split("|")[6]
                                    shopping_session_id = AccountInfo.split("|")[7]
                                    ixt_initial_screen_id = AccountInfo.split("|")[8]
                                    trigger_session_id = AccountInfo.split("|")[9]
                                    UsernameNow = AccountInfo.split('|')[10]
                                    try:
                                        data = f"source_name=&reason_id=1&frx_context="
                                        k = {
                                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
                                            "Host": "i.instagram.com",
                                            'cookie': f"sessionid={TOKEN}",
                                            "X-CSRFToken": "uNs1OZ6CPvJBSmmQOvWDKGFkm2frIDEY",
                                            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                                            }
                                        k2 = requests.post(f"https://i.instagram.com/users/{TargetID}/flag/", headers=k, data=data)
                                        if k2.status_code == 404:
                                            print(f"Banned : {TargetUsername}")
                                            bot.send_message(int(Userid),f"<b>Banned : {TargetUsername}</b>",parse_mode="HTML")
                                        elif k2.status_code == 200:
                                            Done+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Spam</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                        else:
                                            Error+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Spam</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    except:
                                        headers = {
                                            "Accept": "*/*",
                                            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                            "Content-Type": "application/x-www-form-urlencoded",
                                            "Cookie": "massing",
                                            "Dpr": "0.9",
                                            "Origin": "https://www.instagram.com",
                                            "Referer": "https://www.instagram.com/{}/".format(TargetUsername),
                                            "Sec-Ch-Prefers-Color-Scheme": "light",
                                            "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                            "Sec-Ch-Ua-Mobile": "?0",
                                            "Sec-Ch-Ua-Model": """""",
                                            "Sec-Ch-Ua-Platform": """Windows""",
                                            "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                            "Sec-Fetch-Dest": "empty",
                                            "Sec-Fetch-Mode": "cors",
                                            "Sec-Fetch-Site": "same-origin",
                                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                            "Viewport-Width": "238",
                                            "X-Asbd-Id": "129477",
                                            "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                            "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                            "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                            "X-Ig-App-Id": "936619743392459"}
                                        data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{TargetUsername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                        response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                        if response.text.__contains__("id"):
                                            mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                            account.remove(
                                                f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                            if len(account) == 0:
                                                bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid),
                                                                    mess.message_id,parse_mode="HTML")
                                            else:
                                                sleep(1)
                                                bot.delete_message(int(Userid), mess.message_id)
                                        else:
                                            print(f"Banned : {TargetUsername}")
                                            bot.send_message(int(Userid), f"<b>Banned : {TargetUsername}</b>",parse_mode="HTML")
                            sleep(sleepnumber)
                    if Self == True:
                            if MessageNow == "Stop":
                                if ChatIDNow == Userid:
                                    print("[+] Stop Report Profile : {}".format(Userid))
                                    bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                    break
                            else:
                                for AccountInfo in account:
                                    AccountInfo = str(AccountInfo)
                                    TOKEN = AccountInfo.split("|")[0]
                                    CLAIM_TOKEN = AccountInfo.split("|")[1]
                                    ANDROID_ID = AccountInfo.split("|")[2]
                                    UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                    MID = AccountInfo.split("|")[4]
                                    USER_ID = AccountInfo.split("|")[5]
                                    FAMILY_ID = AccountInfo.split("|")[6]
                                    shopping_session_id = AccountInfo.split("|")[7]
                                    ixt_initial_screen_id = AccountInfo.split("|")[8]
                                    trigger_session_id = AccountInfo.split("|")[9]
                                    UsernameNow = AccountInfo.split('|')[10]
                                    try:
                                        url = "https://www.instagram.com/api/v1/web/reports/get_frx_prompt/"
                                        hea = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(TargetUsername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                        data1 = {
                                            'entry_point':'1',
                                            'location':'2',
                                            'object_type':'5',
                                            'object_id':TargetID,
                                            'container_module':'profilePage',
                                            'frx_prompt_request_type':'1'}
                                        req1  = requests.post(url=url,headers=hea,data=data1)
                                        context1 = req1.json()['response']['context']
                                        data2 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context1,
                                                'selected_tag_types':'["ig_report_account"]',
                                                'frx_prompt_request_type':'2',
                                            }
                                        req2  = requests.post(url=url,headers=hea,data=data2)
                                        context2 = req2.json()['response']['context']
                                        data3 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context2,
                                                'selected_tag_types':'["ig_self_injury_v3"]',
                                                'frx_prompt_request_type':'2',
                                            }
                                        req3  = requests.post(url=url,headers=hea,data=data3)
                                        context3= req3.json()['response']['context']
                                        data4 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context3,
                                                'action_type':'2',
                                                'frx_prompt_request_type':'4'
                                            }
                                        req4  = requests.post(url=url,headers=hea,data=data4)
                                        if req4.json()["status"] == "ok" in req4.text:
                                            Done+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Self</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                        else:
                                            Error+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Self</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    except Exception as g:
                                        print(g)
                                        headers = {
                                            "Accept": "*/*",
                                            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                            "Content-Type": "application/x-www-form-urlencoded",
                                            "Cookie": "massing",
                                            "Dpr": "0.9",
                                            "Origin": "https://www.instagram.com",
                                            "Referer": "https://www.instagram.com/{}/".format(TargetUsername),
                                            "Sec-Ch-Prefers-Color-Scheme": "light",
                                            "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                            "Sec-Ch-Ua-Mobile": "?0",
                                            "Sec-Ch-Ua-Model": """""",
                                            "Sec-Ch-Ua-Platform": """Windows""",
                                            "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                            "Sec-Fetch-Dest": "empty",
                                            "Sec-Fetch-Mode": "cors",
                                            "Sec-Fetch-Site": "same-origin",
                                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                            "Viewport-Width": "238",
                                            "X-Asbd-Id": "129477",
                                            "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                            "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                            "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                            "X-Ig-App-Id": "936619743392459"}
                                        data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{TargetUsername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                        response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                        if response.text.__contains__("id"):
                                            mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                            account.remove(
                                                f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                            if len(account) == 0:
                                                bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid),
                                                                    mess.message_id,parse_mode="HTML")
                                            else:
                                                sleep(1)
                                                bot.delete_message(int(Userid), mess.message_id)
                                        else:
                                            print(f"Banned : {TargetUsername}")
                                            bot.send_message(int(Userid), f"<b>Banned : {TargetUsername}</b>",parse_mode="HTML")
                            sleep(sleepnumber)
                    if Hate == True:
                            if MessageNow == "Stop":
                                if ChatIDNow == Userid:
                                    print("[+] Stop Report Profile : {}".format(Userid))
                                    bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                    break
                            else:
                                for AccountInfo in account:
                                    AccountInfo = str(AccountInfo)
                                    TOKEN = AccountInfo.split("|")[0]
                                    CLAIM_TOKEN = AccountInfo.split("|")[1]
                                    ANDROID_ID = AccountInfo.split("|")[2]
                                    UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                    MID = AccountInfo.split("|")[4]
                                    USER_ID = AccountInfo.split("|")[5]
                                    FAMILY_ID = AccountInfo.split("|")[6]
                                    shopping_session_id = AccountInfo.split("|")[7]
                                    ixt_initial_screen_id = AccountInfo.split("|")[8]
                                    trigger_session_id = AccountInfo.split("|")[9]
                                    UsernameNow = AccountInfo.split('|')[10]
                                    try:
                                        url = "https://www.instagram.com/api/v1/web/reports/get_frx_prompt/"
                                        headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(TargetUsername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                        data1 = {
                                            'entry_point':'1',
                                            'location':'2',
                                            'object_type':'5',
                                            'object_id':TargetID,
                                            'container_module':'profilePage',
                                            'frx_prompt_request_type':'1'}
                                        req1  = requests.post(url=url,headers=hea,data=data1)
                                        context1 = req1.json()['response']['context']
                                        data2 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context1,
                                                'selected_tag_types':'["ig_report_account"]',
                                                'frx_prompt_request_type':'2',
                                            }
                                        req2  = requests.post(url=url,headers=hea,data=data2)
                                        context2 = req2.json()['response']['context']
                                        data3 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context2,
                                                'selected_tag_types':'["ig_its_inappropriate"]',
                                                'frx_prompt_request_type':'2',
                                            }
                                        req3  = requests.post(url=url,headers=hea,data=data3)
                                        context3= req3.json()['response']['context']
                                        data4 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context3,
                                                'selected_tag_types': '["ig_hate_speech_v3"]',
                                                'frx_prompt_request_type':'2'
                                            }
                                        req4  = requests.post(url=url,headers=hea,data=data4)
                                        context4= req4.json()['response']['context']
                                        data5 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context4,
                                                'action_type':'2',
                                                'frx_prompt_request_type':'4'
                                            }
                                        req5  = requests.post(url=url,headers=hea,data=data5)
                                        if req5.json()["status"] == "ok" in req5.text:
                                            Done+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Hate</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                        else:
                                            Error+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Hate</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    except:
                                        headers = {
                                            "Accept": "*/*",
                                            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                            "Content-Type": "application/x-www-form-urlencoded",
                                            "Cookie": "massing",
                                            "Dpr": "0.9",
                                            "Origin": "https://www.instagram.com",
                                            "Referer": "https://www.instagram.com/{}/".format(TargetUsername),
                                            "Sec-Ch-Prefers-Color-Scheme": "light",
                                            "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                            "Sec-Ch-Ua-Mobile": "?0",
                                            "Sec-Ch-Ua-Model": """""",
                                            "Sec-Ch-Ua-Platform": """Windows""",
                                            "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                            "Sec-Fetch-Dest": "empty",
                                            "Sec-Fetch-Mode": "cors",
                                            "Sec-Fetch-Site": "same-origin",
                                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                            "Viewport-Width": "238",
                                            "X-Asbd-Id": "129477",
                                            "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                            "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                            "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                            "X-Ig-App-Id": "936619743392459"}
                                        data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{TargetUsername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                        response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                        if response.text.__contains__("id"):
                                            mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                            account.remove(
                                                f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                            if len(account) == 0:
                                                bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid),
                                                                    mess.message_id,parse_mode="HTML")
                                            else:
                                                sleep(1)
                                                bot.delete_message(int(Userid), mess.message_id)
                                        else:
                                            print(f"Banned : {TargetUsername}")
                                            bot.send_message(int(Userid), f"<b>Banned : {TargetUsername}</b>",parse_mode="HTML")
                            sleep(sleepnumber)
                    if Violence == True:
                            if MessageNow == "Stop":
                                if ChatIDNow == Userid:
                                    print("[+] Stop Report Profile : {}".format(Userid))
                                    bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                    break
                            else:
                                for AccountInfo in account:
                                    AccountInfo = str(AccountInfo)
                                    TOKEN = AccountInfo.split("|")[0]
                                    CLAIM_TOKEN = AccountInfo.split("|")[1]
                                    ANDROID_ID = AccountInfo.split("|")[2]
                                    UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                    MID = AccountInfo.split("|")[4]
                                    USER_ID = AccountInfo.split("|")[5]
                                    FAMILY_ID = AccountInfo.split("|")[6]
                                    shopping_session_id = AccountInfo.split("|")[7]
                                    ixt_initial_screen_id = AccountInfo.split("|")[8]
                                    trigger_session_id = AccountInfo.split("|")[9]
                                    UsernameNow = AccountInfo.split('|')[10]
                                    try:
                                        url = "https://www.instagram.com/api/v1/web/reports/get_frx_prompt/"
                                        headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(TargetUsername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                        data1 = {
                                            'entry_point':'1',
                                            'location':'2',
                                            'object_type':'5',
                                            'object_id':TargetID,
                                            'container_module':'profilePage',
                                            'frx_prompt_request_type':'1',
                                        }

                                        req1  = requests.post(url,headers=headers,data=data1)
                                        context1 = req1.json()['response']['context']
                                        data2 = {
                                            'entry_point':'1',
                                            'location':'2',
                                            'object_type':'5',
                                            'object_id':TargetID,
                                            'container_module':'profilePage',
                                            'context':context1,
                                            'selected_tag_types':'["ig_report_account"]',
                                            'frx_prompt_request_type':'2',
                                        }
                                        req2  = requests.post(url,headers=headers,data=data2)
                                        context2 = req2.json()['response']['context']
                                        data4 = {
                                            'entry_point':'1',
                                            'location':'2',
                                            'object_type':'5',
                                            'object_id':TargetID,
                                            'container_module':'profilePage',
                                            'context':context2,
                                            'selected_tag_types':'["ig_violence_parent"]',
                                            'frx_prompt_request_type':'2',
                                        }
                                        req4  = requests.post(url,headers=headers,data=data4)
                                        context4 = req4.json()['response']['context']
                                        data5 = {
                                            'entry_point':'1',
                                            'location':'2',
                                            'object_type':'5',
                                            'object_id': TargetID,
                                            'container_module':'profilePage',
                                            'context':context4,
                                            'selected_tag_types':'["ig_violence_threat"]',
                                            'action_type':'2',
                                            'frx_prompt_request_type':'2',
                                        }
                                        req5  = requests.post(url,headers=headers,data=data5)
                                        if req5.json()["status"] == "ok" in req5.text:
                                            Done+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Violance</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                        else:
                                            Error+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Violance</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    except Exception as f:
                                        print(f)
                                        headers = {
                                            "Accept": "*/*",
                                            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                            "Content-Type": "application/x-www-form-urlencoded",
                                            "Cookie": "massing",
                                            "Dpr": "0.9",
                                            "Origin": "https://www.instagram.com",
                                            "Referer": "https://www.instagram.com/{}/".format(TargetUsername),
                                            "Sec-Ch-Prefers-Color-Scheme": "light",
                                            "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                            "Sec-Ch-Ua-Mobile": "?0",
                                            "Sec-Ch-Ua-Model": """""",
                                            "Sec-Ch-Ua-Platform": """Windows""",
                                            "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                            "Sec-Fetch-Dest": "empty",
                                            "Sec-Fetch-Mode": "cors",
                                            "Sec-Fetch-Site": "same-origin",
                                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                            "Viewport-Width": "238",
                                            "X-Asbd-Id": "129477",
                                            "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                            "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                            "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                            "X-Ig-App-Id": "936619743392459"}
                                        data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{TargetUsername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                        response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                        if response.text.__contains__("id"):
                                            mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                            account.remove(
                                                f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                            if len(account) == 0:
                                                bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid),
                                                                    mess.message_id,parse_mode="HTML")
                                            else:
                                                sleep(1)
                                                bot.delete_message(int(Userid), mess.message_id)
                                        else:
                                            print(f"Banned : {TargetUsername}")
                                            bot.send_message(int(Userid), f"<b>Banned : {TargetUsername}</b>",parse_mode="HTML")
                            sleep(sleepnumber)
                    if Nudity == True:
                            if MessageNow == "Stop":
                                if ChatIDNow == Userid:
                                    print("[+] Stop Report Profile : {}".format(Userid))
                                    bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                    break
                            else:
                                for AccountInfo in account:
                                    AccountInfo = str(AccountInfo)
                                    TOKEN = AccountInfo.split("|")[0]
                                    CLAIM_TOKEN = AccountInfo.split("|")[1]
                                    ANDROID_ID = AccountInfo.split("|")[2]
                                    UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                    MID = AccountInfo.split("|")[4]
                                    USER_ID = AccountInfo.split("|")[5]
                                    FAMILY_ID = AccountInfo.split("|")[6]
                                    shopping_session_id = AccountInfo.split("|")[7]
                                    ixt_initial_screen_id = AccountInfo.split("|")[8]
                                    trigger_session_id = AccountInfo.split("|")[9]
                                    UsernameNow = AccountInfo.split('|')[10]
                                    try:
                                        url = "https://www.instagram.com/api/v1/web/reports/get_frx_prompt/"
                                        hea = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(TargetUsername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                        data1 = {
                                            'entry_point':'1',
                                            'location':'2',
                                            'object_type':'5',
                                            'object_id':TargetID,
                                            'container_module':'profilePage',
                                            'frx_prompt_request_type':'1'}
                                        req1  = requests.post(url=url,headers=hea,data=data1)
                                        context1 = req1.json()['response']['context']
                                        data2 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context1,
                                                'selected_tag_types':'["ig_report_account"]',
                                                'frx_prompt_request_type':'2',
                                            }
                                        req2  = requests.post(url=url,headers=hea,data=data2)
                                        context2 = req2.json()['response']['context']
                                        data3 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context2,
                                                'selected_tag_types':'["ig_its_inappropriate"]',
                                                'frx_prompt_request_type':'2',
                                            }
                                        req3  = requests.post(url=url,headers=hea,data=data3)
                                        context3= req3.json()['response']['context']
                                        data4 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context3,
                                                'selected_tag_types': '["ig_nudity_v2"]',
                                                'frx_prompt_request_type':'2'
                                            }
                                        req4  = requests.post(url=url,headers=hea,data=data4)
                                        context4= req4.json()['response']['context']
                                        data5 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context4,
                                                'selected_tag_types': '["ig_nudity_or_pornography_v3"]',
                                                'action_type':'2',
                                                'frx_prompt_request_type':'2'
                                            }
                                        req5  = requests.post(url=url,headers=hea,data=data5)
                                        if req5.json()["status"] == "ok" in req5.text:
                                            Done+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Nutidy</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                        else:
                                            Error+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Nutidy</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    except:
                                        headers = {
                                            "Accept": "*/*",
                                            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                            "Content-Type": "application/x-www-form-urlencoded",
                                            "Cookie": "massing",
                                            "Dpr": "0.9",
                                            "Origin": "https://www.instagram.com",
                                            "Referer": "https://www.instagram.com/{}/".format(TargetUsername),
                                            "Sec-Ch-Prefers-Color-Scheme": "light",
                                            "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                            "Sec-Ch-Ua-Mobile": "?0",
                                            "Sec-Ch-Ua-Model": """""",
                                            "Sec-Ch-Ua-Platform": """Windows""",
                                            "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                            "Sec-Fetch-Dest": "empty",
                                            "Sec-Fetch-Mode": "cors",
                                            "Sec-Fetch-Site": "same-origin",
                                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                            "Viewport-Width": "238",
                                            "X-Asbd-Id": "129477",
                                            "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                            "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                            "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                            "X-Ig-App-Id": "936619743392459"}
                                        data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{TargetUsername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                        response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                        if response.text.__contains__("id"):
                                            mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                            account.remove(
                                                f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                            if len(account) == 0:
                                                bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid),
                                                                    mess.message_id,parse_mode="HTML")
                                            else:
                                                sleep(1)
                                                bot.delete_message(int(Userid), mess.message_id)
                                        else:
                                            print(f"Banned : {TargetUsername}")
                                            bot.send_message(int(Userid), f"<b>Banned : {TargetUsername}</b>",parse_mode="HTML")
                            sleep(sleepnumber)
                    if Bullying == True:
                            if MessageNow == "Stop":
                                if ChatIDNow == Userid:
                                    print("[+] Stop Report Profile : {}".format(Userid))
                                    bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                    break
                            else:
                                for AccountInfo in account:
                                    AccountInfo = str(AccountInfo)
                                    TOKEN = AccountInfo.split("|")[0]
                                    CLAIM_TOKEN = AccountInfo.split("|")[1]
                                    ANDROID_ID = AccountInfo.split("|")[2]
                                    UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                    MID = AccountInfo.split("|")[4]
                                    USER_ID = AccountInfo.split("|")[5]
                                    FAMILY_ID = AccountInfo.split("|")[6]
                                    shopping_session_id = AccountInfo.split("|")[7]
                                    ixt_initial_screen_id = AccountInfo.split("|")[8]
                                    trigger_session_id = AccountInfo.split("|")[9]
                                    UsernameNow = AccountInfo.split('|')[10]
                                    try:
                                        url = "https://www.instagram.com/api/v1/web/reports/get_frx_prompt/"
                                        hea = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(TargetUsername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                        data1 = {
                                            'entry_point':'1',
                                            'location':'2',
                                            'object_type':'5',
                                            'object_id':TargetID,
                                            'container_module':'profilePage',
                                            'frx_prompt_request_type':'1'}
                                        req1  = requests.post(url=url,headers=hea,data=data1)
                                        context1 = req1.json()['response']['context']
                                        data2 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context1,
                                                'selected_tag_types':'["ig_report_account"]',
                                                'frx_prompt_request_type':'2',
                                            }
                                        req2  = requests.post(url=url,headers=hea,data=data2)
                                        context2 = req2.json()['response']['context']
                                        data3 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context2,
                                                'selected_tag_types':'["ig_its_inappropriate"]',
                                                'frx_prompt_request_type':'2',
                                            }
                                        req3  = requests.post(url=url,headers=hea,data=data3)
                                        context3= req3.json()['response']['context']
                                        data4 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context3,
                                                'selected_tag_types': '["ig_bullying_or_harassment_comment_v3"]',
                                                'frx_prompt_request_type':'2'
                                            }
                                        req4  = requests.post(url=url,headers=hea,data=data4)
                                        context4= req4.json()['response']['context']
                                        data5 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context4,
                                                'selected_tag_types': '["ig_bullying_or_harassment_me_v3"]',
                                                'frx_prompt_request_type':'2'
                                        }
                                        req5  = requests.post(url=url,headers=hea,data=data5)
                                        context5 = req5.json()['response']['context']
                                        data6 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context5,
                                                'action_type': '2',
                                                'frx_prompt_request_type':'4'
                                        }
                                        req6  = requests.post(url=url,headers=hea,data=data6)
                                        if req6.json()["status"] == "ok" in req6.text:
                                            Done+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Bullying</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                        else:
                                            Error+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Bullying</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    except:
                                        headers = {
                                            "Accept": "*/*",
                                            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                            "Content-Type": "application/x-www-form-urlencoded",
                                            "Cookie": "massing",
                                            "Dpr": "0.9",
                                            "Origin": "https://www.instagram.com",
                                            "Referer": "https://www.instagram.com/{}/".format(TargetUsername),
                                            "Sec-Ch-Prefers-Color-Scheme": "light",
                                            "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                            "Sec-Ch-Ua-Mobile": "?0",
                                            "Sec-Ch-Ua-Model": """""",
                                            "Sec-Ch-Ua-Platform": """Windows""",
                                            "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                            "Sec-Fetch-Dest": "empty",
                                            "Sec-Fetch-Mode": "cors",
                                            "Sec-Fetch-Site": "same-origin",
                                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                            "Viewport-Width": "238",
                                            "X-Asbd-Id": "129477",
                                            "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                            "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                            "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                            "X-Ig-App-Id": "936619743392459"}
                                        data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{TargetUsername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                        response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                        if response.text.__contains__("id"):
                                            mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                            account.remove(
                                                f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                            if len(account) == 0:
                                                bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid),
                                                                    mess.message_id,parse_mode="HTML")
                                            else:
                                                sleep(1)
                                                bot.delete_message(int(Userid), mess.message_id)
                                        else:
                                            print(f"Banned : {TargetUsername}")
                                            bot.send_message(int(Userid), f"<b>Banned : {TargetUsername}</b>",parse_mode="HTML")

                            sleep(sleepnumber)
                    if Drugs == True:
                            if MessageNow == "Stop":
                                if ChatIDNow == Userid:
                                    print("[+] Stop Report Profile : {}".format(Userid))
                                    bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                    break
                            else:
                                for AccountInfo in account:
                                    AccountInfo = str(AccountInfo)
                                    TOKEN = AccountInfo.split("|")[0]
                                    CLAIM_TOKEN = AccountInfo.split("|")[1]
                                    ANDROID_ID = AccountInfo.split("|")[2]
                                    UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                    MID = AccountInfo.split("|")[4]
                                    USER_ID = AccountInfo.split("|")[5]
                                    FAMILY_ID = AccountInfo.split("|")[6]
                                    shopping_session_id = AccountInfo.split("|")[7]
                                    ixt_initial_screen_id = AccountInfo.split("|")[8]
                                    trigger_session_id = AccountInfo.split("|")[9]
                                    UsernameNow = AccountInfo.split('|')[10]
                                    try:
                                        url = "https://www.instagram.com/api/v1/web/reports/get_frx_prompt/"
                                        hea = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(TargetUsername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                        data1 = {
                                            'entry_point':'1',
                                            'location':'2',
                                            'object_type':'5',
                                            'object_id':TargetID,
                                            'container_module':'profilePage',
                                            'frx_prompt_request_type':'1'}
                                        req1  = requests.post(url=url,headers=hea,data=data1)
                                        context1 = req1.json()['response']['context']
                                        data2 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context1,
                                                'selected_tag_types':'["ig_report_account"]',
                                                'frx_prompt_request_type':'2',
                                            }
                                        req2  = requests.post(url=url,headers=hea,data=data2)
                                        context2 = req2.json()['response']['context']
                                        data3 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context2,
                                                'selected_tag_types':'["ig_its_inappropriate"]',
                                                'frx_prompt_request_type':'2',
                                            }
                                        req3  = requests.post(url=url,headers=hea,data=data3)
                                        context3= req3.json()['response']['context']
                                        data4 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context3,
                                                'selected_tag_types': '["ig_sale_of_illegal_or_regulated_goods_v3"]',
                                                'frx_prompt_request_type':'2'
                                            }
                                        req4  = requests.post(url=url,headers=hea,data=data4)
                                        context4= req4.json()['response']['context']
                                        data5 = {
                                                'entry_point':'1',
                                                'location':'2',
                                                'object_type':'5',
                                                'object_id':TargetID,
                                                'container_module':'profilePage',
                                                'context':context4,
                                                'selected_tag_types': '["ig_drugs_v3"]',
                                                'action_type': '2',
                                                'frx_prompt_request_type':'2'
                                            }
                                        req5  = requests.post(url=url,headers=hea,data=data5)
                                        if req5.json()["status"] == "ok" in req5.text:
                                            Done+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Drugs</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                        else:
                                            Error+=1
                                            bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nTarget : @{TargetUsername}\nMode : Drugs</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    except:
                                        headers = {
                                            "Accept": "*/*",
                                            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                            "Content-Type": "application/x-www-form-urlencoded",
                                            "Cookie": "massing",
                                            "Dpr": "0.9",
                                            "Origin": "https://www.instagram.com",
                                            "Referer": "https://www.instagram.com/{}/".format(TargetUsername),
                                            "Sec-Ch-Prefers-Color-Scheme": "light",
                                            "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                            "Sec-Ch-Ua-Mobile": "?0",
                                            "Sec-Ch-Ua-Model": """""",
                                            "Sec-Ch-Ua-Platform": """Windows""",
                                            "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                            "Sec-Fetch-Dest": "empty",
                                            "Sec-Fetch-Mode": "cors",
                                            "Sec-Fetch-Site": "same-origin",
                                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                            "Viewport-Width": "238",
                                            "X-Asbd-Id": "129477",
                                            "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                            "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                            "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                            "X-Ig-App-Id": "936619743392459"}
                                        data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{TargetUsername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                        response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                        if response.text.__contains__("id"):
                                            mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                            account.remove(
                                                f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                            if len(account) == 0:
                                                bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid),
                                                                    mess.message_id,parse_mode="HTML")
                                            else:
                                                sleep(1)
                                                bot.delete_message(int(Userid), mess.message_id)
                                        else:
                                            print(f"Banned : {TargetUsername}")
                                            bot.send_message(int(Userid), f"<b>Banned : {TargetUsername}</b>",parse_mode="HTML")
                            sleep(sleepnumber)
def ReportStory(Userid):
        global url,response
        print("[+] Start Report Story : {}".format(Userid))
        Done = 0
        Error = 0
        account = open(f"./Subscribers/{str(Userid)}/AccountsInfo.txt","r").read().splitlines()
        StoreisID = open(f"./Subscribers/{str(Userid)}/Stoires.txt",'r').read().splitlines()
        sleepnumber =  int(open(f"./Subscribers/{str(Userid)}/Sleep.txt","r").read().splitlines()[0])
        while 1:
            if MessageNow == "Stop":
                if ChatIDNow == Userid:
                    print("[+] Stop Report Story : {}".format(Userid))
                    bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                    break
            for List in StoreisID:
                StoryID = List.split(':')[0]
                Targetusername = List.split(':')[1]
                if Spam == True:
                        if MessageNow == "Stop":
                            if ChatIDNow == Userid:
                                print("[+] Stop Report Story : {}".format(Userid))
                                bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                break
                        else:
                            for AccountInfo in account:
                                AccountInfo = str(AccountInfo)
                                TOKEN = AccountInfo.split("|")[0]
                                CLAIM_TOKEN = AccountInfo.split("|")[1]
                                ANDROID_ID = AccountInfo.split("|")[2]
                                UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                MID = AccountInfo.split("|")[4]
                                USER_ID = AccountInfo.split("|")[5]
                                FAMILY_ID = AccountInfo.split("|")[6]
                                shopping_session_id = AccountInfo.split("|")[7]
                                ixt_initial_screen_id = AccountInfo.split("|")[8]
                                trigger_session_id = AccountInfo.split("|")[9]
                                UsernameNow = AccountInfo.split('|')[10]
                                try:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                    url = "https://www.instagram.com/api/v1/web/reports/get_frx_prompt/"
                                    datas = {
                                            "entry_point": "1",
                                            'location': '4',
                                            'object_type': '1',
                                            'object_id': StoryID,
                                            'container_module': 'StoriesPage',
                                            'frx_prompt_request_type': '1'
                                        }
                                    request = requests.post(url,headers=headers,data=datas).json()
                                    context = request["response"]["context"]
                                    spamdata = {
                                            "entry_point": "1",
                                            "location": "4",
                                            "object_type": "1",
                                            "object_id": StoryID,
                                            "container_module": "StoriesPage",
                                            "context": context,
                                            "selected_tag_types": '["ig_spam_v3"]',
                                            'frx_prompt_request_type': '2'
                                        }
                                    reque = requests.post(url,headers=headers,data=spamdata).json()
                                    if 'Done' in reque["response"]["done_button_label"]["text"]:
                                        Done+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Spam</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    else:
                                        Error+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Spam</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                except:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": "massing",
                                        "Dpr": "0.9",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}/".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                        "Sec-Ch-Ua-Mobile": "?0",
                                        "Sec-Ch-Ua-Model": """""",
                                        "Sec-Ch-Ua-Platform": """Windows""",
                                        "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                        "Viewport-Width": "238",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                        "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                        "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                        "X-Ig-App-Id": "936619743392459"}
                                    data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{Targetusername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                    response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                    if response.text.__contains__("id"):
                                        mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                        account.remove(
                                            f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                        if len(account) == 0:
                                            bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid), mess.message_id,parse_mode="HTML")
                                        else:
                                            sleep(1)
                                            bot.delete_message(int(Userid), mess.message_id)
                                    else:
                                        print(f"Banned : {Targetusername}")
                                        bot.send_message(int(Userid), f"<b>Banned : @{Targetusername}</b>",parse_mode="HTML")
                        sleep(sleepnumber)
                if Self == True:
                        if MessageNow == "Stop":
                            if ChatIDNow == Userid:
                                print("[+] Stop Report Story : {}".format(Userid))
                                bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                break
                        else:
                            for AccountInfo in account:
                                AccountInfo = str(AccountInfo)
                                TOKEN = AccountInfo.split("|")[0]
                                CLAIM_TOKEN = AccountInfo.split("|")[1]
                                ANDROID_ID = AccountInfo.split("|")[2]
                                UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                MID = AccountInfo.split("|")[4]
                                USER_ID = AccountInfo.split("|")[5]
                                FAMILY_ID = AccountInfo.split("|")[6]
                                shopping_session_id = AccountInfo.split("|")[7]
                                ixt_initial_screen_id = AccountInfo.split("|")[8]
                                trigger_session_id = AccountInfo.split("|")[9]
                                UsernameNow = AccountInfo.split('|')[10]
                                try:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                    datas = {
                                            "entry_point": "1",
                                            'location': '4',
                                            'object_type': '1',
                                            'object_id': StoryID,
                                            'container_module': 'StoriesPage',
                                            'frx_prompt_request_type': '1'
                                        }
                                    request = requests.post(url,headers=headers,data=datas).json()
                                    context = request["response"]["context"]
                                    datae = {
                                            "entry_point": "1",
                                            "location": "4",
                                            "object_type": "1",
                                            "object_id": StoryID,
                                            "container_module": "StoriesPage",
                                            "context": context,
                                            "selected_tag_types": '["ig_self_injury_v3"]',
                                            "frx_prompt_request_type": '2'
                                        }
                                    response1 = requests.post(url,headers=headers,data=datae).json()
                                    real = response1["response"]["context"]
                                    dataq = {
                                            "entry_point": "1",
                                            "location": "4",
                                            "object_type": "1",
                                            "object_id": StoryID,
                                            "container_module": "StoriesPage",
                                            "context": real,
                                            "action_type": "2",
                                            "frx_prompt_request_type": "4"
                                    }
                                    res = requests.post(url,headers=headers,data=dataq).json()
                                    if 'Done' in res["response"]["done_button_label"]["text"]:
                                        Done+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Self</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    else:
                                        Error+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Self</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                except:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": "massing",
                                        "Dpr": "0.9",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}/".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                        "Sec-Ch-Ua-Mobile": "?0",
                                        "Sec-Ch-Ua-Model": """""",
                                        "Sec-Ch-Ua-Platform": """Windows""",
                                        "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                        "Viewport-Width": "238",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                        "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                        "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                        "X-Ig-App-Id": "936619743392459"}
                                    data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{Targetusername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                    response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                    if response.text.__contains__("id"):
                                        mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                        account.remove(
                                            f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                        if len(account) == 0:
                                            bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid), mess.message_id,parse_mode="HTML")
                                        else:
                                            sleep(1)
                                            bot.delete_message(int(Userid), mess.message_id)
                                    else:
                                        print(f"Banned : {Targetusername}")
                                        bot.send_message(int(Userid), f"<b>Banned : @{Targetusername}</b>",parse_mode="HTML")
                        sleep(sleepnumber)
                if Hate == True:
                        if MessageNow == "Stop":
                            if ChatIDNow == Userid:
                                print("[+] Stop Report Story : {}".format(Userid))
                                bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                break
                        else:
                            for AccountInfo in account:
                                AccountInfo = str(AccountInfo)
                                TOKEN = AccountInfo.split("|")[0]
                                CLAIM_TOKEN = AccountInfo.split("|")[1]
                                ANDROID_ID = AccountInfo.split("|")[2]
                                UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                MID = AccountInfo.split("|")[4]
                                USER_ID = AccountInfo.split("|")[5]
                                FAMILY_ID = AccountInfo.split("|")[6]
                                shopping_session_id = AccountInfo.split("|")[7]
                                ixt_initial_screen_id = AccountInfo.split("|")[8]
                                trigger_session_id = AccountInfo.split("|")[9]
                                UsernameNow = AccountInfo.split('|')[10]
                                try:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                    datas = {
                                            "entry_point": "1",
                                            'location': '4',
                                            'object_type': '1',
                                            'object_id': StoryID,
                                            'container_module': 'StoriesPage',
                                            'frx_prompt_request_type': '1'
                                        }
                                    request = requests.post(url,headers=headers,data=datas).json()
                                    context = request["response"]["context"]
                                    datapushup = {
                                            "entry_point": "1",
                                            "location": "4",
                                            "object_type": "1",
                                            "object_id": StoryID,
                                            "container_module": "StoriesPage",
                                            "context": context,
                                            'selected_tag_types': '["ig_hate_speech_v3"]',
                                            'frx_prompt_request_type': '2'
                                        }
                                    req = requests.post(url,headers=headers,data=datapushup).json()
                                    real_context = req["response"]["context"]
                                    data  = {
                                            'entry_point': '1',
                                            'location': '4',
                                            'object_type': '1',
                                            'object_id': StoryID,
                                            'container_module': 'StoriesPage',
                                            'context': real_context,
                                            'action_type': '2',
                                            'frx_prompt_request_type': '4'
                                    }
                                    response = requests.post(url,headers=headers,data=data).json()
                                    if 'Done' in response["response"]["done_button_label"]["text"]:
                                        Done+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Hate</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    else:
                                        Error+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Hate</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                except:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": "massing",
                                        "Dpr": "0.9",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}/".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                        "Sec-Ch-Ua-Mobile": "?0",
                                        "Sec-Ch-Ua-Model": """""",
                                        "Sec-Ch-Ua-Platform": """Windows""",
                                        "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                        "Viewport-Width": "238",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                        "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                        "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                        "X-Ig-App-Id": "936619743392459"}
                                    data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{Targetusername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                    response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                    if response.text.__contains__("id"):
                                        mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                        account.remove(
                                            f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                        if len(account) == 0:
                                            bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid), mess.message_id,parse_mode="HTML")
                                        else:
                                            sleep(1)
                                            bot.delete_message(int(Userid), mess.message_id)
                                    else:
                                        print(f"Banned : {Targetusername}")
                                        bot.send_message(int(Userid), f"<b>Banned : @{Targetusername}</b>",parse_mode="HTML")
                        sleep(sleepnumber)
                if Violence == True:
                        if MessageNow == "Stop":
                            if ChatIDNow == Userid:
                                print("[+] Stop Report Story : {}".format(Userid))
                                bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                break
                        else:
                            for AccountInfo in account:
                                AccountInfo = str(AccountInfo)
                                TOKEN = AccountInfo.split("|")[0]
                                CLAIM_TOKEN = AccountInfo.split("|")[1]
                                ANDROID_ID = AccountInfo.split("|")[2]
                                UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                MID = AccountInfo.split("|")[4]
                                USER_ID = AccountInfo.split("|")[5]
                                FAMILY_ID = AccountInfo.split("|")[6]
                                shopping_session_id = AccountInfo.split("|")[7]
                                ixt_initial_screen_id = AccountInfo.split("|")[8]
                                trigger_session_id = AccountInfo.split("|")[9]
                                UsernameNow = AccountInfo.split('|')[10]
                                try:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                    datas = {
                                            "entry_point": "1",
                                            'location': '4',
                                            'object_type': '1',
                                            'object_id': StoryID,
                                            'container_module': 'StoriesPage',
                                            'frx_prompt_request_type': '1'
                                        }
                                    request = requests.post(url,headers=headers,data=datas).json()
                                    context = request["response"]["context"]
                                    datab = {
                                            "entry_point": '1',
                                            "location": '4',
                                            "object_type": '1',
                                            "object_id": StoryID,
                                            "container_module": "StoriesPage",
                                            "context": context,
                                            "selected_tag_types": '["ig_violence_parent"]',
                                            "frx_prompt_request_type": "2"
                                        }
                                    respone = requests.post(url,headers=headers,data=datab).json()
                                    real_context = respone["response"]["context"]
                                    datac = {
                                            "entry_point": '1',
                                            'location': '4',
                                            'object_type': '1',
                                            'object_id': StoryID,
                                            'container_module': 'StoriesPage',
                                            'context': real_context,
                                            'selected_tag_types': '["ig_violence_threat"]',
                                            'action_type': '2',
                                            'frx_prompt_request_type': '2'
                                        }
                                    respone2 = requests.post(url,headers=headers,data=datac).json()
                                    if 'Done' in respone2["response"]["done_button_label"]["text"]:
                                        Done+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Violence</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    else:
                                        Error+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Violence</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                except:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": "massing",
                                        "Dpr": "0.9",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}/".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                        "Sec-Ch-Ua-Mobile": "?0",
                                        "Sec-Ch-Ua-Model": """""",
                                        "Sec-Ch-Ua-Platform": """Windows""",
                                        "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                        "Viewport-Width": "238",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                        "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                        "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                        "X-Ig-App-Id": "936619743392459"}
                                    data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{Targetusername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                    response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                    if response.text.__contains__("id"):
                                        mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                        account.remove(
                                            f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                        if len(account) == 0:
                                            bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid), mess.message_id,parse_mode="HTML")
                                        else:
                                            sleep(1)
                                            bot.delete_message(int(Userid), mess.message_id)
                                    else:
                                        print(f"Banned : {Targetusername}")
                                        bot.send_message(int(Userid), f"<b>Banned : @{Targetusername}</b>",parse_mode="HTML")
                        sleep(sleepnumber)
                if Nudity == True:
                        if MessageNow == "Stop":
                            if ChatIDNow == Userid:
                                print("[+] Stop Report Story : {}".format(Userid))
                                bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                break
                        else:
                            for AccountInfo in account:
                                AccountInfo = str(AccountInfo)
                                TOKEN = AccountInfo.split("|")[0]
                                CLAIM_TOKEN = AccountInfo.split("|")[1]
                                ANDROID_ID = AccountInfo.split("|")[2]
                                UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                MID = AccountInfo.split("|")[4]
                                USER_ID = AccountInfo.split("|")[5]
                                FAMILY_ID = AccountInfo.split("|")[6]
                                shopping_session_id = AccountInfo.split("|")[7]
                                ixt_initial_screen_id = AccountInfo.split("|")[8]
                                trigger_session_id = AccountInfo.split("|")[9]
                                UsernameNow = AccountInfo.split('|')[10]
                                try:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                    datas = {
                                            "entry_point": "1",
                                            'location': '4',
                                            'object_type': '1',
                                            'object_id': StoryID,
                                            'container_module': 'StoriesPage',
                                            'frx_prompt_request_type': '1'
                                    }
                                    request = requests.post(url,headers=headers,data=datas).json()
                                    context = request["response"]["context"]
                                    real_data = {
                                            "entry_point": "1",
                                            'location': '4',
                                            'object_type': '1',
                                            'object_id': StoryID,
                                            'container_module': 'StoriesPage',
                                            'context': context,
                                            'selected_tag_types': '["ig_nudity_v2"]',
                                            'frx_prompt_request_type': '2'
                                    }
                                    accept = requests.post(url,headers=headers,data=real_data).json()
                                    real = accept["response"]["context"]
                                    dataa = {
                                            "entry_point": "1",
                                            'location': '4',
                                            'object_type': '1',
                                            'object_id': StoryID,
                                            'container_module': 'StoriesPage',
                                            'context': real,
                                            'selected_tag_types': '["ig_nudity_or_pornography_v3"]',
                                            'action_type': '2',
                                            'frx_prompt_request_type': '2'
                                        }
                                    response = requests.post(url,headers=headers,data=dataa).json()
                                    if 'Done' in response["response"]["done_button_label"]["text"]:
                                        Done+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Nudity</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    else:
                                        Error+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Nudity</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                except:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": "massing",
                                        "Dpr": "0.9",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}/".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                        "Sec-Ch-Ua-Mobile": "?0",
                                        "Sec-Ch-Ua-Model": """""",
                                        "Sec-Ch-Ua-Platform": """Windows""",
                                        "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                        "Viewport-Width": "238",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                        "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                        "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                        "X-Ig-App-Id": "936619743392459"}
                                    data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{Targetusername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                    response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                    if response.text.__contains__("id"):
                                        mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                        account.remove(
                                            f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                        if len(account) == 0:
                                            bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid), mess.message_id,parse_mode="HTML")
                                        else:
                                            sleep(1)
                                            bot.delete_message(int(Userid), mess.message_id)
                                    else:
                                        print(f"Banned : {Targetusername}")
                                        bot.send_message(int(Userid), f"<b>Banned : @{Targetusername}</b>",parse_mode="HTML")
                        sleep(sleepnumber)
                if Bullying == True:
                        if MessageNow == "Stop":
                            if ChatIDNow == Userid:
                                print("[+] Stop Report Story : {}".format(Userid))
                                bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                break
                        else:
                            for AccountInfo in account:
                                AccountInfo = str(AccountInfo)
                                TOKEN = AccountInfo.split("|")[0]
                                CLAIM_TOKEN = AccountInfo.split("|")[1]
                                ANDROID_ID = AccountInfo.split("|")[2]
                                UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                MID = AccountInfo.split("|")[4]
                                USER_ID = AccountInfo.split("|")[5]
                                FAMILY_ID = AccountInfo.split("|")[6]
                                shopping_session_id = AccountInfo.split("|")[7]
                                ixt_initial_screen_id = AccountInfo.split("|")[8]
                                trigger_session_id = AccountInfo.split("|")[9]
                                UsernameNow = AccountInfo.split('|')[10]
                                try:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                    datas = {
                                            "entry_point": "1",
                                            'location': '4',
                                            'object_type': '1',
                                            'object_id': StoryID,
                                            'container_module': 'StoriesPage',
                                            'frx_prompt_request_type': '1'
                                        }
                                    request = requests.post(url,headers=headers,data=datas).json()
                                    context = request["response"]["context"]
                                    dataa = {
                                            "entry_point": '1',
                                            "location": '4',
                                            "object_type": '1',
                                            "object_id": StoryID,
                                            "container_module": "StoriesPage",
                                            "context": context,
                                            "selected_tag_types": '["ig_bullying_or_harassment_comment_v3"]',
                                            "frx_prompt_request_type": "2"
                                        }
                                    get_real = requests.post(url,headers=headers,data=dataa).json()
                                    real_context = get_real["response"]["context"]
                                    datab = {
                                            "entry_point": "1",
                                            "location": "4",
                                            "object_type": "1",
                                            "object_id": StoryID,
                                            "container_module": "StoriesPage",
                                            "context": real_context,
                                            "selected_tag_types": '["ig_bullying_or_harassment_me_v3"]',
                                            'frx_prompt_request_type': '2'
                                        }
                                    acce = requests.post(url,headers=headers,data=datab).json()
                                    get_final = acce["response"]["context"]
                                    datac = {       
                                            "entry_point": '1',
                                            "location": '4',
                                            "object_type": '1',
                                            "object_id": StoryID,
                                            "container_module": 'StoriesPage',
                                            "context": get_final,
                                            "action_type": '2',
                                            "frx_prompt_request_type": '4'
                                    }
                                    finaly = requests.post(url,headers=headers,data=datac).json()
                                    if 'Done' in finaly["response"]["done_button_label"]["text"]:
                                        Done+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Bullying</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    else:
                                        Error+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Bullying</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                except:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": "massing",
                                        "Dpr": "0.9",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}/".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                        "Sec-Ch-Ua-Mobile": "?0",
                                        "Sec-Ch-Ua-Model": """""",
                                        "Sec-Ch-Ua-Platform": """Windows""",
                                        "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                        "Viewport-Width": "238",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                        "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                        "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                        "X-Ig-App-Id": "936619743392459"}
                                    data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{Targetusername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                    response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                    if response.text.__contains__("id"):
                                        mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                        account.remove(
                                            f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                        if len(account) == 0:
                                            bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid), mess.message_id,parse_mode="HTML")
                                        else:
                                            sleep(1)
                                            bot.delete_message(int(Userid), mess.message_id)
                                    else:
                                        print(f"Banned : {Targetusername}")
                                        bot.send_message(int(Userid), f"<b>Banned : @{Targetusername}</b>",parse_mode="HTML")
                        sleep(sleepnumber)
                if Drugs == True:
                        if MessageNow == "Stop":
                            if ChatIDNow == Userid:
                                print("[+] Stop Report Story : {}".format(Userid))
                                bot.send_message(int(Userid),"<b>Done Stopped Bot!</b>",parse_mode="HTML")
                                break
                        else:
                            for AccountInfo in account:
                                AccountInfo = str(AccountInfo)
                                TOKEN = AccountInfo.split("|")[0]
                                CLAIM_TOKEN = AccountInfo.split("|")[1]
                                ANDROID_ID = AccountInfo.split("|")[2]
                                UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
                                MID = AccountInfo.split("|")[4]
                                USER_ID = AccountInfo.split("|")[5]
                                FAMILY_ID = AccountInfo.split("|")[6]
                                shopping_session_id = AccountInfo.split("|")[7]
                                ixt_initial_screen_id = AccountInfo.split("|")[8]
                                trigger_session_id = AccountInfo.split("|")[9]
                                UsernameNow = AccountInfo.split('|')[10]
                                try:
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": f"sessionid={TOKEN}",
                                        "Dpr": "2",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                                        "Viewport-Width": "414",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "uUZL4WYzot87gg3to79QKhPiUsjDn3j3",
                                        "X-Ig-App-Id": "1217981644879628",
                                        "X-Ig-Www-Claim": CLAIM_TOKEN,
                                        "X-Instagram-Ajax": "1011351817",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }
                                    datas = {
                                            "entry_point": "1",
                                            'location': '4',
                                            'object_type': '1',
                                            'object_id': StoryID,
                                            'container_module': 'StoriesPage',
                                            'frx_prompt_request_type': '1'
                                        }
                                    request = requests.post(url,headers=headers,data=datas).json()
                                    context = request["response"]["context"]
                                    datab = {
                                            "entry_point": '1',
                                            "location": '4',
                                            "object_type": '1',
                                            "object_id": StoryID,
                                            "container_module": "StoriesPage",
                                            "context": context,
                                            "selected_tag_types": '["ig_sale_of_illegal_or_regulated_goods_v3"]',
                                            "frx_prompt_request_type": "2"
                                        }
                                    resposne23 = requests.post(url,headers=headers,data=datab).json()
                                    real = resposne23["response"]["context"]
                                    datae = {
                                            "entry_point": '1',
                                            "location": '4',
                                            "object_type": '1',
                                            "object_id": StoryID,
                                            "container_module": 'StoriesPage',
                                            "context": real,
                                            "selected_tag_types": '["ig_drugs_alcohol_tobacco"]',
                                            "action_type": '2',
                                            "frx_prompt_request_type": '2'
                                        }
                                    res = requests.post(url,headers=headers,data=datae).json()
                                    if 'Done' in res["response"]["done_button_label"]["text"]:
                                        Done+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Drugs</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                    else:
                                        Error+=1
                                        bot.edit_message_text(f"<b>Done : {Done} / Error : {Error}\nMode : Drugs</b>",int(Userid),editme.message_id,parse_mode="HTML")
                                except Exception as gg:
                                    print(gg)
                                    headers = {
                                        "Accept": "*/*",
                                        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                                        "Content-Type": "application/x-www-form-urlencoded",
                                        "Cookie": "massing",
                                        "Dpr": "0.9",
                                        "Origin": "https://www.instagram.com",
                                        "Referer": "https://www.instagram.com/{}/".format(Targetusername),
                                        "Sec-Ch-Prefers-Color-Scheme": "light",
                                        "Sec-Ch-Ua": """Not_A Brand"";v=""8"", ""Chromium"";v=""120"", ""Google Chrome"";v=""120""",
                                        "Sec-Ch-Ua-Mobile": "?0",
                                        "Sec-Ch-Ua-Model": """""",
                                        "Sec-Ch-Ua-Platform": """Windows""",
                                        "Sec-Ch-Ua-Platform-Version": """10.0.0""",
                                        "Sec-Fetch-Dest": "empty",
                                        "Sec-Fetch-Mode": "cors",
                                        "Sec-Fetch-Site": "same-origin",
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                                        "Viewport-Width": "238",
                                        "X-Asbd-Id": "129477",
                                        "X-Csrftoken": "dr120O7qrtRWYqNpve1ZKZMUUvabvmwX",
                                        "X-Fb-Friendly-Name": "PolarisBarcelonaProfileBadgeQuery",
                                        "X-Fb-Lsd": "8zU6-6taj5nvCF19VJuRmo",
                                        "X-Ig-App-Id": "936619743392459"}
                                    data = f'av=17841464245050085&__d=www&__user=0&__a=1&__req=3&__hs=19748.HYP%3Ainstagram_web_pkg.2.1..0.1&dpr=1&__ccg=UNKNOWN&__rev=1011051482&__s=wlmtlh%3Axkto79%3Az658jf&__hsi=7328560169802750276&__dyn=7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2sx-0z8-U2zxe2GewGwso88cobEaU2eUlwhEe87q7U88138bpEbUGdG1QwTwFwIw8O321LwTwKG1pg661pwr86C1mwrd6goK68jxeUnAw&__csr=gkML4vcLN2mBRpyqCSmQBBQozihkCbGlV9LAAy9aA8KVVEkzkqeh4F99VEiEECRgJ2pbBiExbhdfKEC4bhryVVdmGAKF8gyk8yqDDCXBBDwHJ0zx26801bSi029k02YS064o2l4iezzk09sCw2P-1te3a226Eb80xl0Hc0_816yw9-00FIE&__comet_req=7&fb_dtsg=NAcOTRjvM-fXT1VlxZ6oSOgcLDQj-48bLcaTuf9bxw8zdjeIHvAsRMA%3A17843691127146670%3A1706313365&jazoest=26312&lsd=8zU6-6taj5nvCF19VJuRmo&__spin_r=1011051482&__spin_b=trunk&__spin_t=1706313381&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisBarcelonaProfileBadgeQuery&variables=%7B%22username%22%3A%22{Targetusername}%22%7D&server_timestamps=true&doc_id=6887760227926196'
                                    response = post("https://www.instagram.com/api/graphql", headers=headers, data=data)
                                    if response.text.__contains__("id"):
                                        mess = bot.send_message(int(Userid), f"<b>New Status >> {UsernameNow} Session Burned!</b>",parse_mode="HTML")
                                        account.remove(
                                            f"{TOKEN}|{CLAIM_TOKEN}|{ANDROID_ID}|{UUID_OR_DEVICE_ID}|{MID}|{USER_ID}|{FAMILY_ID}|{shopping_session_id}|{ixt_initial_screen_id}|{trigger_session_id}|{UsernameNow}")
                                        if len(account) == 0:
                                            bot.edit_message_text("<b>All Sessions Was Burned!</b>", int(Userid), mess.message_id,parse_mode="HTML")
                                        else:
                                            sleep(1)
                                            bot.delete_message(int(Userid), mess.message_id)
                                    else:
                                        print(f"Banned : {Targetusername}")
                                        bot.send_message(int(Userid), f"<b>Banned : @{Targetusername}</b>",parse_mode="HTML")
                        sleep(sleepnumber)
def SaveTargets(message):
    global editme
    v = open(f"./Subscribers/{str(message.chat.id)}/Targets.txt","w").write("")
    if message.content_type == "text":
        newpath = str(message.text).splitlines()
        for account in newpath:    
            open(f"./Subscribers/{str(message.chat.id)}/Targets.txt","a").write(f"{account}\n")
    elif message.content_type == "document":
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"./Subscribers/{str(message.chat.id)}/Targets.txt", 'wb') as new_file:
            new_file.write(downloaded_file)
    targets = open(f"./Subscribers/{str(message.chat.id)}/Targets.txt","r").read().splitlines()
    filter = []
    Counter = int(open(f"./Subscribers/{str(message.chat.id)}/Counter.txt","r").read().splitlines()[0])
    WhiteList = open("whitelist.txt",'r').read().split()
    for m in targets:
        if WhiteList.__contains__(m):
            filter.append(m)

    if len(filter) > 0:
        if Counter == 1:
            bot.send_message(message.chat.id,"<b>Good Bye Ya F7l!</b>",parse_mode="HTML")
            user_id = str(message.chat.id)
            try:
                folder_to_delete = './Subscribers/{}'.format(user_id)
                delete_folder(folder_to_delete)
                ff = open("Subscribers.txt", 'r').read().splitlines()
                open("Subscribers.txt", 'w').write('')
                ff.remove(user_id)
                for m in ff:
                    open("Subscribers.txt", 'a').write(f"{m}\n")
                bot.send_message(int(ADMINID), "<b>Done Remove , Because He Broke The Laws : {}</b>".format(user_id),parse_mode="HTML")
            except Exception as f:
                print(f)
                bot.send_message(int(ADMINID), "<b>Not Found : {}</b>".format(user_id),parse_mode="HTML")
        elif Counter == 0:
            open(f"./Subscribers/{str(message.chat.id)}/Counter.txt","w").write('1')
            bot.send_message(message.chat.id,"<b>You Have 1 warning!</b>",parse_mode="HTML")
    else:
        open(f"./Subscribers/{str(message.chat.id)}/Targets.txt","w").write("")
        editme = bot.send_message(message.chat.id,"<b>Start Checking!</b>",parse_mode="HTML")
        sleep(1.5)
        ex = 0
        listlenth = len(targets)
        for targ in targets:
            Accounts = open(f"./Subscribers/{str(message.chat.id)}/AccountsInfo.txt","r").read().splitlines()
            AccountInfo = str(choice(Accounts))
            TOKEN = AccountInfo.split("|")[0]
            CLAIM_TOKEN = AccountInfo.split("|")[1]
            ANDROID_ID = AccountInfo.split("|")[2]
            UUID_OR_DEVICE_ID = AccountInfo.split("|")[3]
            MID = AccountInfo.split("|")[4]
            USER_ID = AccountInfo.split("|")[5]
            FAMILY_ID = AccountInfo.split("|")[6]
            shopping_session_id = AccountInfo.split("|")[7]
            ixt_initial_screen_id = AccountInfo.split("|")[8]
            trigger_session_id = AccountInfo.split("|")[9]
            UsernameNow = AccountInfo.split('|')[10]
            headers = {
                "User-Agent": "Instagram 177.0.0.30.119 Android (21/5.0.2; 240dpi; 540x960; samsung; SM-G530H; fortunave3g; qcom; en_GB; 276028020)",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Language": "en-US,en;q=0.9",
                "Cookie":f"sessionid={TOKEN}"
            }
            response = get(f"https://i.instagram.com/api/v1/users/web_profile_info/?username={targ}",headers=headers)
            if response.text.__contains__("data"):
                try:
                    user_id = response.json()["data"]["user"]["id"]
                    timestart = str(datetime.now())
                    open(f"MonitorList.txt","a").write(f"{targ}:{str(message.chat.id)}\n")
                    open(f"./Monitor/{targ}.txt","w").write(f"{targ}\n{timestart}")
                    ex+=1
                    open(f"./Subscribers/{str(message.chat.id)}/Targets.txt","a").write(f"{targ}:{user_id}\n")
                    bot.edit_message_text("<b>User Found: @{}</b>".format(targ),editme.chat.id,editme.message_id,parse_mode="HTML")
                except:
                    bot.edit_message_text("<b>User Not Found : @{}</b>".format(targ), editme.chat.id, editme.message_id,
                                          parse_mode="HTML")
            else:
                bot.edit_message_text("<b>User Not Found : @{}</b>".format(targ),editme.chat.id,editme.message_id,parse_mode="HTML")
        bot.edit_message_text(f"<b>Checking Finish , Found {ex}/{listlenth}</b>",editme.chat.id,editme.message_id,parse_mode="HTML")
        TARGETS_LIST_LENTH = len(open(f"./Subscribers/{str(message.chat.id)}/Targets.txt","r").read().splitlines())
        AccountsLenth = len(open(f"./Subscribers/{str(message.chat.id)}/AccountsInfo.txt","r").read().splitlines())
        if TARGETS_LIST_LENTH == 0:
            bot.edit_message_text(f"<b>Bro No Good Target!</b>", editme.chat.id, editme.message_id, parse_mode="HTML")
            sleep(2)
            bot.edit_message_text(f"<b>Give Me Your Targets [Accept File] ?</b>", editme.chat.id, editme.message_id, parse_mode="HTML")
            bot.register_next_step_handler_by_chat_id(message.chat.id,SaveTargets)
        else:
            bot.edit_message_text(f"<b>Enter Sleep [ 0 = Defult Sleep ] ? ?</b>", editme.chat.id, editme.message_id, parse_mode="HTML")
            bot.register_next_step_handler_by_chat_id(message.chat.id,SaveSleep)
def SaveSleep(message):
    global editme
    sleepnum = str(message.text)
    try:
        tryconvertsleep = int(sleepnum)
        if tryconvertsleep == 0:
            sleepnum = "6"
        open(f"./Subscribers/{str(message.chat.id)}/Sleep.txt","w").write(sleepnum)
        TARGETS_LIST_LENTH = len(open(f"./Subscribers/{str(message.chat.id)}/Targets.txt","r").read().splitlines())
        AccountsLenth = len(open(f"./Subscribers/{str(message.chat.id)}/AccountsInfo.txt","r").read().splitlines())
        inlines = types.InlineKeyboardMarkup(row_width=2)
        profile = types.InlineKeyboardButton("profile", callback_data="profilemode")
        story = types.InlineKeyboardButton("Story", callback_data="storymode")
        hilights = types.InlineKeyboardButton("Highlights", callback_data="hilightmode")
        inlines.row(profile, story, hilights)
        editme = bot.send_message(message.chat.id,f"<b>You Have {str(AccountsLenth)} Good Account & {TARGETS_LIST_LENTH} Target/s & Sleep = {sleepnum}, Now Choice Report Mode ?</b>",reply_markup=inlines,parse_mode="HTML")
    except:
        bot.edit_message_text(f"<b>Bro , Give Me Only Numbers ? </b>", editme.chat.id, editme.message_id, parse_mode="HTML")
        sleep(1)
        bot.register_next_step_handler_by_chat_id(message.chat.id,SaveSleep)
def SaveWebhook(message):
    webhook = str(message.text)
    open(f"./Subscribers/{str(message.chat.id)}/webhook.txt","w").write(f"{webhook}")
    bot.send_message(message.chat.id,"<b>Updated</b>",parse_mode="HTML")
def SaveName(message):
    newname = str(message.text)
    open(f"./Subscribers/{str(message.chat.id)}/name.txt","w").write(newname)
    bot.send_message(message.chat.id, "<b>Updated</b>", parse_mode="HTML")
def SaveMonUser(message):
    user = str(message.text)
    open("MonitorList.txt","a").write(f"{user}\n")
    time = datetime.now()
    open(f"./monitor/{user}.txt","w").write(f"{user}\n{time}")
    bot.send_message(message.chat.id,"<b>Done Added!</b>",parse_mode="HTML")
def NextStepPromoCode(message):
    PromoCode = str(message.text)
    code = PromoCode.split(":")[0];count = PromoCode.split(":")[1];maxcust = PromoCode.split(":")[2];spot_type = PromoCode.split(":")[3]
    with open(f"./PromoCodes/{code}.json","w") as g:
        dump({"maxcount":f"{maxcust}","count":f"{count}","type":f"{spot_type}","ids":[]},g)
    bot.send_message(message.chat.id,"<b>Done Add PromoCode!</b>",parse_mode="HTML")



bot.polling(non_stop=True)
