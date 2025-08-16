from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from prompt import user_goal_prompt
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional, Tuple, Any, Callable, Dict, List
import asyncio
import re
import json

cfg = RunnableConfig(recursion_limit=100)

def initialize_model(google_api_key: str) -> ChatGoogleGenerativeAI:
    """Initialize the Google Generative AI model with enhanced configuration."""
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key,
        temperature=0.7,
        max_tokens=4000
    )

def validate_url(url: str) -> bool:
    """Validate if a URL is properly formatted."""
    if not url:
        return False
    # Basic URL validation
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(url_pattern.match(url))

def extract_tool_names(tools: List[Dict]) -> List[str]:
    """Extract tool names from the tools list."""
    tool_names = []
    for tool in tools:
        if 'name' in tool:
            tool_names.append(tool['name'])
    return tool_names

async def setup_agent_with_tools(
    google_api_key: str,
    youtube_pipedream_url: str,
    drive_pipedream_url: Optional[str] = None,
    notion_pipedream_url: Optional[str] = None,
    progress_callback: Optional[Callable[[str], None]] = None
) -> Tuple[Any, Dict[str, Any]]:
    """
    Set up the agent with YouTube (mandatory) and optional Drive or Notion tools.
    Returns the agent and a status report.
    """
    status_report = {
        "youtube_available": False,
        "drive_available": False,
        "notion_available": False,
        "available_tools": [],
        "errors": []
    }
    
    try:
        if progress_callback:
            progress_callback("Setting up agent with tools... ✅")
        
        # Validate YouTube URL (mandatory)
        if not validate_url(youtube_pipedream_url):
            raise ValueError("Invalid YouTube Pipedream URL provided")
        
        # Initialize tools configuration with mandatory YouTube
        tools_config = {
            "youtube": {
                "url": youtube_pipedream_url,
                "transport": "streamable_http"
            }
        }

        # Add Drive if URL provided and valid
        if drive_pipedream_url and validate_url(drive_pipedream_url):
            tools_config["drive"] = {
                "url": drive_pipedream_url,
                "transport": "streamable_http"
            }
            if progress_callback:
                progress_callback("Added Google Drive integration... ✅")

        # Add Notion if URL provided and valid
        if notion_pipedream_url and validate_url(notion_pipedream_url):
            tools_config["notion"] = {
                "url": notion_pipedream_url,
                "transport": "streamable_http"
            }
            if progress_callback:
                progress_callback("Added Notion integration... ✅")

        if progress_callback:
            progress_callback("Initializing MCP client... ✅")
        
        # Initialize MCP client with configured tools
        mcp_client = MultiServerMCPClient(tools_config)
        
        if progress_callback:
            progress_callback("Getting available tools... ✅")
        
        # Get all tools and validate them
        tools = await mcp_client.get_tools()
        tool_names = extract_tool_names(tools)
        status_report["available_tools"] = tool_names
        
        # Check which tools are actually available
        youtube_tools = [tool for tool in tool_names if 'youtube' in tool.lower()]
        drive_tools = [tool for tool in tool_names if 'drive' in tool.lower() or 'google' in tool.lower()]
        notion_tools = [tool for tool in tool_names if 'notion' in tool.lower()]
        
        status_report["youtube_available"] = len(youtube_tools) > 0
        status_report["drive_available"] = len(drive_tools) > 0
        status_report["notion_available"] = len(notion_tools) > 0
        
        if progress_callback:
            progress_callback(f"Available tools: {', '.join(tool_names)}")
        
        if progress_callback:
            progress_callback("Creating AI agent... ✅")
        
        # Create agent with initialized model
        mcp_orch_model = initialize_model(google_api_key)
        agent = create_react_agent(mcp_orch_model, tools)
        
        if progress_callback:
            progress_callback("Setup complete! Starting to generate learning path... ✅")
        
        return agent, status_report
        
    except Exception as e:
        error_msg = f"Error in setup_agent_with_tools: {str(e)}"
        status_report["errors"].append(error_msg)
        print(error_msg)
        raise

def create_fallback_prompt(user_goal: str, available_tools: List[str]) -> str:
    """Create a fallback prompt when document creation tools are unavailable."""
    base_prompt = f"""
User Goal: {user_goal}

Since document creation tools are not available, please create a comprehensive learning path with the following:

1. **Day-wise Learning Structure**: Break down the learning goal into manageable daily topics
2. **YouTube Video Recommendations**: For each day, recommend 2-3 high-quality YouTube videos
3. **Learning Objectives**: Clear objectives for each day
4. **Practice Suggestions**: Simple exercises or projects for each day
5. **Progress Tracking**: How to measure progress for each day

Format the response as:
# Learning Path: [Topic]

## Day 1: [Topic]
**Learning Objectives:**
- [Objective 1]
- [Objective 2]

**Recommended Videos:**
1. [Video Title] - [URL]
2. [Video Title] - [URL]

**Practice Exercise:**
[Description of what to practice]

[Continue for each day...]

**Additional Resources:**
- [Recommended channels/websites]
"""
    return base_prompt

def run_agent_sync(
    google_api_key: str,
    youtube_pipedream_url: str,
    drive_pipedream_url: Optional[str] = None,
    notion_pipedream_url: Optional[str] = None,
    user_goal: str = "",
    progress_callback: Optional[Callable[[str], None]] = None
) -> dict:
    """
    Synchronous wrapper for running the agent with enhanced error handling.
    """
    async def _run():
        try:
            agent, status_report = await setup_agent_with_tools(
                google_api_key=google_api_key,
                youtube_pipedream_url=youtube_pipedream_url,
                drive_pipedream_url=drive_pipedream_url,
                notion_pipedream_url=notion_pipedream_url,
                progress_callback=progress_callback
            )
            
            # Determine which prompt to use based on available tools
            if status_report["drive_available"] or status_report["notion_available"]:
                # Use full prompt with document creation
                learning_path_prompt = "User Goal: " + user_goal + "\n" + user_goal_prompt
                if progress_callback:
                    progress_callback("Using full learning path generation with document creation...")
            else:
                # Use fallback prompt for YouTube-only functionality
                learning_path_prompt = create_fallback_prompt(user_goal, status_report["available_tools"])
                if progress_callback:
                    progress_callback("Using YouTube-only learning path generation...")
            
            if progress_callback:
                progress_callback("Generating your learning path...")
            
            # Run the agent
            result = await agent.ainvoke(
                {"messages": [HumanMessage(content=learning_path_prompt)]},
                config=cfg
            )
            
            if progress_callback:
                progress_callback("Learning path generation complete!")
            
            # Add status report to result
            result["status_report"] = status_report
            return result
            
        except Exception as e:
            error_msg = f"Error in _run: {str(e)}"
            print(error_msg)
            raise

    # Run in new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_run())
    finally:
        loop.close()

def format_learning_path_result(result: dict) -> str:
    """Format the learning path result for better display."""
    if not result or "messages" not in result:
        return "No results were generated. Please try again."
    
    formatted_result = ""
    for msg in result["messages"]:
        content = msg.content
        # Clean up the content for better display
        content = content.replace("📚", "").strip()
        formatted_result += f"{content}\n\n"
    
    return formatted_result
