"""
Decorator for marking and configuring functions as tools for OpenAI's function calling.
"""

def tool(name=None, description=None):
    """
    Decorator to mark a function as an OpenAI tool and add metadata.
    
    Args:
        name (str, optional): Custom name for the tool. Defaults to the function name.
        description (str, optional): Description of what the tool does. 
                                     Defaults to the function docstring.
    
    Returns:
        callable: The decorated function with added tool metadata
    """
    def decorator(func):
        # Mark this function as a tool
        func._is_tool = True
        
        # Set tool name (use function name if not specified)
        func._tool_name = name or func.__name__
        
        # Set tool description (use docstring if not specified)
        func._tool_description = description or func.__doc__
        
        # Function to convert the tool to the OpenAI format
        def to_openai_tool():
            """Convert this function to the OpenAI tool format."""
            if not hasattr(func, '_tool_params'):
                raise AttributeError(f"Tool function {func.__name__} is missing '_tool_params' attribute")
                
            return {
                "type": "function",
                "function": {
                    "name": func._tool_name,
                    "description": func._tool_description,
                    "parameters": func._tool_params
                }
            }
        
        # Attach the conversion method to the function
        func.to_openai_tool = to_openai_tool
        
        return func
    return decorator

def get_tool_definition(func):
    """
    Helper function to get the OpenAI tool definition from a decorated function.
    
    Args:
        func: A function decorated with @tool
        
    Returns:
        dict: The OpenAI tool definition
    """
    if not hasattr(func, '_is_tool') or not func._is_tool:
        raise ValueError(f"Function {func.__name__} is not marked as a tool")
    
    return {
        "type": "function",
		"name": func._tool_name,
		"description": func._tool_description,
		"parameters": func._tool_params
    }

def create_tools_list(funcs):
    """
    Convert a list of tool functions to OpenAI tools format.
    
    Args:
        funcs: List of functions decorated with @tool
        
    Returns:
        list: List of OpenAI tool definitions
    """
    return [get_tool_definition(func) for func in funcs]