# English Listening Evaluation System 🎧

![English Listening](https://miro.medium.com/v2/resize:fit:1024/1*5b5EZIxYES-lC_YGxLvtDQ.gif)

An intelligent English listening comprehension evaluation system powered by AI that generates personalized listening exercises with graduated difficulty levels and provides detailed performance assessments based on CEFR standards.

## 🚀 Live Demo

**Try it now:** [English Helper Listening - Live Demo](https://huggingface.co/spaces/YoussefA7med/English_Helper_Listening)

Experience the full functionality of the English Listening Evaluation System directly in your browser! No installation required.

## 🌟 Features

### 🎯 **Personalized Content Generation**
- Generate listening passages on any topic of interest
- AI-powered content creation using DeepSeek Chat API
- Engaging and educational content tailored for language learners

### 📊 **Graduated Difficulty Levels**
- **A1-A2 (Beginner)**: Simple sentences, basic vocabulary, present tense
- **B1 (Intermediate)**: Complex sentences, varied vocabulary, past/future tenses
- **B2 (Upper-Intermediate)**: Advanced grammar, academic vocabulary, conditional forms
- **C1-C2 (Advanced)**: Sophisticated language, complex ideas, advanced structures

### 🔊 **High-Quality Text-to-Speech**
- Individual audio files for each difficulty level
- Natural-sounding speech using advanced TTS technology
- Clear pronunciation optimized for language learning

### 📝 **Comprehensive Assessment**
- **Comprehension Score**: Overall understanding evaluation
- **Accuracy Score**: Detail recognition and precision
- **Vocabulary Recognition**: Word identification capabilities
- **CEFR Level Assessment**: Automatic level determination

### 🎓 **Detailed Feedback System**
- Correctly identified information highlighting
- Missed information analysis
- Vocabulary gap identification
- Personalized improvement recommendations
- Motivational comments and encouragement

## 🚀 Getting Started

### Try Online First
Before setting up locally, test the system using our **[Live Demo](https://huggingface.co/spaces/YoussefA7med/English_Helper_Listening)** to see if it meets your needs!

### Prerequisites

Before running the application locally, ensure you have the following:

- Python 3.8 or higher
- Required Python packages (see [Installation](#installation))
- API keys for the required services

### Required API Keys

You'll need to obtain the following API keys:

1. **DeepSeek API Key**: For AI-powered content generation and evaluation
   - Sign up at [DeepSeek Platform](https://platform.deepseek.com/)
   
2. **Hugging Face Token**: For accessing the TTS service
   - Get your token from [Hugging Face](https://huggingface.co/settings/tokens)
   
3. **TTS Service Password**: For the private Text-to-Speech service
   - Contact the service provider for access credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/english-listening-evaluation.git
   cd english-listening-evaluation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   HUGGINGFACE_TOKEN=your_huggingface_token_here
   TTS_PASSWORD=your_tts_password_here
   ```

4. **Run the application**
   ```bash
   python listening_evaluation.py
   ```

5. **Access the interface**
   
   Open your browser and navigate to the URL displayed in the terminal (typically `http://localhost:7860`)

## 📋 Requirements

Create a `requirements.txt` file with the following dependencies:

```txt
gradio>=4.0.0
requests>=2.31.0
python-dotenv>=1.0.0
gradio-client>=0.8.0
pydub>=0.25.1
```

## 🎮 How to Use

### Step 1: Enter Topic
- Input any topic you want to practice listening with
- Examples: "Climate Change", "Technology", "Travel", "History", "Science"

### Step 2: Generate Audio
- Click "Generate Listening Audio" to create your personalized content
- The system generates 4 audio files with increasing difficulty

### Step 3: Listen and Comprehend
- Play each audio file as many times as needed
- **A1-A2**: Start with the beginner level
- **B1**: Progress to intermediate
- **B2**: Challenge yourself with upper-intermediate
- **C1-C2**: Test advanced comprehension skills

### Step 4: Write Your Response
- Write down everything you understood from all paragraphs
- Focus on capturing main ideas and details
- Don't worry about perfect grammar in your response

### Step 5: Get Evaluated
- Click "Evaluate My Listening Comprehension"
- Receive detailed feedback on your performance
- Get personalized recommendations for improvement

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Topic Input   │───▶│  Content Gen.    │───▶│   TTS Engine    │
└─────────────────┘    │  (DeepSeek API)  │    │ (HuggingFace)   │
                       └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Evaluation    │◀───│  User Response   │◀───│  Audio Files    │
│   (DeepSeek)    │    │   Collection     │    │   (4 levels)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🎯 Learning Benefits

### For Language Learners
- **Progressive Skill Building**: Start at your level and advance gradually
- **Real-world Topics**: Practice with relevant, interesting content
- **Immediate Feedback**: Get instant assessment and improvement tips
- **Self-paced Learning**: Repeat exercises as many times as needed

### For Educators
- **Curriculum Support**: Supplement existing listening programs
- **Assessment Tool**: Evaluate student progress objectively
- **Customizable Content**: Generate materials for specific topics
- **CEFR Alignment**: Standards-based evaluation system

## 🔧 Customization

### Adding New Difficulty Levels
Modify the `generate_listening_passage()` function to include additional CEFR levels or custom difficulty parameters.

### Changing TTS Voices
Update the TTS parameters in the `text_to_speech()` function to use different voices or emotional tones.

### Custom Evaluation Criteria
Extend the evaluation system by modifying the `evaluate_listening_performance()` function to include additional assessment metrics.

## 📊 Technical Details

### AI Models Used
- **Content Generation**: DeepSeek Chat API for creating graduated difficulty passages
- **Performance Evaluation**: Advanced language processing for comprehensive assessment
- **Text-to-Speech**: High-quality neural TTS for natural-sounding audio

### Supported Languages
- Primary: English (US)
- Future support planned for additional languages

### Audio Formats
- Output: WAV format for maximum compatibility
- Quality: Optimized for speech clarity and comprehension

## 🤝 Contributing

We welcome contributions to improve the English Listening Evaluation System!

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution
- Additional language support
- New evaluation metrics
- UI/UX improvements
- Performance optimizations
- Documentation enhancements

## 🐛 Troubleshooting

### Common Issues

**Issue: Audio not generating**
- Solution: Check TTS service credentials and internet connection

**Issue: Evaluation not working**
- Solution: Verify DeepSeek API key is valid and has sufficient credits

**Issue: Interface not loading**
- Solution: Ensure all dependencies are installed and Python version is compatible

### Getting Help
- Check the [Issues](https://github.com/yourusername/english-listening-evaluation/issues) page
- Create a new issue with detailed error descriptions
- Include system information and error logs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **DeepSeek**: For providing advanced language AI capabilities
- **Hugging Face**: For TTS infrastructure and model hosting
- **Gradio**: For the intuitive web interface framework
- **CEFR Framework**: For standardized language proficiency guidelines

## 📞 Contact

- **Project Maintainer**: [Youssef Ahmed](mailto:youssef111ahmed111@gmail.com)
- **GitHub**: [@youssefa7med](https://github.com/youssefa7med)

---

### 🌟 Star this repository if it helped you improve your English listening skills!

**Made with ❤️ for English language learners worldwide**
