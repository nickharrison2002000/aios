"""
LLM Client - FULL FEATURED with Custom Jinja2 Filters
Includes validation, error handling, exploitation-specific formatting
OPTIMIZED: Streaming mode + KV cache reuse
NO TRUNCATION - FULL OUTPUT
"""
import re
import json
import sys
from jinja2 import Environment, FileSystemLoader, pass_environment
from llama_cpp import Llama

class LLMClient:
    def __init__(self, model_path: str, ctx: int = 4096, n_threads: int = 12, n_gpu_layers: int = -1):
        """Initialize LLM client with streaming and KV cache support."""
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=n_gpu_layers,
            n_ctx=ctx,
            n_threads=n_threads,
            verbose=False
        )
        self.ctx_size = ctx
        self.max_ctx = 262144
        
        # KV cache management
        self.kv_cache = None
        self.use_kv_cache = True
        
        # Setup Jinja2 template environment with custom filters
        try:
            template_env = Environment(
                loader=FileSystemLoader('/root/aios2'),
                trim_blocks=True,
                lstrip_blocks=True
            )
            
            # Add custom filters
            template_env.filters['validate_json'] = self._filter_validate_json
            template_env.filters['format_tool_call'] = self._filter_format_tool_call
            template_env.filters['safe_string'] = self._filter_safe_string
            
            # Add custom globals
            template_env.globals['raise_exception'] = self._raise_exception
            
            self.template = template_env.get_template('AIOS_TEMPLATE.jinja2')
            print("✅ AIOS template loaded successfully with custom filters")
        except Exception as e:
            print(f"⚠️ Failed to load AIOS template: {e}")
            print("   Using fallback prompting")
            self.template = None

    def _raise_exception(self, message: str):
        """Jinja2 global function to raise exceptions."""
        raise Exception(message)

    def _filter_validate_json(self, obj: dict) -> dict:
        """Validate and clean JSON objects."""
        if isinstance(obj, dict):
            return obj
        try:
            return json.loads(json.dumps(obj))
        except:
            return {}

    def _filter_format_tool_call(self, name: str, args: dict) -> str:
        """Format tool call for display."""
        return f"{name}({', '.join(f'{k}={v}' for k, v in args.items())})"

    def _filter_safe_string(self, text: str) -> str:
        """Escape special characters for safe display."""
        if not isinstance(text, str):
            text = str(text)
        return text.replace("<", "&lt;").replace(">", "&gt;")

    def __call__(self, messages: list, tools: dict = None) -> dict:
        """Make instance callable."""
        return self.chat(messages, tools)

    def chat(self, messages: list, tools: dict = None, stream: bool = True) -> dict:
        """Chat with model using streaming and KV cache."""
        self._check_and_adjust_context(messages)
        
        # Build prompt
        if self.template:
            try:
                prompt = self.template.render(
                    messages=messages,
                    tools=tools,
                    add_generation_prompt=True
                )
            except Exception as e:
                print(f"⚠️ Template render error: {e}")
                prompt = self._build_prompt_fallback(messages, tools)
        else:
            prompt = self._build_prompt_fallback(messages, tools)
        
        # Generate response with streaming
        if stream:
            content = self._generate_streaming(prompt)
        else:
            response = self.llm(
                prompt,
                max_tokens=8192,
                temperature=0.4,
                top_p=0.95,
                stop=["<|im_end|>", "USER:", "Task>"]
            )
            content = response["choices"][0]["text"].strip()
        
        # Extract thinking
        thinking = ""
        if "<think>" in content:
            think_match = re.search(r'<think>(.*?)</think>', content, re.DOTALL)
            if think_match:
                thinking = think_match.group(1).strip()
                content = content.replace(think_match.group(0), "").strip()
        
        # Extract tool calls
        tool_calls = self._extract_tool_calls(content)
        
        return {
            "content": content,
            "thinking": thinking,
            "tool_calls": tool_calls
        }

    def _generate_streaming(self, prompt: str) -> str:
        """
        Generate response with streaming.
        Tokens appear in real-time, improving perceived speed.
        """
        content = ""
        print("\n📝 LLM RESPONSE (streaming):\n", end="", flush=True)
        
        for chunk in self.llm(
            prompt,
            max_tokens=8192,
            temperature=0.4,
            top_p=0.95,
            stop=["<|im_end|>", "USER:", "Task>"],
            stream=True
        ):
            token = chunk["choices"][0]["text"]
            content += token
            print(token, end="", flush=True)
        
        print("\n")  # Newline after streaming completes
        return content.strip()

    def _check_and_adjust_context(self, messages: list):
        """Monitor context usage - NO ACTION, JUST REPORT."""
        total_chars = sum(len(m.get("content", "")) for m in messages)
        estimated_tokens = int(total_chars / 4) + 500
        usage_percent = (estimated_tokens / self.ctx_size) * 100
        
        if usage_percent > 90:
            print(f"⚠️ Context usage: {usage_percent:.1f}%")

    def _build_prompt_fallback(self, messages: list, tools: dict = None) -> str:
        """Fallback prompt building."""
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user").upper()
            content = msg.get("content", "")
            prompt += f"{role}:\n{content}\n\n"
        
        if tools:
            prompt += "TOOLS:\n"
            for tool_name in tools.keys():
                prompt += f"- {tool_name}\n"
            prompt += "\n"
        
        prompt += "ASSISTANT:\n"
        return prompt

    def _extract_tool_calls(self, text: str) -> list:
        """Extract tool calls from response."""
        tool_calls = []
        matches = re.findall(r'<tool_call>\s*(.*?)\s*</tool_call>', text, re.DOTALL)
        
        for match in matches:
            block = match.strip()
            block = re.sub(r'^```json\s*', '', block)
            block = re.sub(r'```$', '', block)
            block = block.strip()
            
            try:
                tool_json = json.loads(block)
                if "name" in tool_json:
                    tool_calls.append({
                        "id": f"tool_{len(tool_calls)}",
                        "function": {
                            "name": tool_json["name"],
                            "arguments": json.dumps(tool_json.get("arguments", {}))
                        }
                    })
            except json.JSONDecodeError as e:
                print(f"⚠️ Failed to parse tool JSON: {e}")
        
        return tool_calls
