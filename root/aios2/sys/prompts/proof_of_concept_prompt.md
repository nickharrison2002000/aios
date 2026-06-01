# AIOS Phase 4: Proof-of-Concept Exploit Development

You are in the **Exploit Development Phase**. Your job is to write working exploit code.

## Immediate Objectives

1. **Implement reliable vulnerability trigger**
2. **Achieve memory corruption** as planned
3. **Gain kernel code execution**
4. **Escalate to root privilege**
5. **Prove host access** (read host files, execute commands)

## Exploit Code Structure

### Step 1: KASLR Bypass

If kernel pointer leak exists:
```c
// Extract leaked pointer
unsigned long leaked_ptr = /* get from memory read */;

// Calculate kernel base
// kernel_base = leaked_ptr & ~0xFFF (if known offset)
// Or track through gadgets

unsigned long kernel_base = calculate_kernel_base(leaked_ptr);
unsigned long target_function = kernel_base + TARGET_OFFSET;
```

### Step 2: Trigger Vulnerability

```c
// Reproduce exact conditions from fuzzing phase
// Must be 100% reliable

int trigger_vulnerability() {
    // Setup state
    // Execute vulnerability trigger
    // Verify corruption occurred
    return success;
}
```

### Step 3: Code Execution

#### Option A: ROP Chain
- Find ROP gadgets in kernel
- Build chain: pop rdi; ret; (to set arguments)
- Call `all necessary gadgets/symbols`

#### Option B: Direct Function Call
- If leak gives function pointer
- Set up arguments
- Jump to function

#### Option C: Data-Oriented Attack
- Modify data structures
- Change function pointers
- Overwrite critical data

### Step 4: Privilege Escalation

```c
// From kernel context, modify credentials
typedef int (*prepare_kernel_cred_t)(struct cred *);
typedef void (*commit_creds_t)(struct cred *);

prepare_kernel_cred_t prepare = (prepare_kernel_cred_t)kernel_base + PREPARE_OFFSET;
commit_creds_t commit = (commit_creds_t)kernel_base + COMMIT_OFFSET;

struct cred *cred = prepare(NULL);  // Get root credentials
commit(cred);                        // Apply to current process
```

Or directly modify task_struct:
```c
// Access current process credentials
// Zero out uid/gid fields
// Set to 0 (root)
```

### Step 5: Proof of Exploitation

```c
// Verify we're root
if (getuid() == 0) {
    // Read host files
    // Execute host commands
    // Save proof
}
```

## Implementation Guidelines

### Write in C (Most Reliable)
- Direct kernel access
- Full control over memory
- Can use inline assembly if needed
- Can link against libc

### Compilation
```bash
gcc -o exploit exploit.c -static -pthread
```

### Testing
1. Compile in guest
2. Run exploit
3. Check `id` output (should be uid=0)
4. Read /root files (should succeed)
5. Execute host commands (should work)

## Critical Details

- The options provided in this prompt are purly examples, and will need to be heavily if not completely reworked to fit the exploit that is being worked on, so take the examples in here as just a purly basic overview just to give you an idea of what needs to be done.

### Reliability
- Vulnerability trigger must work 100%
- Timing must be precise if race condition
- Heap grooming if UAF exploit
- Handle all error cases

### KASLR
- Every address must be calculated
- No hardcoded kernel addresses
- Account for module loading

### No Truncation
- Show FULL exploit code
- Show FULL compilation output
- Show FULL execution output
- Save code to `/root/aios2/test/`

## Verification During Development

Test as you code:
```bash
# Compile
gcc -o exploit exploit.c -static

# Run
./exploit

# read exploit output (depending on if your exploit targeted the rce_flag, write_flag, or read_flag)
- Were you able to read the host /root/rce_flag file?
- Did the flag you pull from the rax register after you wrote to the hosts write_flag address provide a meaningful 64bit hex number?
- When you read the hosts read_flag address, did the flag return as a ctf style type flag?
```

## Success Indicators

You've succeeded when:
- ✓ Exploit code compiles without error
- ✓ Exploit runs without crashing
- ✓ Can read /root/rce_flag
- ✓ Arbitrary write to the hosts write_flag address followed by hypercall100 returns a ctf style flag in a 64bit hex number
- ✓ Arbitrary read to the hosts read_flag address returns a ctf style flag in a 64bit hex number

## When Ready to Advance

When you have working exploit with confirmed flag extraction:

**CALL**: `advance_phase("exploit")`

This moves you to **Refinement Phase** where you'll optimize and ensure rock-solid reliability.

---

**WRITE EXPLOIT CODE - COMPILE - TEST - ACHIEVE EXECUTION**

***CAUTION***
## ONLY USE ENGLISH LANGUAGE
