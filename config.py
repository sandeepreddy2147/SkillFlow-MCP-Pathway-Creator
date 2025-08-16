"""
Configuration settings for the MCP Learning Path Generator
"""

# Model Configuration
MODEL_CONFIG = {
    "model_name": "gemini-2.5-flash",
    "temperature": 0.7,
    "max_tokens": 4000,
    "recursion_limit": 100
}

# UI Configuration
UI_CONFIG = {
    "page_title": "MCP Learning Path Generator",
    "page_icon": "🎓",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Validation Configuration
VALIDATION_CONFIG = {
    "api_key_prefix": "AI",
    "url_patterns": {
        "pipedream": r"^https://[a-zA-Z0-9-]+\.pipedream\.net/.*$",
        "general": r"^https?://.*$"
    }
}

# Tool Configuration
TOOL_CONFIG = {
    "youtube": {
        "required": True,
        "name": "YouTube",
        "description": "Video search and playlist creation"
    },
    "drive": {
        "required": False,
        "name": "Google Drive",
        "description": "Document creation and storage"
    },
    "notion": {
        "required": False,
        "name": "Notion",
        "description": "Page creation and organization"
    }
}

# Progress Configuration
PROGRESS_CONFIG = {
    "steps": {
        "setup": 0.1,
        "integration": 0.2,
        "tools": 0.4,
        "mode": 0.5,
        "generation": 0.6,
        "complete": 1.0
    }
}

# Example Learning Goals
EXAMPLE_GOALS = [
    "I want to learn Python basics in 3 days",
    "I want to learn data science fundamentals in 10 days",
    "I want to learn web development with React in 2 weeks",
    "I want to learn machine learning basics in 5 days",
    "I want to learn JavaScript for beginners in 7 days",
    "I want to learn SQL database management in 4 days"
]

# Error Messages
ERROR_MESSAGES = {
    "api_key_missing": "❌ Please enter your Google AI Studio API key",
    "api_key_invalid": "❌ Invalid API key format",
    "youtube_url_missing": "❌ YouTube URL is required",
    "youtube_url_invalid": "❌ Invalid YouTube URL format",
    "drive_url_missing": "❌ Please enter your Pipedream Drive URL",
    "notion_url_missing": "❌ Please enter your Pipedream Notion URL",
    "goal_missing": "❌ Please enter your learning goal",
    "tool_unavailable": "❌ Tool is not available",
    "generation_failed": "❌ No results were generated. Please try again."
}

# Success Messages
SUCCESS_MESSAGES = {
    "generation_complete": "🎉 Learning path generated successfully!",
    "setup_complete": "✅ Setup complete! Starting to generate learning path...",
    "tools_available": "✅ Available tools detected"
}

# CSS Styles
CSS_STYLES = """
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #ffe6e6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff4444;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e6ffe6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #44ff44;
        margin: 1rem 0;
    }
    .tool-status {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin: 0.25rem;
    }
    .tool-available {
        background-color: #d4edda;
        color: #155724;
    }
    .tool-unavailable {
        background-color: #f8d7da;
        color: #721c24;
    }
</style>
""" 