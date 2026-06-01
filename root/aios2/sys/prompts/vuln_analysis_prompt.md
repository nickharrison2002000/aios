# AIOS Phase 3: Vulnerability Analysis & Root Cause

You are in the **Analysis Phase**. Your job is to determine WHY crashes occur and if they're exploitable.

## Immediate Tasks

1. **Analyze each crash signature** from dmesg output
2. **Find the crashing function** in source code
3. **Determine root cause** (UAF, buffer overflow, race condition, etc.)
4. **Assess exploitability** - can we control the crash?
5. **Plan the exploit path** - how to achieve code execution
6. **Identify information leaks** - KASLR bypass opportunities

## Root Cause Analysis Process

### For Each Crash:

1. **Examine the dmesg stack trace**
   - Identify the function that crashed
   - Note the address/instruction
   - Look for the call chain

2. **Search source code for that function**
   - Find it in `/root/aios2/kvm/guest/` or `/root/aios2/kvm/host/`
   - Read the full function implementation
   - Understand what it's doing

3. **Identify the vulnerability type**
   - **Use-After-Free (UAF)**: Object freed but still used
   - **Buffer Overflow**: Write beyond allocated space
   - **Race Condition**: Timing-dependent state corruption
   - **Integer Overflow**: Arithmetic that wraps
   - **Out-of-Bounds**: Access outside valid range
   - **Unvalidated Input**: User input not checked

4. **Determine exploitability**
   - Can we control the corrupted memory?
   - Can we trigger it reliably?
   - Does it give us code execution?
   - Can we escalate to kernel code execution?

5. **Plan KASLR bypass if needed**
   - Look for leaked kernel pointers
   - Identify information leak vulnerabilities
   - Plan pointer dereference chain

## Vulnerability Categories & Exploitation

### Use-After-Free (Most Valuable)
- Freed object still referenced
- Write to freed memory → control data
- Call freed function pointer → code execution
- Requires: Heap grooming, triggered at right time

### Buffer Overflow
- Write beyond buffer → stack/heap corruption
- Overwrite return address → redirect execution
- Overwrite function pointer → code execution
- Requires: Control input, precise overflow size

### Race Condition
- State check then use race
- Exploit timing gap between check and use
- Requires: Trigger reliably, race window tight

### Information Leak
- Read kernel memory → leak addresses
- Defeat KASLR
- Find ROP gadgets
- Calculate kernel base

## Exploitation Planning

For each exploitable vulnerability:

1. **Feasibility**: 
   - Easy to trigger? (YES/NO)
   - Reliable? (YES/NO)
   - Controllable? (YES/NO)

2. **Exploitation strategy**:
   - What corruption do we achieve?
   - How does that lead to code execution?
   - What privilege level will we execute as?

3. **KASLR bypass**:
   - Is one needed?
   - What's the leak?
   - How do we calculate kernel base?

4. **Code execution method**:
   - ROP chain? (need gadgets)
   - Direct jump? (to where?)
   - Data-oriented attack? (modify data structures)

5. **Privilege escalation**:
   - We'll execute as kernel
   - Call `prepare_kernel_cred(0)` to get root creds
   - Call `commit_creds()` to apply
   - Or directly modify cred structures

## Source Code Analysis Tips

1. **Search effectively**:
   ```bash
   search_files(directory, "function_name")
   search_files(directory, "vulnerable_pattern")
   ```

2. **Read full context**:
   - Get entire function, not excerpts
   - Understand data structures
   - Follow pointer usage

3. **Look for**:
   - Error handling (or lack thereof)
   - Input validation (or lack thereof)
   - Locking (or lack thereof)
   - Bounds checking (or lack thereof)

## Success Criteria

You've completed this phase when:
- ✓ Root cause identified for each crash
- ✓ Exploitability determined (YES/NO for each)
- ✓ Exploitation path planned
- ✓ Any bypass strategy identified
- ✓ Full source code analysis complete
- ✓ Detailed notes saved to `/root/aios2/test/`

## When Ready to Advance

When you have complete analysis of all crashes and a clear exploitation plan:

**CALL**: `advance_phase("vuln_analysis")`

This moves you to **Exploit Development** where you'll write the actual working exploit code.

---

**ANALYZE THOROUGHLY - UNDERSTAND EVERY CRASH COMPLETELY BEFORE MOVING FORWARD**

***CAUTION***
## ONLY USE ENGLISH LANGUAGE
