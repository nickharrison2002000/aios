"""
Tool definitions for AIOS agent
Includes go_back_to_phase tool for phase management
NO TRUNCATION - FULL OUTPUT FOR ALL RESULTS
"""
import subprocess
import os
import json

def execute_bash(command: str, cwd: str = "/root") -> str:
    """Execute bash command with full output capture - NO TRUNCATION."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout + result.stderr
        return output if output else "(command executed successfully with no output)"
    except subprocess.TimeoutExpired:
        return "TIMEOUT: Command execution exceeded 120 seconds"
    except Exception as e:
        return f"ERROR executing command: {str(e)}"

def read_file(path: str) -> str:
    """Read and return complete file contents - NO TRUNCATION."""
    try:
        if not os.path.isfile(path):
            return f"ERROR: File not found: {path}"
        with open(path, 'r', errors='ignore') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"ERROR reading file: {str(e)}"

def write_file(path: str, content: str) -> str:
    """Write content to file, creating directories as needed."""
    try:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return f"✓ Successfully written to {path} ({len(content)} bytes)"
    except Exception as e:
        return f"ERROR writing file: {str(e)}"

def edit_file(path: str, old_string: str, new_string: str) -> str:
    """Edit file by replacing first occurrence of old_string with new_string."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        if old_string not in content:
            return f"ERROR: String not found in file: {path}"
        new_content = content.replace(old_string, new_string, 1)
        with open(path, 'w') as f:
            f.write(new_content)
        return f"✓ Successfully edited {path}"
    except Exception as e:
        return f"ERROR editing file: {str(e)}"

def list_directory(directory: str) -> str:
    """List directory contents with file/directory indicators - NO TRUNCATION."""
    try:
        if not os.path.isdir(directory):
            return f"ERROR: Directory not found: {directory}"
        items = os.listdir(directory)
        output = f"Directory: {directory}\n"
        output += f"Total items: {len(items)}\n\n"
        for item in sorted(items):
            path = os.path.join(directory, item)
            if os.path.isdir(path):
                output += f"  [DIR]  {item}/\n"
            else:
                size = os.path.getsize(path)
                output += f"  [FILE] {item} ({size} bytes)\n"
        return output
    except Exception as e:
        return f"ERROR listing directory: {str(e)}"

def search_files(directory: str, pattern: str) -> str:
    """Search for pattern in files recursively - NO TRUNCATION."""
    try:
        if not os.path.isdir(directory):
            return f"ERROR: Directory not found: {directory}"
        results = []
        matches_found = 0
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if pattern.lower() in line.lower():
                                results.append(f"{filepath}:{line_num}: {line.strip()}")
                                matches_found += 1
                except:
                    pass
        if results:
            return '\n'.join(results) + f"\n\n(Found {matches_found} matches)"
        else:
            return f"No matches found for pattern: {pattern}"
    except Exception as e:
        return f"ERROR searching files: {str(e)}"

def web_request(url: str, method: str = "GET") -> str:
    """Make HTTP request and return response content - NO TRUNCATION."""
    try:
        import urllib.request
        import urllib.error
        req = urllib.request.Request(url, method=method)
        req.add_header('User-Agent', 'AIOS-Agent/1.0')
        response = urllib.request.urlopen(req, timeout=30)
        content = response.read().decode('utf-8', errors='ignore')
        return content
    except Exception as e:
        return f"ERROR making web request: {str(e)}"

def advance_phase(current_phase: str) -> str:
    """
    Advance to the next exploitation phase.
    Called by LLM when ready to move from current phase to next.
    Updates the system prompt to the new phase's instructions.
    
    Required argument:
    - current_phase (str): The phase you are currently in
    """
    return f"Phase advancement requested: {current_phase}"

def go_back_to_phase(target_phase: str) -> str:
    """
    Jump back to a specific phase for debugging/retesting.
    Useful when you need to restart from an earlier phase.
    
    Required argument:
    - target_phase (str): The phase to jump to (research, fuzz, vuln_analysis, exploit, iterate, verify)
    """
    return f"Jump to phase requested: {target_phase}"

def mark_done(summary: str) -> str:
    """
    Mark task as complete with summary.
    
    Required argument:
    - summary (str): Summary of success and proof of exploitation
    """
    return f"TASK_COMPLETE: {summary}"

# Tool registry
TOOL_MAP = {
    "execute_bash": execute_bash,
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "list_directory": list_directory,
    "search_files": search_files,
    "web_request": web_request,
    "advance_phase": advance_phase,
    "go_back_to_phase": go_back_to_phase,
    "mark_done": mark_done,
}

# Tool schema for LLM - EXACT PARAMETER NAMES
TOOL_SCHEMA = {
    "execute_bash": {
        "description": "Execute bash command on system",
        "parameters": {
            "command": "str - the bash command to execute",
            "cwd": "str (optional) - working directory, default /root"
        }
    },
    "read_file": {
        "description": "Read and return complete file contents (no truncation)",
        "parameters": {
            "path": "str - full path to file"
        }
    },
    "write_file": {
        "description": "Write content to file, creating directories as needed",
        "parameters": {
            "path": "str - full path to file",
            "content": "str - content to write"
        }
    },
    "edit_file": {
        "description": "Edit file by replacing first occurrence of old_string with new_string",
        "parameters": {
            "path": "str - full path to file",
            "old_string": "str - text to find and replace",
            "new_string": "str - replacement text"
        }
    },
    "list_directory": {
        "description": "List directory contents with file/directory indicators",
        "parameters": {
            "directory": "str - full path to directory"
        }
    },
    "search_files": {
        "description": "Search for pattern in files recursively",
        "parameters": {
            "directory": "str - directory to search",
            "pattern": "str - pattern to search for"
        }
    },
    "web_request": {
        "description": "Make HTTP request and return response",
        "parameters": {
            "url": "str - URL to request",
            "method": "str (optional) - HTTP method, default GET"
        }
    },
    "advance_phase": {
        "description": "Advance to next exploitation phase. Call when ready to move from current phase to next.",
        "parameters": {
            "current_phase": "str - the phase you are currently in"
        }
    },
    "go_back_to_phase": {
        "description": "Jump back to a specific phase for debugging/retesting",
        "parameters": {
            "target_phase": "str - the phase to jump to (research|fuzz|vuln_analysis|exploit|iterate|verify)"
        }
    },
    "mark_done": {
        "description": "Mark task complete with proof of exploitation",
        "parameters": {
            "summary": "str - summary of success and proof"
        }
    }
}
