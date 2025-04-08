import os
from dotenv import load_dotenv
from groq import Groq
import gradio as gr
from langdetect import detect


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print("API KEY:", api_key)
client = Groq(api_key=api_key)



# Define chatbot function
def chat_with_stream(user_input, history):
   
    try:
      language = detect(user_input)
      if language not in ["en", "fr"]:
        language = "en"  
    except Exception as e:
        language = "en"  


    if language == "fr":
        system_prompt = {
            "role": "system",
            "content": """
            Vous êtes un assistant de planification d'événements efficace. Votre objectif est de fournir des informations claires, concises et exploitables sous forme de puces.
Souvenez-vous toujours des interactions passées pour fournir des conseils pertinents et supposez que tout le monde veut une option moins chère.
N'oubliez jamais d'être amical et accessible, utilisez des émojis pertinents dans presque tous les messages pour soutenir une approche amicale et terminez par une question de suivi.
"""
        }
    
    else:system_prompt = {
        "role": "system",
        "content": """
        You are an efficient Event Planning Assistant. Your goal is to provide clear, concise, and actionable information in bullet points.
        Always remember past interactions to provide relevant advice and assume everyone wants a cheaper option.
        Always remember to be friendly and approachable use  relevant emojis almost every message to support friendly approach and end with a follow-up question.
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
        print("RESPONSE DEBUG:", bot_response)
        

    

    except Exception as e:
        return "Oops! Something went wrong. Please try again in a moment. If the issue continues, contact us at 343-777-9651."
        

    
custom_css = """
 /* Remove box and center everything */
.gradio-container {
  padding: 0 !important;
  margin: 0 !important;
  width: 100% !important;
  max-width: none !important;
  box-shadow: none !important;
  border: none !important;
}


#chatbot_component {
  width: 100% !important;
  height: calc(100vh - 80px);
  padding: 0;
  margin: 0;
  background: white !important;
  border: none !important;
  box-shadow: none !important;
}


.chat-history {
  background-color: #fafafa;
  border-right: 1px solid #eee;
  padding: 10px;
}


#textbox_component {
  position: fixed !important;
  bottom: 0;
  width: 76% !important;
  height:20% !important;
  left: 0;
  background: none !important;
  padding: 16px 24px;
  z-index: 99;
  display: flex;
  align-items: center;
  border-top: 1px solid #e0e0e0;
}

#textbox_component textarea,
#textbox_component input {
  width: 100%;
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 16px;
  border: 1px solid #ccc;
}
#textbox_component button {
    background-color: black !important;
    color: white !important;
    font-size: 16px;
    border-radius: 8px;
    padding:20px 20px;
    cursor: pointer;
    transition: background 0.3s ease-in-out;
    background-image: none !important; /* Remove any background image */
    background: black!important; /* Ensures background color is applied */
    margin-left: 5px;
}
#textbox_component button svg{
width:25px;
height:25px;
}
#textbox_component button:hover{
background-color: #303236 !important;
}
@media (max-width: 768px) {
  #textbox_component {
    height: auto !important;
    padding: 12px 16px;
    border-top: 1px solid #444;
    background-color: white !important;
  }

  #textbox_component textarea,
  #textbox_component input {
    font-size: 16px !important;
    padding: 10px 14px !important;
  }

  #textbox_component button {
    padding: 12px 16px !important;
  }

  #chatbot_component {
    height: calc(100vh - 160px); /* Account for input height on mobile */
    overflow-y: auto;
  }
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
def change_mode(mode:str):  
     if mode == "DarkMode":
       return f"""  
    <style>
      /* Targeting all text within the chatbot container */
     body,
.gradio-container{{
    background-color: #121212 !important;
    color: white !important;
}}

 #chatbot_component *{{
    background-color:  #121212 !important;
}}
#chatbot_component .examples * {{
          background-color: black !important;}}

#chatbot_component .placeholder h1 {{
  color: white !important;
}}
 #chatbot_component .placeholder center {{
    color: white !important;
}}
#chatbot_component .message *{{
    color: white !important;
    border-radius: 12px;
}}
#chatbot_component .message button svg {{
    fill: white !important;
    width: 20px;
    height: 20px;
    opacity: 0.6;
    transition: opacity 0.2s ease;
}}

#textbox_component  {{
          background-color: #EEEEF0 !important;
          border-color:#EEFEF5!important;
          border-width: 1px;
          border-radious:25px;
      }}
#textbox_component button {{   
    color: black !important;
    font-size: 16px;
    border-radius: 8px;
    padding:20px 20px;
    cursor: pointer;
    transition: background 0.3s ease-in-out;
}}
.submit-button {{
    background-color: white !important;
    background-image: none !important; /* Remove any background image */
    background: white !important; /* Ensures background color is applied */
    margin-left: 5px;
}}
.submit-button svg{{
width:25px;
height:25px;
}}
.tabs {{
    background-color: #121212 !important;
    color: white !important;
}}


    </style>
      """
     else:
        return f"""  
    <style>
      /* Targeting all text within the chatbot container */
      #chatbot_component * {{
         background-color: white !important;
      }}
      #textbox_component {{
          background-color:#EEEEF0 !important;
           border-color:#EEFEF5!important;
           border-width: 1px;
           border-radius:25px;
      }}
#textbox_component button {{
   
    color: black !important;
    font-size: 16px;
    border-radius: 8px;
    padding:20px 20px;
    cursor: pointer;
    transition: background 0.3s ease-in-out;
}}
.submit-button {{
    background-color: #EEFEF5 !important;
    background-image: none !important; /* Remove any background image */
    background: #EEFEF5 !important; /* Ensures background color is applied */
    margin-left: 5px;
}}
.submit-button svg{{
width:25px;
height:25px;
}}
    </style>
      """

   
         
    
