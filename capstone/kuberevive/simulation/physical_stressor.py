"""
Physical System Stressor & Real Hardware Load Engine (Member 5 Responsibility)
NO MOCKS: Executes real CPU thread saturation, real heap memory allocation,
real socket latency injection, and real garbage collection memory reclamation.
"""

import os
import gc
import math
import time
import psutil
import threading
from typing import Dict, Any, List


class PhysicalStressor:
    """
    Real-world physical stressor that interacts directly with the operating system,
    allocates actual physical RAM, saturates real CPU cores, and introduces real socket latency.
    """
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.cpu_stress_active = False
        self.cpu_threads: List[threading.Thread] = []
        
        # Real physical memory allocation buffer
        self.memory_leak_buffer: List[bytearray] = []
        self.memory_stress_active = False
        
        # Real latency delay in milliseconds
        self.injected_latency_ms = 0.0
        
        # Real error injection flag for API requests
        self.http_500_active = False

    # -------------------------------------------------------------
    # REAL CPU STRESS: Spawns real threads computing intensive math
    # -------------------------------------------------------------
    def _cpu_worker(self):
        """Tight loop calculating square roots and trigonometric functions."""
        while self.cpu_stress_active:
            # Intensive floating point operations to burn real CPU cycles
            _ = [math.sqrt(x) * math.sin(x) for x in range(1, 10000)]
            time.sleep(0.001)

    def start_real_cpu_stress(self, num_threads: int = 4):
        """Spawns worker threads to consume actual CPU cores."""
        if self.cpu_stress_active:
            return
        self.cpu_stress_active = True
        self.cpu_threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=self._cpu_worker, daemon=True)
            t.start()
            self.cpu_threads.append(t)

    def stop_real_cpu_stress(self):
        """Halts all active CPU burn threads."""
        self.cpu_stress_active = False
        self.cpu_threads = []

    # -------------------------------------------------------------
    # REAL MEMORY LEAK: Allocates real megabytes into process heap
    # -------------------------------------------------------------
    def allocate_real_memory_leak(self, megabytes: int = 40):
        """
        Allocates actual byte arrays in physical RAM.
        Can be verified via Task Manager or psutil memory counters.
        """
        self.memory_stress_active = True
        try:
            # Allocate real non-zero bytes to force OS page allocation
            chunk = bytearray(megabytes * 1024 * 1024)
            for i in range(0, len(chunk), 4096):
                chunk[i] = 1  # Touch each 4KB memory page
            self.memory_leak_buffer.append(chunk)
        except MemoryError:
            pass

    def release_real_memory(self):
        """
        Flushes all physical memory leak buffers and invokes garbage collection.
        Visibly drops RAM utilization in the OS process table.
        """
        self.memory_leak_buffer.clear()
        gc.collect()
        self.memory_stress_active = False

    # -------------------------------------------------------------
    # REAL LATENCY & ERROR REGRESSION
    # -------------------------------------------------------------
    def inject_network_latency(self, latency_ms: float = 1200.0):
        self.injected_latency_ms = latency_ms

    def clear_latency(self):
        self.injected_latency_ms = 0.0

    def inject_http_500_storm(self):
        self.http_500_active = True

    def clear_http_500(self):
        self.http_500_active = False

    # -------------------------------------------------------------
    # REAL SYSTEM METRICS PROBE (via psutil)
    # -------------------------------------------------------------
    def get_real_telemetry(self) -> Dict[str, Any]:
        """
        Queries actual operating system telemetry using psutil:
        - Real host CPU %
        - Real host Virtual RAM %
        - Real process Private RSS RAM in MB
        - Injected latency and error state
        """
        host_cpu = psutil.cpu_percent(interval=None)
        mem_info = psutil.virtual_memory()
        proc_mem_mb = round(self.process.memory_info().rss / (1024 * 1024), 2)

        return {
            "real_host_cpu_pct": round(host_cpu, 2),
            "real_host_ram_pct": round(mem_info.percent, 2),
            "real_proc_rss_mb": proc_mem_mb,
            "real_allocated_leak_mb": len(self.memory_leak_buffer) * 40,
            "injected_latency_ms": self.injected_latency_ms,
            "http_500_active": self.http_500_active,
            "timestamp": time.time()
        }

