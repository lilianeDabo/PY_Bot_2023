
import random

def cues(message_content):
    list = ["hi", "bonjour"]
    for val in list:
        if val == message_content:
            return val

def returns():
    list = ["(っ◔◡◔)っ ♥ 𝙃𝙚𝙡𝙡𝙤 ♥", "＼ʕ •ᴥ•ʔ／ 𝙃𝙤𝙬 𝙖𝙧𝙚 𝙮𝙤𝙪 ? ♥ "]
    return list[random.randint(0,1)]