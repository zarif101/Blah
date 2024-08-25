import openai
import os

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"]="sk-DX1STMau-CZLq9pj-owP5dAHdRxO_M0wFTbxhLoZYDT3BlbkFJgnGIRcZuv0M6OfHdzZbXhhPO1BqPSbV3vprgJj2GYA"
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to read content from a text file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to generate a response from OpenAI
def generate_response(prompt, context):
    # Combine context with the prompt
    full_prompt = f"Context:\n{context}\n\nQuestion:\n{prompt}"
    
    # Call OpenAI's GPT-3 model
    output = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": full_prompt}])
    
    return output.choices[0].message.content

# Main function
def main(query):
    # File containing the knowledge base
    file_path = "history/history.txt"
    
    # Read the content from the file
    context = read_file(file_path)
    
    # User query
    #while True:
    added_query=" Do your best. Remember that the context holds the transcript for a call. Do not make stuff up."
    #query = input('Give your question about the call: ')
    query=query+added_query
        
    # Generate a response
    answer = generate_response(query, context)
    
    #print("Answer:", answer)
    return answer

if __name__ == "__main__":
    main('TEST QUERY')