from llm_convo.agents import ChatAgent


def run_conversation(agent_a: ChatAgent, agent_b: ChatAgent):
    transcript = []

    custom_string = "The following is a conversation transcript. The first person to speak is the robot assistant."
    save_folder='/Users/zarifazher/Desktop/cool_projects/Blah/llm_convo/llm_convo/examples/history/'
    filename = save_folder+"history.txt"
    f=open(filename,'w')
    f.write(custom_string + "\n")
    f.close()
    added=[]
    #with open(filename, 'w') as file:
    while True:
        text_a = agent_a.get_response(transcript)
        transcript.append(text_a)
        print("->", text_a, transcript)
        if text_a=='goodbye':#end convo key
            print('CONVO ENDING!!!')
            break
        text_b = agent_b.get_response(transcript)
        transcript.append(text_b)
        print("->", text_b, transcript)

        for string in transcript:
            if string not in added:
                print('Writing',string)
                f=open(filename,'a')
                f.write(string + "\n")
                f.close()
                added.append(string)
            else:
                continue
