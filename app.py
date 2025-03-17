from groq import Groq
import gradio as gr
from langdetect import detect

# Initialize Groq client
client = Groq(api_key="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")

# Define chatbot function
def chat_with_stream(user_input, history):
    # System prompt (only added if history is empty)
    try:
      language = detect(user_input)
      if language not in ["en", "fr"]:
        language = "en"  # Force English if detection is uncertain
    except Exception as e:
        language = "en"  


    if language == "fr":
        system_prompt = {
            "role": "system",
            "content": """
            Vous êtes un assistant de planification d'événements efficace. Votre objectif est de fournir des informations claires, concises et exploitables sous forme de puces.
Souvenez-vous toujours des interactions passées pour fournir des conseils pertinents et supposez que tout le monde veut une option moins chère.
N'oubliez jamais d'être amical et accessible, utilisez des émojis dans presque tous les messages pour soutenir une approche amicale.
"""
        }
    
    else:system_prompt = {
        "role": "system",
        "content": """
        You are an efficient Event Planning Assistant. Your goal is to provide clear, concise, and actionable information in bullet points.
        Always remember past interactions to provide relevant advice and assume everyone wants a cheaper option.
        Always remember to be friendly and approachable use emojis almost every message to support friendly approach.
        """
    }

    # Convert history to message format
    if not history:
     conversation_history = [system_prompt] #first message set to system_prompt
    else:
     conversation_history = []

    if not user_input.strip():
        user_input = "Event Planning"
    #print("History:", history)
      
    # Unpack history correctly
      
    for entry in history:
        if isinstance(entry, dict) and 'role' in entry and 'content' in entry:
            # Append only valid entries
            conversation_history.append({
                "role": entry['role'], 
                "content": entry['content']
            })
        else:
            print(f"Invalid entry format: {entry}")  # Log invalid entries



    # Append latest user input
    conversation_history.append({"role": "user", "content": user_input})
    # Log the final conversation history before sending to the API
    ##print("Final Conversation History:", conversation_history)



    try:
        # Call the API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False, 
            stop=None
        )

        bot_response = completion.choices[0].message.content  # Get chatbot reply
        return bot_response  # Ensure response is a string
    

    except Exception as e:
        return "Oops! Something went wrong. Please try again in a moment. If the issue continues, contact us at 343-777-9651."

    
custom_css = """
   /* Background color */
body { 
    background-color: #FCD5CE;  
    font-family: 'Arial', sans-serif;
    font-size: 16px;
}

/* Chatbot container */
.gradio-container {
    background-color: #edf6f9; !important;  /* Light gray */
}




"""
def change_text_color(color: str):
    # Adjust the selector below based on your Chatbot's DOM.
    return f"""
    <style>
      /* Targeting all text within the chatbot container */
      #chatbot_component * {{
          color: {color} !important;
      }}
    </style>
    """



   

# Launch Gradio chat interface
with gr.Blocks(theme=gr.themes.Ocean(), css=custom_css) as demo:
    gr.Markdown("## Event Buddy 🫂")
    chatbot = gr.Chatbot(elem_id="chatbot_component",placeholder="<h1>Hi I'm Event Buddy 🫂</h1><br><center>Ask Me Anything</center>", label="EventBuddy")
    

  
    with gr.Sidebar():
        gr.Markdown("Auto detect Both English and French")
        gr.Markdown("Just type in the language you are comfortable with")
        language = gr.Radio(["English", "French"], label="Language"),
        font_color =gr.ColorPicker(label="Font Color")
        
        color_style = gr.HTML()
        font_color.input(change_text_color, inputs=font_color, outputs=color_style)
        
        
    with gr.Row():
        with gr.Column():
            gr.ChatInterface(
            fn=chat_with_stream,
            type="messages",  
            title="",
            examples=[
                      "What are some fun activities for an event?",
                      "What are some budget-friendly event ideas",
                      "What are some event planning tips?",
                      
                       ],
            #cache_examples=False,
            theme="ocean",
            save_history=True,
            chatbot= chatbot,
)
    

demo.launch(share=True)


