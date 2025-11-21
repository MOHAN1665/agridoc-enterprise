# import google.generativeai as genai
# from google.generativeai.types import FunctionDeclaration, Tool
# from src.config import Config
# from src.database import OutbreakRegistry
# import json

# class PlantDoctorAgent:
#     def __init__(self):
#         # 1. Configure API
#         genai.configure(api_key=Config.GOOGLE_API_KEY)
#         self.db = OutbreakRegistry()
        
#         # 2. Define the Tool
#         self.log_tool = {
#             'function_declarations': [
#                 {
#                     'name': 'log_outbreak',
#                     'description': 'Logs a disease to the database. Call this if confidence > 70%.',
#                     'parameters': {
#                         'type_': 'OBJECT',
#                         'properties': {
#                             'plant': {'type_': 'STRING'},
#                             'disease': {'type_': 'STRING'},
#                             'confidence': {'type_': 'NUMBER'},
#                             'severity': {'type_': 'STRING'}
#                         },
#                         'required': ['plant', 'disease', 'confidence', 'severity']
#                     }
#                 }
#             ]
#         }
        
#         # 3. Initialize Model
#         self.model = genai.GenerativeModel(
#             model_name=Config.MODEL_NAME,
#             tools=[self.log_tool],
#             system_instruction="You are an expert AI Botanist. You can see images. Analyze the plant health."
#         )

#     def analyze_and_act(self, image_bytes):
#         prompt = """
#         Analyze this plant image.
#         1. Identify the plant and any disease (or say 'Healthy').
#         2. If a specific disease is detected with >70% confidence, CALL the 'log_outbreak' function.
#         3. After the tool call (or if no tool is needed), provide a diagnosis and 3 organic remedies.
#         """
        
#         # Send Image + Prompt
#         response = self.model.generate_content(
#             [
#                 {'mime_type': 'image/jpeg', 'data': image_bytes},
#                 prompt
#             ],
#             tool_config={'function_calling_config': 'AUTO'}
#         )
        
#         # === ROBUST PARSING LOGIC ===
#         logged_status = False
#         final_text_response = ""
#         function_call_found = None

#         try:
#             # Iterate through ALL parts to find text and function calls
#             # Gemini 2.0 often outputs: [Text Part (Thought)] -> [FunctionCall Part]
#             for part in response.candidates[0].content.parts:
#                 if part.function_call:
#                     function_call_found = part.function_call
                
#                 # Collect any text (thoughts) provided before/after
#                 if part.text:
#                     final_text_response += part.text + "\n\n"

#             # If we found a function call, execute it
#             if function_call_found:
#                 fc = function_call_found
#                 if fc.name == "log_outbreak":
#                     # Convert arguments to dict
#                     args = {k: v for k, v in fc.args.items()}
                    
#                     print(f"⚠️ Model calling tool: {args}")
#                     self.db.log_incident(**args)
#                     logged_status = True
                    
#                     # Generate the final user-friendly summary
#                     # We ask the model to summarize the action it just took
#                     summary_model = genai.GenerativeModel(Config.MODEL_NAME)
#                     summary_response = summary_model.generate_content(
#                         f"I just detected {args['disease']} on {args['plant']} and logged it. "
#                         f"Current thoughts: {final_text_response}. "
#                         f"Please write a clean, helpful diagnosis and 3 organic remedies for the user."
#                     )
#                     final_text_response = summary_response.text

#             # If no text was generated at all (rare), provide a fallback
#             if not final_text_response.strip():
#                 final_text_response = "Analysis complete. Check the logs for details."

#         except Exception as e:
#             print(f"Parsing Error: {e}")
#             final_text_response = f"I analyzed the image, but encountered a processing error: {str(e)}"

#         return final_text_response, logged_status


import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool
from src.config import Config
from src.database import OutbreakRegistry
import json

class PlantDoctorAgent:
    def __init__(self):
        # 1. Configure API
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.db = OutbreakRegistry()
        
        # 2. Define the Tool
        self.log_tool = {
            'function_declarations': [
                {
                    'name': 'log_outbreak',
                    'description': 'Logs a disease to the database. Call this if confidence > 70%.',
                    'parameters': {
                        'type_': 'OBJECT',
                        'properties': {
                            'plant': {'type_': 'STRING'},
                            'disease': {'type_': 'STRING'},
                            'confidence': {'type_': 'NUMBER'},
                            'severity': {'type_': 'STRING'}
                        },
                        'required': ['plant', 'disease', 'confidence', 'severity']
                    }
                }
            ]
        }
        
        # 3. Initialize Model
        self.model = genai.GenerativeModel(
            model_name=Config.MODEL_NAME,
            tools=[self.log_tool],
            system_instruction="You are an expert AI Botanist. You can see images. Analyze the plant health."
        )

    # === FIX: Added 'language' parameter here ===
    def analyze_and_act(self, image_bytes, language="English"):
        # === FIX: Added 'f' before the string to make it dynamic ===
        prompt = f"""
        Analyze this plant image.
        1. Identify the plant and any disease (or say 'Healthy').
        2. If a specific disease is detected with >70% confidence, CALL the 'log_outbreak' function.
        3. After the tool call (or if no tool is needed), provide a diagnosis and 3 organic remedies in {language} language.
        """
        
        # Send Image + Prompt
        response = self.model.generate_content(
            [
                {'mime_type': 'image/jpeg', 'data': image_bytes},
                prompt
            ],
            tool_config={'function_calling_config': 'AUTO'}
        )
        
        # === ROBUST PARSING LOGIC ===
        logged_status = False
        final_text_response = ""
        function_call_found = None

        try:
            # Iterate through ALL parts to find text and function calls
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    function_call_found = part.function_call
                
                if part.text:
                    final_text_response += part.text + "\n\n"

            # If we found a function call, execute it
            if function_call_found:
                fc = function_call_found
                if fc.name == "log_outbreak":
                    args = {k: v for k, v in fc.args.items()}
                    
                    print(f"⚠️ Model calling tool: {args}")
                    self.db.log_incident(**args)
                    logged_status = True
                    
                    # Generate summary in the correct language
                    summary_model = genai.GenerativeModel(Config.MODEL_NAME)
                    summary_response = summary_model.generate_content(
                        f"I just detected {args['disease']} on {args['plant']} and logged it. "
                        f"Current thoughts: {final_text_response}. "
                        f"Please write a clean, helpful diagnosis and 3 organic remedies for the user in {language} language."
                    )
                    final_text_response = summary_response.text

            if not final_text_response.strip():
                final_text_response = "Analysis complete. Check the logs for details."

        except Exception as e:
            print(f"Parsing Error: {e}")
            final_text_response = f"I analyzed the image, but encountered a processing error: {str(e)}"

        return final_text_response, logged_status