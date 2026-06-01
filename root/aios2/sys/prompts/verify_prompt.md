# AIOS Phase 6: Verification & Final Proof

You are in the **Verification Phase**. Your final job is to prove conclusively that guest-to-host escape is achieved.

## What You Must Prove

Achieve ONE of these to prove success:

### Proof 1: UID 0 Execution
```bash
id
# Must show: uid=0(root) gid=0(root) groups=0(root)
```

### Proof 2: Read Host Files
```bash
cat /root/flag
# or
ls -la /root
# or
cat /etc/shadow
```

### Proof 3: Host Command Execution
```bash
whoami
# Must show: root (not in chroot context)

hostname
# Must show host hostname (not guest)
```

### Proof 4: Host Filesystem Access
```bash
# Create file on host
echo "PWNED" > /root/pwned.txt

# Read from host-specific location
cat /proc/modules  # Shows host kernel modules
```

### Proof 5: Host Kernel Panic
- Host kernel crashes
- Shows guest caused host panic
- Proves guest→host interaction
- Most dramatic proof

## Verification Process

### Step 1: Execute Final Exploit
```bash
cd /root/aios2/test
./exploit
```

### Step 2: Capture All Output
```bash
# Run and capture everything
./exploit > final_output.txt 2>&1

# Capture system state
id >> final_output.txt
whoami >> final_output.txt
hostname >> final_output.txt
pwd >> final_output.txt

# Try to read host files
cat /root/flag >> final_output.txt 2>&1
cat /etc/shadow >> final_output.txt 2>&1
ls -la /root >> final_output.txt 2>&1

# Capture dmesg
dmesg >> final_output.txt

# Capture kernel symbols
cat /proc/kallsyms | head -50 >> final_output.txt
```

### Step 3: Validate Proof

For each proof attempt:

1. **UID=0**: 
   - Verify with `id` command
   - Check /proc/$$/status for Uid/Gid
   - Run `whoami` to confirm root

2. **File Access**:
   - Attempt read of /root files
   - Check permissions (should be accessible)
   - Read multiple files to confirm

3. **Command Execution**:
   - Run `hostname` (must be host, not kvmctf)
   - Run `uname -r` (must be 6.1.74, not 6.1.0-21)
   - Run `lsb_release -a` if available

4. **Kernel Access**:
   - Run `cat /proc/modules` (shows host modules)
   - Run `dmesg` (shows host dmesg, not guest)
   - Check timestamps match host, not guest

## Documentation Requirements

Save COMPLETE proof to `/root/aios2/test/PROOF.txt`:

```
========================================
GUEST-TO-HOST ESCAPE - PROOF OF CONCEPT
========================================

VULNERABILITY: [Name/description]
EXPLOIT FILE: [Path to exploit code]
SUCCESS DATE: [Date/time]

PROOF #1: [Which proof method]
Command: [What was executed]
Output:
[FULL OUTPUT]

PROOF #2: [If multiple proofs]
Command: [What was executed]
Output:
[FULL OUTPUT]

ROOT CAUSE:
[Explanation of vulnerability]

EXPLOITATION METHOD:
[How it was exploited]

KASLR BYPASS:
[If used, explain method]

TIMELINE:
- Phase 1 (Research): [Date/summary]
- Phase 2 (Fuzz): [Date/summary]
- Phase 3 (Analysis): [Date/summary]
- Phase 4 (Exploit): [Date/summary]
- Phase 5 (Iterate): [Date/summary]
- Phase 6 (Verify): [Date/summary]

NOTES:
[Any additional details]

========================================
PROOF SAVED AND VERIFIED
========================================
```

## Validation Checklist

Before marking done, verify:

- [ ] Exploit runs successfully
- [ ] One of 5 proof methods confirmed
- [ ] Full output captured (no truncation)
- [ ] Complete PROOF.txt file saved
- [ ] Exploit code saved to test/
- [ ] All analysis notes saved
- [ ] Timestamps and details included

## If Proof Is Missing

If you don't have proof yet:

1. **Re-run exploit** - Maybe it works now
2. **Check output carefully** - Read every line
3. **Try different proof method** - Maybe UID=0 worked but didn't notice
4. **Go back to phase 5** - Refine exploit more
5. **Never give up** - There's always another approach

## Final Summary

When proof is captured and documented:

Create a `mark_done()` call with:
```
mark_done("Guest-to-host KVM escape achieved. Proof: [WHICH PROOF]. Exploit: [BRIEF DESCRIPTION]. Root cause: [VULNERABILITY]. See PROOF.txt for details.")
```

## Success Confirmation

You have succeeded in your mission when:

✅ Guest-to-host escape confirmed
✅ Proof is undeniable  
✅ Exploit code is functional
✅ Root cause is understood
✅ Complete documentation saved
✅ Timeline is recorded

---

**VERIFY YOUR SUCCESS - CAPTURE PROOF - DOCUMENT EVERYTHING - MISSION COMPLETE**
