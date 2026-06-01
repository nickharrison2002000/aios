# AIOS - Autonomous KVM Exploitation System

An autonomous agent system for discovering, analyzing, and exploiting vulnerabilities in KVM hypervisors to achieve guest-to-host escape.

## What is AIOS?

AIOS is an AI-powered security research system that:
- Autonomously researches KVM vulnerability landscape
- Systematically fuzzes KVM interfaces to find exploitable bugs
- Analyzes crashes to identify root causes
- Develops working proof-of-concept exploits
- Iterates and refines until exploitation succeeds
- Verifies guest-to-host escape with proof

## Key Features

✅ **6-Phase Exploitation Workflow**
- Phase 1: Research & analysis
- Phase 2: Fuzzing & vulnerability discovery
- Phase 3: Root cause analysis
- Phase 4: Exploit development
- Phase 5: Iteration & refinement
- Phase 6: Verification & proof

✅ **Thinking Model Support**
- Shows complete reasoning process
- Full transparency into decision-making
- Visible analysis at each step

✅ **No Truncation**
- Complete tool output always
- Full file contents displayed
- Entire crash logs captured
- Comprehensive documentation

✅ **Tool-Driven Phase Management**
- Model controls phase transitions
- Explicit `advance_phase()` tool calls
- Clean separation between phases
- Proper context management

✅ **Autonomous Operation**
- Runs 25 iterations per phase
- Self-corrects on failures
- Tries alternative approaches
- Never stops until success

## Architecture

```
AIOS
├── main.py              # Entry point
├── agent_core.py        # Agent engine
├── llm_client.py        # LLM interface with template
├── tools.py             # Tool definitions
├── permissions.py       # Access control
├── kvm_context.py       # KVM header management
│
├── sys/
│   ├── prompts/         # 6 phase-specific prompts
│   │   ├── sys_prompt.md
│   │   ├── fuzz_prompt.md
│   │   ├── vuln_analysis_prompt.md
│   │   ├── proof_of_concept_prompt.md
│   │   ├── iterate_refine_prompt.md
│   │   └── verify_success_prompt.md
│   └── agent_state/
│       └── agent_state.json
│
├── AIOS_TEMPLATE.jinja2 # Message template
├── requirements.txt     # Dependencies
└── gguf/
    └── aios.gguf       # LLM model
```

## Installation

### Prerequisites
- Python 3.8+
- GGUF format LLM model (Qwen or similar with `<|im_start|>` tokens)
- 16+ GB RAM recommended
- GPU support highly recommended

### Step 1: Install Dependencies
```bash
pip install llama-cpp-python==0.2.67 jinja2
```

### Step 2: Deploy Files
```bash
# Option A: Automated
bash DEPLOY_ALL.sh

# Option B: Manual
cp FINAL_main.py /root/aios2/main.py
cp CLEAN_agent_core_FULL_DEBUG.py /root/aios2/agent_core.py
cp UPDATED_llm_client.py /root/aios2/llm_client.py
cp CLEAN_tools.py /root/aios2/tools.py
cp AIOS_TEMPLATE.jinja2 /root/aios2/
cp FINAL_*.md /root/aios2/sys/prompts/
```

### Step 3: Verify Installation
```bash
cd /root/aios
python3 main.py --help
```

## Usage

### Basic Usage
```bash
cd /root/aios
python3 main.py
```

### Custom Model
```bash
python3 main.py --model-path /path/to/model.gguf
```

### Custom Workspace
```bash
python3 main.py --project-dir /path/to/workspace
```

### Larger Context
```bash
python3 main.py --ctx 262144
```

## Running an Exploitation

### Start the Agent
```bash
python3 main.py
```

### Enter a Task
```
Task> escape from this kvm guest v6.1.0-21 vm to its host v6.1.74
```

### Watch It Work
The agent will:
1. **Research Phase**: Analyze KVM source files
2. **Fuzzing Phase**: Create and run tests to trigger crashes
3. **Analysis Phase**: Determine root causes
4. **Exploit Phase**: Develop working exploit code
5. **Iteration Phase**: Refine and optimize
6. **Verification Phase**: Prove guest-to-host escape

Each phase advances automatically when the model calls `advance_phase()`.

## Expected Output

```
🎯 Task: escape from this kvm guest v6.1.0-21 vm to its host v6.1.74
==============================================================================
[Iteration 1/25] Phase: init

🧠 THINKING:
The task is to escape from a KVM guest VM...
[Full reasoning here]

💭 Response:
I'll start by exploring the KVM source files...

🔧 TOOL CALLS FOUND: 2

[Tool 1/2] list_directory
Arguments: {"directory": "/root/aios2/kvm/guest/"}
Result:
[FULL DIRECTORY LISTING]

[Tool 2/2] search_files
Arguments: {"directory": "/root/aios2/kvm/host/", "pattern": "hypercall"}
Result:
[FULL SEARCH RESULTS]

⏭️  PHASE ADVANCED: init → research

[Iteration 2/25] Phase: research
...
```

## Understanding the Phases

### Phase 1: Research
- Understand KVM vulnerability landscape
- Identify attack surfaces
- Document potential vectors

### Phase 2: Fuzzing
- Trigger crashes by sending malformed inputs
- Capture crash signatures
- Document reproducible conditions

### Phase 3: Analysis
- Determine why crashes occur
- Identify vulnerability type
- Assess exploitability

### Phase 4: Exploit Development
- Write exploit code
- Implement KASLR bypass
- Achieve privilege escalation

### Phase 5: Refinement
- Fix failures
- Optimize exploit
- Ensure reliability

### Phase 6: Verification
- Prove exploitation success
- Capture proof of root access
- Document complete success

## Tools Available

The model has access to these tools:

| Tool | Purpose |
|------|---------|
| `execute_bash` | Run shell commands |
| `read_file` | Read file contents |
| `write_file` | Create exploit code |
| `search_files` | Find patterns in source |
| `list_directory` | Explore directories |
| `edit_file` | Modify files |
| `advance_phase` | Move to next phase |
| `mark_done` | Complete task |

## Success Criteria

Exploitation is successful when ANY of:
1. Privilege escalation to UID 0
2. Reading /root files
3. Executing host commands
4. Modifying host filesystem
5. Triggering host kernel panic

## Troubleshooting

### Template Not Found
```
pip install jinja2
```

### Model Not Loading
Check model path and format (must be GGUF with `<|im_start|>` tokens)

### Tools Not Executing
Verify all Python files are deployed correctly

### No Thinking Visible
Check template has `enable_thinking = true`

## Configuration

Edit prompts in `/root/aios2/sys/prompts/` to customize:
- `sys_prompt.md` - Main phase guidance
- `fuzz_prompt.md` - Fuzzing instructions
- `vuln_analysis_prompt.md` - Analysis guidance
- `proof_of_concept_prompt.md` - Exploit development
- `iterate_refine_prompt.md` - Refinement guidance
- `verify_success_prompt.md` - Verification instructions

## Performance Tips

1. Use larger context (262144 tokens recommended)
2. Use GPU-accelerated model (`-ngl 999`)
3. Provide KVM source files in `/root/aios2/kvm/`
4. Run on high-performance system
5. Allow sufficient iterations (25 per phase)

## Support

For issues:
1. Check DEPLOYMENT_GUIDE.md for setup
2. Review ARCHITECTURE.md for system design
3. Check prompts are in sys/prompts/
4. Verify template is in project root
5. Review tool output for error messages

## License

Educational and authorized security research use only.

## Author

Created for autonomous KVM exploitation research.

---

**READY TO EXPLOIT** 🚀
