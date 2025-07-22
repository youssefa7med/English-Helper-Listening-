import os
import uuid
import requests
import json
import random
import re
import gradio as gr
from gradio_client import Client
from dotenv import load_dotenv

load_dotenv()

def log_step(msg):
    print(f"[EVAL_LISTENING] {msg}")

# Environment variables
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
TTS_PASSWORD = os.getenv("TTS_PASSWORD")

if not all([DEEPSEEK_API_KEY, HF_TOKEN, TTS_PASSWORD]):
    raise ValueError("Missing required environment variables!")

# Initialize TTS client
TTS_CLIENT = Client("KindSynapse/Youssef-Ahmed-Private-Text-To-Speech-Unlimited", hf_token=HF_TOKEN)

def clean_text_for_tts(text):
    """Clean text for better TTS output"""
    # Remove emojis and special characters
    text = re.sub(r'[🎯🌟✨💫🎤🤖📚📊]', '', text)
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def text_to_speech(text):
    """Convert text to speech using the specified TTS service"""
    try:
        clean_text = clean_text_for_tts(text)
        result = TTS_CLIENT.predict(
            password=TTS_PASSWORD,
            prompt=clean_text,
            voice="coral",
            emotion="Clear and educational",
            use_random_seed=True,
            specific_seed=12345,
            api_name="/text_to_speech_app"
        )
        return result[0] if isinstance(result, (list, tuple)) else result
    except Exception as e:
        log_step(f"Error in text to speech: {str(e)}")
        return None

def generate_listening_passage(topic):
    """Generate a listening passage with graduated difficulty levels"""
    if not DEEPSEEK_API_KEY:
        raise EnvironmentError("Missing DEEPSEEK_API_KEY in environment.")

    prompt = f"""
    Create a listening passage about "{topic}" with graduated difficulty levels. The passage should have 4 paragraphs:
    
    1. First paragraph: A1-A2 level (beginner) - Simple sentences, basic vocabulary, present tense, slow pace
    2. Second paragraph: B1 level (intermediate) - More complex sentences, varied vocabulary, past/future tenses
    3. Third paragraph: B2 level (upper-intermediate) - Complex grammar, academic vocabulary, conditional forms
    4. Fourth paragraph: C1-C2 level (advanced) - Sophisticated language, complex ideas, advanced structures
    
    Each paragraph should be 50-70 words and build upon the previous one while maintaining coherence.
    The content should be engaging, educational, and suitable for listening comprehension.
    Use natural, conversational language that sounds good when spoken aloud.
    
    IMPORTANT: Write ONLY the paragraphs without any level headings or labels. Just provide the 4 paragraphs separated by line breaks.
    Make sure the language flows naturally for audio presentation.
    """

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            json={
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert English language teacher who creates listening materials for language learners at different proficiency levels. Focus on creating content that sounds natural when spoken."
                    },
                    {
                        "role": "user",
                        "content": prompt.strip()
                    }
                ],
                "temperature": random.uniform(0.9, 1),
                "max_tokens": 800
            }
        )

        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"].strip()
        
        return f"Error generating passage: Status {response.status_code}"

    except Exception as e:
        return f"Error generating passage: {str(e)}"

