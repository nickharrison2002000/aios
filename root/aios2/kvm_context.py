"""
KVM Context Manager - Loads KVM header files
"""
import os

class KVMContext:
    """Loads and manages KVM header files for LLM context."""
    
    def __init__(self, project_root: str):
        """Initialize KVM context manager."""
        self.project_root = project_root
        self.kvm_dir = os.path.join(project_root, "kvm")
        self.guest_dir = os.path.join(self.kvm_dir, "guest")
        self.host_dir = os.path.join(self.kvm_dir, "host")
        self.loaded_headers = {}
        
    def load_header(self, header_name: str, is_host: bool = False) -> str:
        """Load a single header file."""
        directory = self.host_dir if is_host else self.guest_dir
        header_path = os.path.join(directory, header_name)
        
        if os.path.isfile(header_path):
            with open(header_path, "r") as f:
                content = f.read()
            self.loaded_headers[header_name] = content
            return content
        return ""
    
    def load_all_headers(self, is_host: bool = False) -> dict:
        """Load all headers from guest or host directory."""
        directory = self.host_dir if is_host else self.guest_dir
        headers = {}
        
        if os.path.isdir(directory):
            for filename in os.listdir(directory):
                if filename.endswith(".h"):
                    filepath = os.path.join(directory, filename)
                    try:
                        with open(filepath, "r") as f:
                            headers[filename] = f.read()
                        self.loaded_headers[filename] = headers[filename]
                    except:
                        pass
        
        return headers
    
    def get_context_summary(self) -> str:
        """Get summary of available KVM headers."""
        summary = "KVM Headers Available:\n"
        summary += f"  Loaded: {len(self.loaded_headers)} files\n"
        for name in sorted(self.loaded_headers.keys()):
            summary += f"  - {name}\n"
        return summary
