# 🎓 MCP Learning Path Generator

A sophisticated Streamlit-based web application that generates personalized learning paths using the Model Context Protocol (MCP). This upgraded version includes enhanced error handling, better UI/UX, fallback mechanisms, and improved tool integration.

## ✨ Features

### Core Functionality
- 🎯 **Personalized Learning Paths**: Generate structured learning plans based on your goals
- 🎥 **YouTube Integration**: Search and recommend high-quality educational videos
- 📁 **Google Drive Integration**: Create and store learning documents (optional)
- 📝 **Notion Integration**: Create organized learning pages (optional)
- 🚀 **Real-time Progress Tracking**: Visual feedback during generation
- 🎨 **Modern UI/UX**: Beautiful, responsive interface with custom styling

### Enhanced Features (v2.0)
- 🔧 **Smart Tool Detection**: Automatically detects available tools and adapts functionality
- 🛡️ **Robust Error Handling**: Graceful fallbacks when tools are unavailable
- 📊 **Tool Status Dashboard**: Real-time status of available integrations
- 📜 **Learning Path History**: Save and manage previous learning paths
- ✅ **Input Validation**: Comprehensive validation for API keys and URLs
- 🎯 **Flexible Modes**: Works with full integration or YouTube-only mode
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile

## 🛠️ Prerequisites

- **Python 3.10+**
- **Google AI Studio API Key** (starts with "AI")
- **Pipedream URLs** for integrations:
  - YouTube (required)
  - Google Drive (optional)
  - Notion (optional)

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd mcp-learning-path-demo
```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Required Setup
1. **Google AI Studio API Key**
   - Get your API key from [Google AI Studio](https://aistudio.google.com/)
   - Key should start with "AI"

2. **Pipedream YouTube Integration**
   - Create a Pipedream workflow for YouTube API
   - Use the webhook URL in the app

### Optional Setup
3. **Google Drive Integration** (Optional)
   - Create a Pipedream workflow for Google Drive API
   - Configure document creation permissions

4. **Notion Integration** (Optional)
   - Create a Pipedream workflow for Notion API
   - Configure page creation permissions

## 🎯 Running the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📖 Usage Guide

### Step 1: Configure Tools
1. Enter your **Google AI Studio API key** in the sidebar
2. Add your **YouTube Pipedream URL** (required)
3. Optionally configure **Drive** or **Notion** URLs
4. The app will automatically detect available tools

### Step 2: Enter Learning Goal
Examples of good learning goals:
- "I want to learn Python basics in 3 days"
- "I want to learn data science fundamentals in 10 days"
- "I want to learn web development with React in 2 weeks"
- "I want to learn machine learning basics in 5 days"

### Step 3: Generate Learning Path
1. Click **"Generate Learning Path"**
2. Watch the real-time progress updates
3. Review your personalized learning plan
4. Access your learning path history

## 🏗️ Project Structure

```
mcp-learning-path-demo/
├── app.py              # Main Streamlit application
├── utils.py            # Core functionality and tool management
├── prompt.py           # AI prompt templates
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python with async/await support
- **AI Model**: Google Gemini 2.5 Flash
- **Protocol**: Model Context Protocol (MCP)
- **Integrations**: YouTube, Google Drive, Notion via Pipedream

### Key Components
- **Tool Detection**: Automatically identifies available MCP tools
- **Fallback System**: Graceful degradation when tools are unavailable
- **Progress Tracking**: Real-time feedback during generation
- **Error Handling**: Comprehensive error management and user feedback
- **History Management**: Persistent storage of learning paths

### Error Handling
- **Invalid API Keys**: Clear validation and error messages
- **Tool Unavailability**: Automatic fallback to available tools
- **Network Issues**: Retry mechanisms and user feedback
- **Generation Failures**: Detailed error reporting and suggestions

## 🎨 UI/UX Features

### Visual Design
- **Gradient Headers**: Modern gradient styling
- **Status Indicators**: Color-coded tool availability
- **Progress Bars**: Real-time generation progress
- **Responsive Layout**: Works on all screen sizes

### User Experience
- **Intuitive Navigation**: Clear sidebar and main content areas
- **Helpful Tooltips**: Context-sensitive help information
- **Validation Feedback**: Immediate input validation
- **History Management**: Easy access to previous learning paths

## 🔄 Modes of Operation

### Full Integration Mode
- YouTube video search and playlist creation
- Google Drive document creation
- Notion page creation
- Complete learning path with all resources

### YouTube-Only Mode
- YouTube video recommendations
- Structured learning path without documents
- Fallback when other tools are unavailable
- Still provides comprehensive learning content

## 🚀 Performance Optimizations

- **Async Operations**: Non-blocking tool interactions
- **Caching**: Efficient result storage and retrieval
- **Memory Management**: Proper cleanup of resources
- **Error Recovery**: Graceful handling of failures

## 🔒 Security Features

- **API Key Protection**: Secure input fields
- **URL Validation**: Comprehensive URL format checking
- **Error Sanitization**: Safe error message display
- **Session Management**: Secure state handling

## 📈 Future Enhancements

- [ ] **Export Options**: PDF, Word, or Markdown export
- [ ] **Social Sharing**: Share learning paths on social media
- [ ] **Progress Tracking**: Track actual learning progress
- [ ] **Collaborative Learning**: Share paths with others
- [ ] **Advanced Analytics**: Learning path effectiveness metrics
- [ ] **Mobile App**: Native mobile application
- [ ] **Offline Mode**: Work without internet connection
- [ ] **Custom Templates**: User-defined learning path templates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**"Invalid API Key" Error**
- Ensure your Google AI Studio API key starts with "AI"
- Check that the key is valid and has proper permissions

**"Tool Not Available" Error**
- Verify your Pipedream URLs are correct
- Check that your Pipedream workflows are properly configured
- Ensure the workflows have the necessary permissions

**"No Results Generated" Error**
- Try a simpler learning goal
- Check your internet connection
- Verify all required fields are filled

**Performance Issues**
- Close other applications to free up memory
- Check your internet connection speed
- Try generating a shorter learning path

## 📞 Support

For support and questions:
- Check the troubleshooting section above
- Review the Pipedream documentation for integration setup
- Open an issue on the GitHub repository

---

**🎓 Happy Learning!** This tool is designed to make your learning journey more structured, engaging, and effective.
