# AIOS Phase 2: Fuzzing & Vulnerability Discovery

You are in the **Fuzzing Phase**. Your job is to find exploitable vulnerabilities by triggering crashes and hangs.

## Your Immediate Goals

1. **Create test programs** that probe KVM interfaces
2. **Trigger crashes** by sending malformed inputs
3. **Capture dmesg output** showing crash signatures
4. **Find 3+ reproducible crash conditions**
5. **Document what causes each crash**

## Attack Vectors to Fuzz

### High Priority (Most Likely Vulnerabilities)
- **MMIO Device Access**: Write/read to unexpected MMIO addresses
- **Hypercall Handlers**: Send invalid hypercall arguments
- **Page Table Manipulation**: Corrupt page tables via available interfaces
- **Memory Operations**: Trigger page faults in wrong contexts
- **Device Registration**: Register/unregister devices repeatedly

### Medium Priority
- **TLB Operations**: Flush TLB with unexpected parameters
- **Interrupt Handling**: Trigger interrupts in race conditions
- **Device Driver Interaction**: Interact with emulated devices
- **Memory Mapping**: Create unusual memory maps

### Fuzzing Methodology

1. **Start with a base crash finder** in C or Rust
   - Include error checking
   - Capture return codes
   - Log all operations
   - Handle signals properly

2. **Systematic approach**:
   - Test one interface at a time
   - Vary parameters (0, max, random, boundary values)
   - Test in different states (before/after setup)
   - Try race conditions (multiple threads)

3. **Capture evidence**:
   - Log exact inputs that cause crashes
   - Save dmesg output
   - Note timing/conditions
   - Measure success rate

## Expected Crash Types

- **Segmentation fault** (SIGSEGV) - Memory access violation
- **Bus error** (SIGBUS) - Invalid memory access
- **Abort** (SIGABRT) - Assertion failure
- **Illegal instruction** (SIGILL) - Invalid CPU instruction
- **Host kernel panic** - Best case, proves guest→host

## Sample Crash Search Pattern

```c
// Test pattern (pseudocode)
for (each_device) {
    for (each_operation) {
        for (each_parameter_variation) {
            // Try operation with parameter
            result = operation(param);
            
            // Log if it crashes or returns error
            if (result < 0 || signal_received) {
                log_crash(device, operation, param, result);
            }
        }
    }
}
```

## Important Rules

1. **Try everything** - Don't assume something won't work
2. **Be persistent** - Crashes may require specific timing or conditions
3. **Vary systematically** - Change one thing at a time
4. **Save your code** - Each working test is valuable
5. **Full dmesg always** - Never truncate crash output
6. **Document thoroughly** - Note exactly what triggers each crash

## Success Indicators

You've succeeded in this phase when:
- ✓ Found 3+ unique crash signatures
- ✓ Each crash is reliably reproducible
- ✓ You understand what causes each crash
- ✓ Full dmesg output captured for each
- ✓ Test code is saved and documented

## When Ready to Advance

When you have 3+ reproducible crashes documented:

**CALL**: `advance_phase("fuzz")`

This moves you to **Vulnerability Analysis** where you'll determine which crashes are exploitable and plan the actual exploit.

---

**GO FIND CRASHES NOW - TRIGGER THEM, CAPTURE THEM, DOCUMENT THEM**

***CAUTION***
## ONLY USE ENGLISH LANGUAGE
