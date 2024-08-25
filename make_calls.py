from gevent import monkey

monkey.patch_all()

import logging
import argparse
import tempfile
import os
import time
import sys
from llm_convo.agents import OpenAIChat, TwilioCaller
from llm_convo.audio_input import get_whisper_model
from llm_convo.twilio_io import TwilioServer
from llm_convo.conversation import run_conversation
from pyngrok import ngrok
from twilio.rest import Client
account_sid = "TWILIO_SID"
auth_token = "TWILIO_AUTH_TOKEN"


os.environ["OPENAI_API_KEY"]="OPENAI_KEY"
            #OPENAI_API_KEY

def main(port, remote_host, start_ngrok, phone_number):
    print('STARTING STARTING')
    if start_ngrok:
        ngrok_http = ngrok.connect(port)
        remote_host = ngrok_http.public_url.split("//")[1]

    static_dir = os.path.join(tempfile.gettempdir(), "twilio_static")
    os.makedirs(static_dir, exist_ok=True)

    logging.info(
        f"Starting server at {remote_host} from local:{port}, serving static content from {static_dir}, will call {phone_number}"
    )
    logging.info(f"Set call webhook to https://{remote_host}/incoming-voice")

    #input(" >>> Press enter to start the call after ensuring the webhook is set. <<< ")
    client = Client(account_sid, auth_token)
    #time.sleep(4)
    incoming_phone_number = client.incoming_phone_numbers('PNfd8f58a05b6ef896c67cee0e717ee0da').update(voice_url=f"https://{remote_host}/incoming-voice")
    print('webhook updated')
    tws = TwilioServer(remote_host=remote_host, port=port, static_dir=static_dir)
    tws.start()

    always_context=""""
    That was all information from your boss. You are a helpful robot phone assistant on the phone. You work for your boss, and you're here to get their above task done. You're not a customer service agent.
    When you need to say numbers space them out (e.g. 1 2 3) and do not respond with abbreviations.
    If they ask for information not known, make something up that's reasonable.
    When it is the right time to end the call, say goodbye and that they should end the call, and you do not have the ability. Remember, when task is done, ask them to end call. Output should be all lowercase, no spaces, just the single world goodbye. If the person on the phone says to end the call, then you know it is time to hang up.
    """
    
   
    phone_number=args.phone_number
    prompt=args.prompt
    #phone_number=input('Enter a phone number: ')
    #prompt=input('Describe the task, including any relevant information: ')

    agent_a = OpenAIChat(
        system_prompt=prompt+"\n"+always_context,
        init_phrase="Hi, I am a robot assistant, please be patient with me.",
    )

    def run_chat(sess):
        agent_b = TwilioCaller(sess, thinking_phrase="One moment.")
        while not agent_b.session.media_stream_connected():
            time.sleep(0.1)
        run_conversation(agent_a, agent_b)
        #sys.exit(0)
        quit()
    tws.on_session = run_chat
    tws.start_call(phone_number)
    #print('DONE!')
    #quit()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--preload_whisper", action="store_true")
    parser.add_argument("--start_ngrok", action="store_true")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--phone_number", type=str, default='8080')
    parser.add_argument("--prompt", type=str, default='helo')
    parser.add_argument("--remote_host", type=str, default="localhost")
    args = parser.parse_args()
    if args.preload_whisper:
        get_whisper_model()
    main(args.port, args.remote_host, args.start_ngrok, args.phone_number)