def evaluate_listening_performance(original_text, user_input):
    """Evaluate listening performance based on original text and user's written response"""
    if not DEEPSEEK_API_KEY:
        raise EnvironmentError("Missing DEEPSEEK_API_KEY in environment.")

    prompt = f"""
    You are an expert English listening comprehension tutor evaluating a learner's listening performance based on CEFR standards.

    The learner listened to the following audio passage:
    ---
    {original_text}
    ---

    This is what they wrote after listening (what they understood):
    ---
    {user_input}
    ---

    Please evaluate their listening comprehension and return a JSON response with:
    1. "comprehension_score": Score out of 100 for overall understanding
    2. "accuracy_score": Score out of 100 for accuracy of details captured
    3. "vocabulary_recognition": Score out of 100 for recognizing vocabulary
    4. "listening_level": Estimated CEFR level (A1-C2) based on comprehension
    5. "correctly_identified": Key points and details they got right
    6. "missed_information": Important information they missed or misunderstood
    7. "vocabulary_gaps": Specific vocabulary they seemed to struggle with
    8. "listening_strengths": What they demonstrated well in their comprehension
    9. "improvement_areas": Specific areas that need work for better listening
    10. "practice_recommendations": Actionable advice for improving listening skills
    11. "level_appropriate_feedback": Feedback tailored to their demonstrated level
    12. "motivational_comment": Encouraging feedback to boost confidence

    Compare what they wrote with the original text to assess:
    - Overall comprehension and main idea understanding
    - Detail recognition and accuracy
    - Vocabulary comprehension
    - Ability to handle different difficulty levels

    Be encouraging while providing constructive feedback. Focus on what they did well first, then areas for improvement.

    Respond in clean JSON format only.
    """

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            json={
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a certified English listening comprehension tutor specializing in CEFR-based assessment. You provide constructive, encouraging feedback that helps students improve."
                    },
                    {
                        "role": "user",
                        "content": prompt.strip()
                    }
                ],
                "temperature": random.uniform(0.9, 1),
                "max_tokens": 1500
            }
        )

        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                clean_json_text = re.sub(r"```json|```", "", content).strip()

                try:
                    return json.loads(clean_json_text)
                except json.JSONDecodeError as decode_err:
                    return {
                        "comprehension_score": 0,
                        "accuracy_score": 0,
                        "vocabulary_recognition": 0,
                        "listening_level": "Unknown",
                        "correctly_identified": [],
                        "missed_information": [],
                        "vocabulary_gaps": [],
                        "listening_strengths": "N/A",
                        "improvement_areas": "N/A",
                        "practice_recommendations": [f"Invalid JSON format: {str(decode_err)}"],
                        "level_appropriate_feedback": "Keep practicing!",
                        "motivational_comment": "Great effort! Keep listening and improving!"
                    }
        else:
            return {
                "comprehension_score": 0,
                "accuracy_score": 0,
                "vocabulary_recognition": 0,
                "listening_level": "Unknown",
                "correctly_identified": [],
                "missed_information": [],
                "vocabulary_gaps": [],
                "listening_strengths": "N/A",
                "improvement_areas": "N/A",
                "practice_recommendations": [f"API Error: {response.status_code}"],
                "level_appropriate_feedback": "Keep practicing!",
                "motivational_comment": "Great effort! Keep listening and improving!"
            }

    except Exception as e:
        return {
            "comprehension_score": 0,
            "accuracy_score": 0,
            "vocabulary_recognition": 0,
            "listening_level": "Unknown",
            "correctly_identified": [],
            "missed_information": [],
            "vocabulary_gaps": [],
            "listening_strengths": "N/A",
            "improvement_areas": "N/A",
            "practice_recommendations": [f"Exception occurred: {str(e)}"],
            "level_appropriate_feedback": "Keep practicing!",
            "motivational_comment": "Great effort! Keep listening and improving!"
        }

def generate_passage_and_audio(topic):
    """Generate listening passage and create audio files for each paragraph"""
    log_step(f"Generating passage for topic: {topic}")
    
    if not topic.strip():
        return "Please enter a topic first!", None, None, None, None, ""
    
    # Generate the passage
    passage = generate_listening_passage(topic)
    log_step("Passage generated successfully")
    
    if passage.startswith("Error"):
        return passage, None, None, None, None, ""
    
    # Split into paragraphs
    paragraphs = [p.strip() for p in passage.split('\n\n') if p.strip()]
    
    if len(paragraphs) != 4:
        # Try different splitting methods
        paragraphs = [p.strip() for p in passage.split('\n') if p.strip() and len(p.strip()) > 20]
    
    # Ensure we have exactly 4 paragraphs
    if len(paragraphs) < 4:
        return "Error: Could not generate 4 proper paragraphs. Please try again.", None, None, None, None, ""
    
    # Take only first 4 paragraphs if more were generated
    paragraphs = paragraphs[:4]
    
    # Generate audio for each paragraph
    audio_files = []
    for i, paragraph in enumerate(paragraphs):
        log_step(f"Generating audio for paragraph {i+1}")
        audio_file = text_to_speech(paragraph)
        audio_files.append(audio_file)
    
    # Create level labels
    levels = ["A1-A2 (Beginner)", "B1 (Intermediate)", "B2 (Upper-Intermediate)", "C1-C2 (Advanced)"]
    
    return (
        "✅ Audio generated successfully! Listen to each paragraph and write what you hear.",
        audio_files[0], audio_files[1], audio_files[2], audio_files[3],
        passage  # Store the original passage for evaluation
    )

