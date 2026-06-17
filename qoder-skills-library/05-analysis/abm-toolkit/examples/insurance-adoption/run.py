# -*- coding: utf-8 -*-
"""
农业保险参保决策 ABM — 可运行示例

基于前景理论 + 社会学习的农户投保决策仿真。
依赖: pip install mesa numpy networkx matplotlib pandas

运行:
    python run.py

输出:
    - 控制台打印参保率/违约率/社会福利的时间序列摘要
    - results/ 目录下生成 CSV 和 PNG 图表
"""

from model import AgriculturalInsuranceModel
import matplotlib.pyplot as plt
import sys
import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # 无头模式，避免弹窗


def run_single(seed=42, steps=50, subsidy_rate=0.25):
    """单次运行仿真"""
    np.random.seed(seed)
    model = AgriculturalInsuranceModel(
        num_farmers=200,
        grid_width=20,
        grid_height=20,
        subsidy_rate=subsidy_rate,
        seed=seed,
    )
    for _ in range(steps):
        model.step()

    df = model.datacollector.get_model_vars_dataframe()
    return df


def run_scenarios(steps=50):
    """情景对比：不同补贴率下的参保率"""
    scenarios = {
        "无补贴 (0%)": 0.00,
        "低补贴 (15%)": 0.15,
        "中补贴 (25%)": 0.25,
        "高补贴 (35%)": 0.35,
    }

    all_results = {}
    for name, subsidy in scenarios.items():
        # 每个情景跑5次取均值
        runs = []
        for seed in range(5):
            df = run_single(seed=seed, steps=steps, subsidy_rate=subsidy)
            runs.append(df["insure_rate"].iloc[-1])
        all_results[name] = {
            "final_insure_rate_mean": np.mean(runs),
            "final_insure_rate_std": np.std(runs),
        }

    return pd.DataFrame(all_results).T


def plot_results(df, save_path="results/"):
    """绘制并保存图表"""
    os.makedirs(save_path, exist_ok=True)

    fig, axes = plt.subplots(2, 1, figsize=(10, 8))

    # Insurance rate
    axes[0].plot(df.index, df["insure_rate"], color="blue", linewidth=2)
    axes[0].set_ylabel("Insurance Rate", fontsize=12)
    axes[0].set_title("Insurance Adoption Dynamics", fontsize=14)
    axes[0].set_ylim(-0.05, 1.05)
    axes[0].grid(True, alpha=0.3)

    # Social welfare
    axes[1].plot(df.index, df["total_welfare"], color="green", linewidth=2)
    axes[1].set_ylabel("Total Welfare (Assets)", fontsize=12)
    axes[1].set_xlabel("Time Step (Year)", fontsize=12)
    axes[1].set_title("Social Welfare Dynamics", fontsize=14)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig(os.path.join(save_path, "insurance_adoption.png"), dpi=150)
    print(f"图表已保存: {save_path}insurance_adoption.png")


def main():
    print("=" * 60)
    print("农业保险参保决策 ABM 仿真")
    print("=" * 60)

    # --- 单次运行 ---
    print("\n[1/3] 单次运行 (补贴率=25%, 50步)...")
    df = run_single(seed=42, steps=50, subsidy_rate=0.25)
    print(f"  最终参保率: {df['insure_rate'].iloc[-1]:.1%}")
    print(f"  最终违约率: {df['default_rate'].iloc[-1]:.1%}")
    print(f"  社会福利:   {df['total_welfare'].iloc[-1]:.0f}")

    os.makedirs("results", exist_ok=True)
    df.to_csv("results/single_run.csv", index=False)

    # --- 情景对比 ---
    print("\n[2/3] 情景对比 (不同补贴率)...")
    scenario_df = run_scenarios(steps=50)
    print(scenario_df.to_string())
    scenario_df.to_csv("results/scenarios.csv")

    # --- 绘图 ---
    print("\n[3/3] 生成图表...")
    plot_results(df)

    print("\n" + "=" * 60)
    print("仿真完成！结果保存在 results/ 目录。")
    print("=" * 60)


if __name__ == "__main__":
    main()
