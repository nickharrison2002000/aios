"""
Permission Manager - Full unrestricted access
"""

class PermissionManager:
    """Manages permissions for tool access."""
    
    def __init__(self, workspace: str):
        """Initialize permission manager."""
        self.workspace = workspace
        self.unrestricted = True

    def check_tool(self, tool_name: str, args: dict) -> tuple:
        """Check if tool is allowed. Always returns True."""
        if self.unrestricted:
            return (True, "FULL_ACCESS")
        return (True, "ALLOWED")
