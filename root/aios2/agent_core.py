"""
AIOS Agent Core - FIXED with Phase Control
- Proper tool extraction from JSON
- go_back_to_PHASE tool for debugging
- Better phase management
- Full output, no truncation
"""
import json
import os
import re
from llm_client import LLMClient
from tools import TOOL_MAP, TOOL_SCHEMA
from permissions import PermissionManager

class Agent:
    """Single agent for full exploitation lifecycle."""
    
    def __init__(self, project_dir: str, llm_client: LLMClient, prompts_dir: str = None, state_file: str = None):
        """Initialize agent."""
        self.pm = PermissionManager(project_dir)
        self.llm = llm_client
        self.workspace = project_dir
        self.prompts_dir = prompts_dir
        
        # Phase tracking
        self.phases = ["research", "fuzz", "vuln_analysis", "exploit", "iterate", "verify"]
        self.current_phase = "research"
        self.phase_index = 0
        
        # Load initial prompt
        self.base_system_prompt = self._load_prompt("sys_prompt.md")
        self.current_system_prompt = self.base_system_prompt
        
        # Metrics
        self.max_iterations = 25
        self.iteration_count = 0
        self.tool_call_count = 0

    def _load_prompt(self, filename: str) -> str:
        """Load prompt from sys/prompts/"""
        if not self.prompts_dir:
            return ""
        path = os.path.join(self.prompts_dir, filename)
        if os.path.isfile(path):
            with open(path, "r") as f:
                return f.read()
        return ""

    def _get_phase_prompt(self, phase_name: str) -> str:
        """Get prompt for specific phase."""
        prompt_map = {
            "research": "sys_prompt.md",
            "fuzz": "fuzz_prompt.md",
            "vuln_analysis": "vuln_analysis_prompt.md",
            "exploit": "proof_of_concept_prompt.md",
            "iterate": "iterate_refine_prompt.md",
            "verify": "verify_success_prompt.md",
        }
        filename = prompt_map.get(phase_name, "sys_prompt.md")
        return self._load_prompt(filename)

    def advance_phase(self, current_phase: str) -> str:
        """Advance to next phase."""
        try:
            idx = self.phases.index(current_phase)
            if idx < len(self.phases) - 1:
                next_phase = self.phases[idx + 1]
                self.current_phase = next_phase
                self.phase_index = idx + 1
                new_prompt = self._get_phase_prompt(next_phase)
                if new_prompt:
                    self.current_system_prompt = new_prompt
                print(f"\n⏭️  PHASE ADVANCED: {current_phase} → {next_phase}\n")
                return f"✅ Advanced to: {next_phase}"
            else:
                return f"✅ All phases complete"
        except ValueError:
            return f"❌ Unknown phase: {current_phase}"

    def go_back_to_phase(self, target_phase: str) -> str:
        """Jump back to a specific phase for debugging."""
        if target_phase not in self.phases:
            return f"❌ Unknown phase: {target_phase}. Available: {', '.join(self.phases)}"
        
        self.current_phase = target_phase
        self.phase_index = self.phases.index(target_phase)
        new_prompt = self._get_phase_prompt(target_phase)
        if new_prompt:
            self.current_system_prompt = new_prompt
        
        print(f"\n⏪ JUMPED BACK TO PHASE: {target_phase}\n")
        return f"✅ Returned to phase: {target_phase}"

    def run(self, task_prompt: str):
        """Execute task through phases."""
        print(f"\n🎯 Task: {task_prompt}")
        print("=" * 80)
        
        messages = [
            {"role": "system", "content": self.current_system_prompt},
            {"role": "user", "content": task_prompt}
        ]
        
        self.iteration_count = 0
        task_complete = False
        
        while self.iteration_count < self.max_iterations and not task_complete:
            self.iteration_count += 1
            print(f"\n[Iteration {self.iteration_count}/{self.max_iterations}] Phase: {self.current_phase}")
            print("-" * 80)
            
            try:
                response = self.llm(messages, TOOL_SCHEMA)
            except Exception as e:
                print(f"❌ LLM error: {e}")
                break
            
            content = response.get("content", "")
            if not content:
                print("❌ Empty response from LLM")
                break
            
            # Show FULL response (no truncation)
            print(f"\n📝 LLM RESPONSE:\n{content}\n")
            
            # Strip thinking tags
            thinking = ""
            response_content = content
            if "<think>" in content:
                match = re.search(r'<think>(.*?)</think>', content, re.DOTALL)
                if match:
                    thinking = match.group(1).strip()
                    response_content = content.replace(match.group(0), "").strip()
            
            # Add to messages
            messages.append({"role": "assistant", "content": content})
            
            # Extract and execute tools
            tool_calls = self._extract_tool_calls(response_content)
            
            if tool_calls:
                print(f"🔧 TOOL CALLS FOUND: {len(tool_calls)}\n")
                
                for i, tc in enumerate(tool_calls):
                    name = tc.get("name", "unknown")
                    args = tc.get("arguments", {})
                    
                    print(f"[{i+1}/{len(tool_calls)}] {name}")
                    print(f"  Args: {args}")
                    
                    result = self._execute_tool(name, args)
                    
                    print(f"  Result: {result[:200]}{'...' if len(result) > 200 else ''}\n")
                    
                    messages.append({
                        "role": "tool",
                        "content": result,
                        "name": name
                    })
                    
                    self.tool_call_count += 1
                
                # Window messages
                if len(messages) > 22:
                    messages = [messages[0]] + messages[-20:]
            else:
                print("⚠️ NO TOOLS FOUND - Pushing LLM to act\n")
                messages.append({
                    "role": "user",
                    "content": "You MUST call a tool now. Choose from the 8 tools available."
                })
            
            # Check for task completion
            if "TASK_COMPLETE" in content.upper() or "mark_done" in content.lower():
                print(f"\n✅ TASK COMPLETE")
                task_complete = True

        print("\n" + "=" * 80)
        print(f"📊 SUMMARY:")
        print(f"   Iterations: {self.iteration_count}/{self.max_iterations}")
        print(f"   Tool calls: {self.tool_call_count}")
        print(f"   Final phase: {self.current_phase}")

    def _extract_tool_calls(self, text: str) -> list:
        """Extract tool calls from response - FIXED JSON parsing."""
        tool_calls = []
        
        # Find <tool_call>...</tool_call> blocks
        matches = re.findall(r'<tool_call>\s*(.*?)\s*</tool_call>', text, re.DOTALL)
        
        for match in matches:
            block = match.strip()
            
            # Remove markdown code blocks
            block = re.sub(r'^```json\s*', '', block)
            block = re.sub(r'```$', '', block)
            block = block.strip()
            
            try:
                tool_json = json.loads(block)
                
                if "name" not in tool_json:
                    continue
                
                tool_calls.append({
                    "name": tool_json["name"],
                    "arguments": tool_json.get("arguments", {})
                })
                
            except json.JSONDecodeError as e:
                print(f"⚠️ Failed to parse JSON: {e}")
        
        return tool_calls

    def _execute_tool(self, name: str, args: dict) -> str:
        """Execute a tool."""
        try:
            # Check permissions
            allowed, reason = self.pm.check_tool(name, args)
            if not allowed:
                return f"ERROR: Denied - {reason}"
            
            # Handle phase control specially
            if name == "advance_phase":
                current = args.get("current_phase", self.current_phase)
                return self.advance_phase(current)
            
            if name == "go_back_to_phase":
                target = args.get("target_phase", "")
                return self.go_back_to_phase(target)
            
            # Execute tool
            if name not in TOOL_MAP:
                return f"ERROR: Unknown tool '{name}'"
            
            func = TOOL_MAP[name]
            result = func(**args)
            return str(result)
            
        except TypeError as e:
            return f"ERROR: {name} - wrong arguments - {str(e)}"
        except Exception as e:
            return f"ERROR: {name} - {str(e)}"