def change_language(language: str):
    if language == "English":
        placeholder = ("<h1>Hey I'm Event Buddy</h1><br><center>Your personal assitant for event planning</center>")
        examples = [
        {
        "text": "What are some fun activities for an event?",
        "display_text": "What are some fun activities for an event?"  # Same as text
        },
        {
        "text": "What are some budget-friendly event ideas",
        "display_text": "What are some budget-friendly event ideas"  # Same as text
        },
        {
        "text": "What are some event planning tips i can do?",
        "display_text": "What are some event planning tips i can do?"  # Same as text
        },
]
    else:
        placeholder =("<h1>Salut, je suis Event Buddy</h1><br><center>Votre assistant personnel pour la planification d'événements</center>")
        examples = [
            {
                "text": "Quelles sont des activités amusantes pour un événement ?",
                "display_text": "Quelles sont des activités amusantes pour un événement ?"
            },
            {
                "text": "Quelles sont des idées d'événements économiques ?",
                "display_text": "Quelles sont des idées d'événements économiques ?"
            },
            {
                "text": "Quels sont des conseils pour organiser un événement ?",
                "display_text": "Quels sont des conseils pour organiser un événement ?"
            },
        ]
    chatbot = gr.Chatbot(elem_id="chatbot_component",type="messages",placeholder=placeholder, label="EventBuddy",examples=examples)
        
    return chatbot
image_path = "/Users/kenoobuwoma/Downloads/school/Secondyear/SEG 3125/Assignments/EventBuddy/static/EventBuddy.png"

    
# Launch Gradio chat interface
with gr.Blocks(theme=gr.themes.Ocean(), css=custom_css) as demo:

    with gr.Tab("Chat",elem_classes="tabs"):
         with gr.Row():
            with gr.Column(scale=3,elem_id="chat_tab"): 
                chatbot = gr.Chatbot(elem_id="chatbot_component",type="messages",placeholder= "<h1>Hey I'm Event Buddy</h1><br><center>Your personal assitant for event planning</center>",show_copy_button = True, show_label= False)
                gr.HTML(value="<script>setTimeout(() => console.log('DEBUG HTML:', document.getElementById('chatbot_component').innerHTML), 1000)</script>")

            with gr.Column(scale=1): 
               
                textbox=gr.Textbox (elem_id="textbox_component",label="User Input", placeholder="Type your message here", lines=1, type="text", interactive = True, submit_btn = True)
                gr.ChatInterface(
                fn=chat_with_stream,
                type="messages",  
                title="",
                examples=[
                      "What are some fun activities for an event?",
                      "What are some budget-friendly event ideas?",
                      "What are some event planning tips i can do?",
                      
                       ],
                theme="ocean",
                save_history=True,
                chatbot= chatbot,
                textbox=textbox,
                editable=True,
                fill_width=True,
                fill_height=True
)
    

    
    with gr.Tab("Setting ⚙️",elem_classes="tabs"):

      with gr.Group(elem_id="smallbox"):  # Creates a box with padding around the grouped components
            gr.Markdown("### Chatbot & Settings", elem_id= "title")  # Optional title inside the box
            with gr.Column(elem_id= "title"):
                language = gr.Radio(
                    ["English", "French"], label="Language"
                )
                mode = gr.Radio(
                    ["DarkMode", "LightMode"], label="Theme", elem_id= "theme"
                )
                font_color =gr.ColorPicker(label="Font Color")
                color_style = gr.HTML()
                background_style = gr.HTML()
                

                # Event handlers
                font_color.change(fn =change_text_color, inputs=font_color, outputs=color_style)
                language.change(fn= change_language, inputs=language, outputs=chatbot)
                mode.change(fn=change_mode, inputs=mode, outputs=background_style)
                
            
 
            
   
    
   
demo.launch()


