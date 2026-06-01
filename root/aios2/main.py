#!/usr/bin/env python3
"""
AIOS - Autonomous KVM Exploitation Agent
Main entry point with full path and context management
"""
import argparse
import os
import sys
from pathlib import Path

def get_project_root():
    """Get project root directory."""
    return Path(__file__).parent.absolute()

def main():
    parser = argparse.ArgumentParser(
        description="AIOS - Autonomous KVM guest-to-host exploitation agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py
  python3 main.py --ctx 262144
  python3 main.py --project-dir /path/to/workspace
        """
    )
    parser.add_argument(
        "--project-dir",
        type=str,
        default=None,
        help="Workspace directory for outputs (default: ./test)"
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default=None,
        help="Path to GGUF model (default: ./gguf/aios.gguf)"
    )
    parser.add_argument(
        "--ctx",
        type=int,
        default=262144,
        help="Context size for model (default: 262144)"
    )
    
    args = parser.parse_args()
    
    # Get project root
    project_root = get_project_root()
    
    # Setup workspace
    if not args.project_dir:
        args.project_dir = os.path.join(project_root, "test")
    os.makedirs(args.project_dir, exist_ok=True)
    
    # Setup model path
    if not args.model_path:
        args.model_path = os.path.join(project_root, "gguf", "aios.gguf")
    
    if not os.path.isfile(args.model_path):
        print(f"❌ ERROR: Model not found: {args.model_path}")
        sys.exit(1)
    
    # Setup directories
    prompts_dir = os.path.join(project_root, "sys", "prompts")
    os.makedirs(prompts_dir, exist_ok=True)
    
    # Verify prompts exist
    required_prompts = [
        "sys_prompt.md",
        "fuzz_prompt.md",
        "vuln_analysis_prompt.md",
        "proof_of_concept_prompt.md",
        "iterate_refine_prompt.md",
        "verify_success_prompt.md"
    ]
    
    missing_prompts = []
    for prompt in required_prompts:
        if not os.path.isfile(os.path.join(prompts_dir, prompt)):
            missing_prompts.append(prompt)
    
    if missing_prompts:
        print(f"⚠️  WARNING: Missing prompts: {', '.join(missing_prompts)}")
    
    # Load LLM
    print(f"📦 Loading model: {args.model_path}")
    try:
        from llm_client import LLMClient
        llm = LLMClient(args.model_path, ctx=args.ctx)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ ERROR: Failed to load model")
        print(f"   {str(e)}")
        sys.exit(1)
    
    # Load agent
    print(f"\n🤖 Initializing agent...")
    try:
        from agent_core import Agent
        agent = Agent(
            project_dir=args.project_dir,
            llm_client=llm,
            prompts_dir=prompts_dir,
            state_file=None
        )
        print("✅ Agent initialized")
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize agent")
        print(f"   {str(e)}")
        sys.exit(1)
    
    # Print status
    print(f"\n{'='*70}")
    print(f"🔓 AIOS - Full Unrestricted Access Enabled")
    print(f"{'='*70}")
    print(f"Workspace:   {args.project_dir}")
    print(f"Model:       {args.model_path}")
    print(f"Context:     {args.ctx} tokens")
    print(f"Prompts:     {prompts_dir}")
    print(f"{'='*70}")
    print(f"\n🚀 AIOS Ready\n")
    print(f"Enter tasks to execute. Type 'exit' to quit.\n")
    
    # Interactive loop
    while True:
        try:
            task = input("Task> ").strip()
            
            if task.lower() == "exit":
                print("Goodbye!")
                break
            
            if not task:
                continue
            
            # Run task
            agent.run(task)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
