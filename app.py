import streamlit as st
from utils import run_agent_sync, format_learning_path_result, validate_url
import time

st.set_page_config(
    page_title="MCP Learning Path Generator", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
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
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🎓 MCP Learning Path Generator</h1>
    <p>Create personalized learning paths using AI and external tools</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = ""
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'last_section' not in st.session_state:
    st.session_state.last_section = ""
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False
if 'status_report' not in st.session_state:
    st.session_state.status_report = {}
if 'result_history' not in st.session_state:
    st.session_state.result_history = []

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input with validation
    google_api_key = st.text_input(
        "🔑 Google AI Studio API Key", 
        type="password",
        help="Enter your Google AI Studio API key"
    )
    
    # Validate API key format
    if google_api_key and not google_api_key.startswith("AI"):
        st.warning("⚠️ API key should start with 'AI'. Please check your key.")
    
    st.markdown("---")
    st.subheader("🔗 Pipedream URLs")
    
    # YouTube URL (required)
    youtube_pipedream_url = st.text_input(
        "📺 YouTube URL (Required)", 
        placeholder="https://your-pipedream-url.com",
        help="Pipedream webhook URL for YouTube integration"
    )
    
    # Validate YouTube URL
    if youtube_pipedream_url and not validate_url(youtube_pipedream_url):
        st.error("❌ Invalid YouTube URL format")
    
    # Secondary tool selection
    secondary_tool = st.radio(
        "🛠️ Select Secondary Tool:",
        ["Drive", "Notion", "None"],
        help="Choose which additional tool to use (optional)"
    )
    
    # Secondary tool URL input
    if secondary_tool == "Drive":
        drive_pipedream_url = st.text_input(
            "📁 Drive URL", 
            placeholder="https://your-pipedream-drive-url.com",
            help="Pipedream webhook URL for Google Drive integration"
        )
        notion_pipedream_url = None
        if drive_pipedream_url and not validate_url(drive_pipedream_url):
            st.error("❌ Invalid Drive URL format")
    elif secondary_tool == "Notion":
        notion_pipedream_url = st.text_input(
            "📝 Notion URL", 
            placeholder="https://your-pipedream-notion-url.com",
            help="Pipedream webhook URL for Notion integration"
        )
        drive_pipedream_url = None
        if notion_pipedream_url and not validate_url(notion_pipedream_url):
            st.error("❌ Invalid Notion URL format")
    else:
        drive_pipedream_url = None
        notion_pipedream_url = None
    
    # Status display
    if st.session_state.status_report:
        st.markdown("---")
        st.subheader("📊 Tool Status")
        
        status = st.session_state.status_report
        if status.get("youtube_available"):
            st.markdown('<span class="tool-status tool-available">✅ YouTube</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="tool-status tool-unavailable">❌ YouTube</span>', unsafe_allow_html=True)
            
        if status.get("drive_available"):
            st.markdown('<span class="tool-status tool-available">✅ Drive</span>', unsafe_allow_html=True)
        elif secondary_tool == "Drive":
            st.markdown('<span class="tool-status tool-unavailable">❌ Drive</span>', unsafe_allow_html=True)
            
        if status.get("notion_available"):
            st.markdown('<span class="tool-status tool-available">✅ Notion</span>', unsafe_allow_html=True)
        elif secondary_tool == "Notion":
            st.markdown('<span class="tool-status tool-unavailable">❌ Notion</span>', unsafe_allow_html=True)

# Main content area
st.header("🎯 Enter Your Learning Goal")

# Quick guide
with st.expander("📖 How to use this app", expanded=False):
    st.markdown("""
    **Step-by-step guide:**
    
    1. **Configure Tools**: Enter your Google API key and Pipedream URLs in the sidebar
    2. **Enter Goal**: Describe what you want to learn (e.g., "I want to learn Python basics in 3 days")
    3. **Generate**: Click the button to create your personalized learning path
    
    **Example Goals:**
    - "I want to learn Python basics in 3 days"
    - "I want to learn data science fundamentals in 10 days"
    - "I want to learn web development with React in 2 weeks"
    - "I want to learn machine learning basics in 5 days"
    
    **Features:**
    - 🎥 YouTube video recommendations
    - 📁 Google Drive document creation (if configured)
    - 📝 Notion page creation (if configured)
    - 📊 Progress tracking
    - 🎯 Personalized learning objectives
    """)

# User goal input
user_goal = st.text_area(
    "What do you want to learn?",
    placeholder="Example: I want to learn Python basics in 3 days",
    height=100,
    help="Describe your learning goal in detail. Be specific about the topic and timeframe."
)

# Progress area
progress_container = st.container()
progress_bar = st.empty()

def update_progress(message: str):
    """Update progress in the Streamlit UI with enhanced feedback"""
    st.session_state.current_step = message
    
    # Determine section and update progress
    if "Setting up agent with tools" in message:
        section = "Setup"
        st.session_state.progress = 0.1
    elif "Added Google Drive integration" in message or "Added Notion integration" in message:
        section = "Integration"
        st.session_state.progress = 0.2
    elif "Creating AI agent" in message:
        section = "Setup"
        st.session_state.progress = 0.3
    elif "Available tools" in message:
        section = "Tools"
        st.session_state.progress = 0.4
    elif "Using full learning path generation" in message or "Using YouTube-only learning path generation" in message:
        section = "Mode"
        st.session_state.progress = 0.5
    elif "Generating your learning path" in message:
        section = "Generation"
        st.session_state.progress = 0.6
    elif "Learning path generation complete" in message:
        section = "Complete"
        st.session_state.progress = 1.0
        st.session_state.is_generating = False
    else:
        section = st.session_state.last_section or "Progress"
    
    st.session_state.last_section = section
    
    # Show progress bar
    progress_bar.progress(st.session_state.progress)
    
    # Update progress container with current status
    with progress_container:
        # Show section header if it changed
        if section != st.session_state.last_section and section != "Complete":
            st.write(f"**{section}**")
        
        # Show message with appropriate icon
        if message == "Learning path generation complete!":
            st.success("🎉 All steps completed!")
        elif "✅" in message:
            st.info(f"✅ {message.replace('✅', '').strip()}")
        else:
            prefix = "🔄" if st.session_state.progress < 0.5 else "⚡"
            st.write(f"{prefix} {message}")

# Generate button with enhanced validation
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_button = st.button(
        "🚀 Generate Learning Path", 
        type="primary", 
        disabled=st.session_state.is_generating,
        use_container_width=True
    )

# Validation and execution
if generate_button:
    # Validate inputs
    validation_errors = []
    
    if not google_api_key:
        validation_errors.append("❌ Please enter your Google AI Studio API key")
    elif not google_api_key.startswith("AI"):
        validation_errors.append("❌ Invalid API key format")
    
    if not youtube_pipedream_url:
        validation_errors.append("❌ YouTube URL is required")
    elif not validate_url(youtube_pipedream_url):
        validation_errors.append("❌ Invalid YouTube URL format")
    
    if secondary_tool == "Drive" and not drive_pipedream_url:
        validation_errors.append("❌ Please enter your Pipedream Drive URL")
    elif secondary_tool == "Notion" and not notion_pipedream_url:
        validation_errors.append("❌ Please enter your Pipedream Notion URL")
    
    if not user_goal:
        validation_errors.append("❌ Please enter your learning goal")
    
    # Show validation errors
    if validation_errors:
        st.error("**Configuration Errors:**")
        for error in validation_errors:
            st.error(error)
    else:
        try:
            # Set generating flag
            st.session_state.is_generating = True
            
            # Reset progress
            st.session_state.current_step = ""
            st.session_state.progress = 0
            st.session_state.last_section = ""
            
            # Run the agent
            result = run_agent_sync(
                google_api_key=google_api_key,
                youtube_pipedream_url=youtube_pipedream_url,
                drive_pipedream_url=drive_pipedream_url,
                notion_pipedream_url=notion_pipedream_url,
                user_goal=user_goal,
                progress_callback=update_progress
            )
            
            # Store status report
            if "status_report" in result:
                st.session_state.status_report = result["status_report"]
            
            # Display results
            st.header("📚 Your Learning Path")
            
            if result and "messages" in result:
                # Format and display the result
                formatted_result = format_learning_path_result(result)
                
                # Display in a nice format
                st.markdown(formatted_result)
                
                # Add to history
                st.session_state.result_history.append({
                    "goal": user_goal,
                    "result": formatted_result,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                
                # Show success message
                st.success("🎉 Learning path generated successfully!")
                
                # Show tool status
                if st.session_state.status_report:
                    st.info(f"**Tools Used:** {', '.join(st.session_state.status_report.get('available_tools', []))}")
                
            else:
                st.error("❌ No results were generated. Please try again.")
                st.session_state.is_generating = False
                
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.error("Please check your API keys and URLs, and try again.")
            st.session_state.is_generating = False

# History section
if st.session_state.result_history:
    st.markdown("---")
    st.header("📜 Previous Learning Paths")
    
    for i, history_item in enumerate(reversed(st.session_state.result_history)):
        with st.expander(f"🎯 {history_item['goal']} - {history_item['timestamp']}"):
            st.markdown(history_item['result'])
            
            # Add delete button
            if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                st.session_state.result_history.pop(len(st.session_state.result_history) - 1 - i)
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    <p>🎓 MCP Learning Path Generator | Powered by Model Context Protocol</p>
    <p>Integrates with YouTube, Google Drive, and Notion for comprehensive learning experiences</p>
</div>
""", unsafe_allow_html=True)
