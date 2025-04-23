"""
Command-line interface for Multi Tool Agent
"""
import sys
import argparse
import json
import logging
from typing import Dict, Any, List, Optional

from .agent import MultiToolAgent
from .tools import registry
from .config import config

def setup_logging(log_level: str = None) -> None:
    """
    Set up logging configuration
    
    Args:
        log_level: The logging level to use
    """
    if log_level is None:
        log_level = config.get("LOG_LEVEL", "INFO")
        
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO
        
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=numeric_level
    )

def create_agent() -> MultiToolAgent:
    """
    Create and configure agent with all registered tools
    
    Returns:
        Configured MultiToolAgent instance
    """
    agent = MultiToolAgent()
    
    # Add all tools from registry
    for tool_name in registry.list_tools():
        tool_info = registry.get_tool(tool_name)
        tool_function = tool_info["function"]
        tool_metadata = tool_info["metadata"]
        
        # Create Tool instance and add to agent
        from .agent import Tool
        tool = Tool(
            name=tool_name,
            function=tool_function,
            description=tool_metadata.description
        )
        agent.add_tool(tool)
        
    return agent

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments
    
    Returns:
        Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(description="Multi Tool Agent CLI")
    
    parser.add_argument(
        "task",
        nargs="?",
        help="Task description for the agent"
    )
    
    parser.add_argument(
        "--config",
        "-c",
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--log-level",
        "-l",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level"
    )
    
    parser.add_argument(
        "--tool",
        "-t",
        help="Specify a specific tool to use"
    )
    
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List all available tools"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )
    
    return parser.parse_args()

def main() -> None:
    """Main entry point for CLI"""
    args = parse_args()
    
    # Configure logging
    setup_logging(args.log_level)
    
    # Load custom configuration if specified
    if args.config:
        from .config import Config
        config = Config(args.config)
    
    # List available tools if requested
    if args.list_tools:
        tool_descriptions = registry.get_tool_descriptions()
        print("Available tools:")
        for name, description in tool_descriptions.items():
            print(f"  - {name}: {description}")
        return
    
    # Create agent
    agent = create_agent()
    
    # Run task if provided
    if args.task:
        result = agent.run(args.task)
        
        # Format and display output
        if args.output == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"Task: {result['task']}")
            print(f"Status: {result['status']}")
            print(f"Tools used: {', '.join(result['tools_used']) if result['tools_used'] else 'None'}")
            print(f"Result: {result['result']}")
    else:
        # Interactive mode if no task provided
        print("Multi Tool Agent Interactive Mode")
        print("Type 'exit' or 'quit' to exit")
        print("Type 'tools' to list available tools")
        
        while True:
            try:
                task = input("\nEnter task: ")
                if task.lower() in ("exit", "quit"):
                    break
                elif task.lower() == "tools":
                    tool_descriptions = registry.get_tool_descriptions()
                    print("Available tools:")
                    for name, description in tool_descriptions.items():
                        print(f"  - {name}: {description}")
                    continue
                    
                result = agent.run(task)
                
                # Format and display output
                if args.output == "json":
                    print(json.dumps(result, indent=2))
                else:
                    print(f"Status: {result['status']}")
                    print(f"Tools used: {', '.join(result['tools_used']) if result['tools_used'] else 'None'}")
                    print(f"Result: {result['result']}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()