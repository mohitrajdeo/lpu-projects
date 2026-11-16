"""
Academic Publication Chart Generator (Member 6 Responsibility)
Generates high-resolution IEEE-compliant figures for the research paper and presentation deck.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set academic publication style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "paper", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def generate_telemetry_chart():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_telemetry.csv")
    if not os.path.exists(csv_path):
        return
    df = pd.read_csv(csv_path).iloc[:450] # Focus on first 450 points including CPU spike
    
    fig, ax1 = plt.subplots(figsize=(8, 3.5), dpi=300)
    
    color = '#1f77b4'
    ax1.set_xlabel('Time Steps (Seconds)', fontsize=10, fontweight='bold')
    ax1.set_ylabel('CPU Usage (%)', color=color, fontsize=10, fontweight='bold')
    ax1.plot(df.index, df['cpu_usage_pct'], color=color, label='CPU Load (%)', linewidth=1.5)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, 110)

    # Highlight anomaly injection region
    anomaly_region = df[df['is_anomaly'] == 1].index
    if len(anomaly_region) > 0:
        ax1.axvspan(anomaly_region[0], anomaly_region[-1], color='#ff7f0e', alpha=0.25, label='Injected Anomaly (CPU Saturation)')

    ax2 = ax1.twinx()
    color = '#d62728'
    ax2.set_ylabel('P99 Latency (ms)', color=color, fontsize=10, fontweight='bold')
    ax2.plot(df.index, df['latency_ms'], color=color, linestyle='--', label='P99 Latency (ms)', linewidth=1.5)
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Fig 2: Telemetry Drift and Dynamic Latency Surge Under Fault Injection', fontsize=11, fontweight='bold', pad=12)
    fig.tight_layout()
    out_path = os.path.join(FIG_DIR, "fig2_telemetry_anomaly_detection.png")
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Saved {out_path}")

def generate_mttd_mttr_chart():
    fig, ax = plt.subplots(figsize=(7, 3.8), dpi=300)
    
    categories = ['MTTD (Mean Time to Detect)', 'MTTR (Mean Time to Recover)']
    traditional = [69.0, 313.7]
    aegisops = [2.8, 6.6]
    
    x = np.arange(len(categories))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, traditional, width, label='Traditional SRE / Manual Alerts', color='#7f7f7f', edgecolor='#333333')
    rects2 = ax.bar(x + width/2, aegisops, width, label='KubeRevive Autonomous Framework', color='#2ca02c', edgecolor='#333333')
    
    ax.set_ylabel('Duration in Seconds (Log Scale)', fontsize=10, fontweight='bold')
    ax.set_yscale('log')
    ax.set_title('Fig 3: Mean Time to Detect (MTTD) & Recover (MTTR) Comparison', fontsize=11, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9, fontweight='bold')
    ax.legend(fontsize=9)
    
    # Value labels
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}s', xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}s\n(-97%)', xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1b781b')
        
    fig.tight_layout()
    out_path = os.path.join(FIG_DIR, "fig3_mttd_mttr_comparison.png")
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Saved {out_path}")

def generate_ablation_chart():
    fig, ax = plt.subplots(figsize=(7, 3.8), dpi=300)
    models = ['Z-Score / EWMA', 'Isolation Forest', 'KubeRevive Hybrid Ensemble']
    precision = [78.4, 89.1, 94.2]
    recall = [81.2, 84.5, 91.8]
    f1 = [79.8, 86.7, 93.0]
    
    x = np.arange(len(models))
    width = 0.25
    
    ax.bar(x - width, precision, width, label='Precision (%)', color='#1f77b4')
    ax.bar(x, recall, width, label='Recall (%)', color='#ff7f0e')
    ax.bar(x + width, f1, width, label='F1-Score (%)', color='#2ca02c')
    
    ax.set_ylabel('Score (%)', fontsize=10, fontweight='bold')
    ax.set_ylim(60, 105)
    ax.set_title('Fig 4: Ablation Study - Anomaly Detection Model Architecture Benchmarking', fontsize=11, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=9, fontweight='bold')
    ax.legend(loc='lower right', fontsize=9)
    
    fig.tight_layout()
    out_path = os.path.join(FIG_DIR, "fig4_ablation_study.png")
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Saved {out_path}")

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(8, 4), dpi=300)
    ax.axis('off')

    boxes = [
        ("Cloud Microservices\n& Telemetry Stream\n(Prometheus / Logs)", 0.08, 0.5, "#dbeafe", "#1e40af"),
        ("Hybrid Anomaly\nDetection Engine\n(Z-Score + iForest)", 0.32, 0.5, "#fef3c7", "#b45309"),
        ("Agentic RCA &\nTriage Engine\n(RAG Postmortems)", 0.56, 0.5, "#e0e7ff", "#4338ca"),
        ("Autonomous Actuators\n& Self-Healing\n(Rollback/Restart/Scale)", 0.80, 0.5, "#dcfce7", "#15803d")
    ]

    for title, x, y, fc, ec in boxes:
        ax.text(x, y, title, ha="center", va="center", fontsize=9, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.8", fc=fc, ec=ec, lw=2))

    # Arrows
    arrow_props = dict(facecolor='#475569', edgecolor='#475569', arrowstyle="->", lw=2)
    ax.annotate("", xy=(0.23, 0.5), xytext=(0.17, 0.5), arrowprops=arrow_props)
    ax.annotate("", xy=(0.47, 0.5), xytext=(0.41, 0.5), arrowprops=arrow_props)
    ax.annotate("", xy=(0.71, 0.5), xytext=(0.65, 0.5), arrowprops=arrow_props)
    
    # Closed loop feedback arrow
    ax.annotate("", xy=(0.08, 0.32), xytext=(0.80, 0.32),
                arrowprops=dict(facecolor='#15803d', edgecolor='#15803d', arrowstyle="->", lw=1.8, linestyle="dashed"))
    ax.text(0.44, 0.28, "Closed-Loop Verification & Stabilization Probe", ha="center", va="center", fontsize=8, color="#15803d", fontweight="bold")

    plt.title('Fig 1: KubeRevive High-Level Multi-Agent Autonomous Architecture', fontsize=11, fontweight='bold')
    fig.tight_layout()
    out_path = os.path.join(FIG_DIR, "fig1_architecture.png")
    plt.savefig(out_path)
    plt.close()
    print(f"[+] Saved {out_path}")

if __name__ == "__main__":
    generate_architecture_diagram()
    generate_telemetry_chart()
    generate_mttd_mttr_chart()
    generate_ablation_chart()