def evaluate_listening_only(original_passage, user_response):
    """Evaluate listening performance"""
    if not original_passage.strip():
        return json.dumps({
            "error": "Please generate audio first!"
        }, indent=2)
    
    if not user_response.strip():
        return json.dumps({
            "error": "Please write what you heard from the audio!"
        }, indent=2)
    
    log_step("Starting listening evaluation...")
    
    # Evaluate performance
    result = evaluate_listening_performance(original_passage, user_response)
    log_step("Evaluation completed")
    
    return json.dumps(result, indent=2, ensure_ascii=False)

# Create the Gradio interface
with gr.Blocks(title="English Listening Evaluation System", theme=gr.themes.Soft()) as iface:
    gr.Markdown("# 🎧 English Listening Evaluation System")
    gr.Markdown("**Practice your English listening skills with graduated difficulty levels!**")
    
    # Step 1: Topic Input
    gr.Markdown("## Step 1: Enter Topic")
    topic_input = gr.Textbox(
        label="Enter a topic for your listening passage",
        placeholder="e.g., Climate Change, Technology, Travel, History, Science, Culture...",
        value=""
    )
    
    generate_btn = gr.Button("🎯 Generate Listening Audio", variant="primary", size="lg")
    
    # Step 2: Audio Generation Status
    gr.Markdown("## Step 2: Generated Audio Files")
    status_output = gr.Textbox(
        label="Generation Status",
        interactive=False,
        placeholder="Status will appear here..."
    )
    
    # Step 3: Audio Players for each level
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🔊 A1-A2 Level (Beginner)")
            audio1 = gr.Audio(label="Listen to Paragraph 1", type="filepath")
        with gr.Column():
            gr.Markdown("### 🔊 B1 Level (Intermediate)")
            audio2 = gr.Audio(label="Listen to Paragraph 2", type="filepath")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🔊 B2 Level (Upper-Intermediate)")
            audio3 = gr.Audio(label="Listen to Paragraph 3", type="filepath")
        with gr.Column():
            gr.Markdown("### 🔊 C1-C2 Level (Advanced)")
            audio4 = gr.Audio(label="Listen to Paragraph 4", type="filepath")
    
    # Step 4: User Input
    gr.Markdown("## Step 3: Write What You Heard")
    gr.Markdown("**Instructions:** Listen to each audio paragraph carefully and write down everything you understood. Don't worry about perfect spelling - focus on capturing the meaning and as many details as possible!")
    
    user_response = gr.Textbox(
        label="✍️ Write what you heard from ALL paragraphs",
        lines=10,
        max_lines=15,
        placeholder="Listen to the audio files above and write down everything you understood here...\n\nTips:\n- Listen to each paragraph multiple times if needed\n- Write down main ideas and details\n- Don't worry about perfect grammar in your response\n- Include as much as you can remember from each level"
    )
    
    evaluate_btn = gr.Button("📊 Evaluate My Listening Comprehension", variant="primary", size="lg")
    
    # Step 5: Evaluation Results
    gr.Markdown("## Step 4: Your Listening Evaluation Results")
    evaluation_output = gr.Code(
        label="📋 Detailed Listening Assessment",
        language="json",
        interactive=False
    )
    
    # Hidden component to store the original passage
    original_passage_store = gr.Textbox(visible=False)
    
    # Connect the functions
    generate_btn.click(
        fn=generate_passage_and_audio,
        inputs=topic_input,
        outputs=[status_output, audio1, audio2, audio3, audio4, original_passage_store]
    )
    
    evaluate_btn.click(
        fn=evaluate_listening_only,
        inputs=[original_passage_store, user_response],
        outputs=evaluation_output
    )
    
    # Instructions
    gr.Markdown("""
    ## 📝 How to Use This System:
    
    1. **Enter a topic** you're interested in learning about
    2. **Generate audio** - the system will create 4 audio paragraphs with increasing difficulty
    3. **Listen carefully** to each paragraph (you can replay them as many times as needed)
    4. **Write down** everything you understood from all paragraphs
    5. **Get evaluated** - receive detailed feedback on your listening comprehension
    
    ## 🎯 Tips for Better Listening:
    - Listen to each paragraph multiple times
    - Focus on main ideas first, then details
    - Don't worry if you don't catch everything - write what you understand
    - Pay attention to context clues
    - Practice regularly with different topics
    """)

if __name__ == "__main__":
    iface.launch()