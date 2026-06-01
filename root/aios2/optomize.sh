#!/usr/bin/env bash

echo "=========================================="
echo "Tuning kernel for exploit testing"
echo "=========================================="

# Disable panic on OOM (system won't reboot)
echo "Setting vm.panic_on_oom=0"
sysctl -w vm.panic_on_oom=0

# Kill the task that triggered OOM, not random system services
echo "Setting vm.oom_kill_allocating_task=1"
sysctl -w vm.oom_kill_allocating_task=1

# Don't dump all tasks (reduces log spam and saves time)
echo "Setting vm.oom_dump_tasks=0"
sysctl -w vm.oom_dump_tasks=0

# Make OOM killer wait less before acting (default is 0)
echo "Setting vm.oom_kill_allocating_task_wait=0"
sysctl -w vm.oom_kill_allocating_task_wait=0 2>/dev/null || true

# Set OOM adjustment for the current shell to be less likely killed
echo "Setting OOM score adjustment for current shell"
echo -500 > /proc/self/oom_score_adj 2>/dev/null || true

# Make the OOM killer more aggressive overall (1-1000, default 50)
echo "Setting vm.oom_killer_aggressiveness=100"
sysctl -w vm.oom_killer_aggressiveness=100 2>/dev/null || true

# Disable kernel panic on other errors (keep system running)
echo "Setting kernel.panic=0"
sysctl -w kernel.panic=0

echo ""
echo "=========================================="
echo "Current OOM settings:"
echo "=========================================="
sysctl vm.panic_on_oom
sysctl vm.oom_kill_allocating_task
sysctl vm.oom_dump_tasks

echo ""
echo "To make these changes permanent, add to /etc/sysctl.conf:"
echo "vm.panic_on_oom=0"
echo "vm.oom_kill_allocating_task=1"
echo "vm.oom_dump_tasks=0"

# Optionally make permanent
read -p "Make these changes permanent? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cat >> /etc/sysctl.conf << EOF

# Exploit testing optimizations
vm.panic_on_oom = 0
vm.oom_kill_allocating_task = 1
vm.oom_dump_tasks = 0
EOF
    echo "Changes saved to /etc/sysctl.conf"
    sysctl -p
fi
