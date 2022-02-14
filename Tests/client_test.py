from ast import Await
import os
import aiohttp
from aiohttp import web

from aries_staticagent import Connection, utils, Message, Target

from common import config

def main():
    keys, target, args = config()
    conn = Connection(keys, target)
    
    m = Message.parse_obj({
            "@type": "https://didcomm.org/basicmessage/1.0/message",
            "~l10n": {"locale": "en"},
            "sent_time": utils.timestamp(),
            "content": "I am a Static client"
        })
    

    conn.send_and_await_reply(m)
    
    

if __name__ == "__main__":
    main()
