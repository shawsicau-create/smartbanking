# -*- coding: utf-8 -*-
"""
汉源花椒保险模拟实验 — 运行脚本

运行:
    python run.py

输出:
    - 控制台打印各情景参保率/违约率/社会福利摘要
    - results/ 目录下生成 CSV 和 PNG 图表

依赖:
    pip install mesa numpy pandas matplotlib
"""

from model import HanyuanPepperInsuranceModel
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")  # 无头模式


# ============================================================
# 单次运行
# ============================================================
def run_single(seed=42, steps=30, subsidy_rate=0.30,
               subsidy_mode="uniform", climate_multiplier=1.0):
    """单次仿真运行"""
    np.random.seed(seed)
    model = HanyuanPepperInsuranceModel(
        num_farmers=300,
        grid_width=20, grid_height=20,
        subsidy_rate=subsidy_rate,
        subsidy_mode=subsidy_mode,
        climate_shock_multiplier=climate_multiplier,
        seed=seed,
    )
    for _ in range(steps):
        model.step()

    df = model.datacollector.get_model_vars_dataframe()
    return df


# ============================================================
# 情景对比
# ============================================================
def run_scenarios(steps=30, n_runs=5):
    """多情景对比实验"""
    scenarios = {
        "基准(30%补贴)": {
            "subsidy_rate": 0.30, "subsidy_mode": "uniform",
            "climate_multiplier": 1.0},
        "高补贴(50%)": {
            "subsidy_rate": 0.50, "subsidy_mode": "uniform",
            "climate_multiplier": 1.0},
        "阶梯补贴": {
            "subsidy_rate": 0.30, "subsidy_mode": "tiered",
            "climate_multiplier": 1.0},
        "极端气候(霜冻×1.5)": {
            "subsidy_rate": 0.30, "subsidy_mode": "uniform",
            "climate_multiplier": 1.5},
        "无保险(对照)": {
            "subsidy_rate": 0.00, "subsidy_mode": "none",
            "climate_multiplier": 1.0},
    }

    all_results = {}
    for name, params in scenarios.items():
        print(f"  运行情景: {name} ...")
        insure_rates = []
        default_rates = []
        welfares = []
        insurer_solvents = []

        for seed in range(n_runs):
            df = run_single(
                seed=seed, steps=steps,
                subsidy_rate=params["subsidy_rate"],
                subsidy_mode=params["subsidy_mode"],
                climate_multiplier=params["climate_multiplier"],
            )
            insure_rates.append(df["insure_rate"].iloc[-1])
            default_rates.append(df["default_rate"].iloc[-1])
            welfares.append(df["total_welfare"].iloc[-1])
            insurer_solvents.append(df["insurer_capital"].iloc[-1])

        all_results[name] = {
            "参保率(均值)": np.mean(insure_rates),
            "参保率(标准差)": np.std(insure_rates),
            "违约率(均值)": np.mean(default_rates),
            "社会福利(均值)": np.mean(welfares),
            "保险公司资本(均值)": np.mean(insurer_solvents),
        }

    return pd.DataFrame(all_results).T


# ============================================================
# 可视化
# ============================================================
def plot_results(df, save_dir="results/"):
    """绘制仿真结果图表"""
    os.makedirs(save_dir, exist_ok=True)

    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    fig.suptitle("汉源花椒保险ABM仿真结果\n(Hanyuan Pepper Insurance ABM Simulation)",
                 fontsize=14, fontweight="bold")

    # 1. 参保率动态
    ax = axes[0, 0]
    ax.plot(df.index, df["insure_rate"], "b-", linewidth=2, label="总体")
    ax.plot(df.index, df["high_alt_insure_rate"],
            "r--", linewidth=1.5, label="高海拔(>1500m)")
    ax.plot(df.index, df["low_alt_insure_rate"],
            "g--", linewidth=1.5, label="低海拔(≤1500m)")
    ax.set_ylabel("Insurance Rate")
    ax.set_title("参保率动态 (Insurance Adoption)")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 2. 违约率
    ax = axes[0, 1]
    ax.plot(df.index, df["default_rate"], "r-", linewidth=2)
    ax.set_ylabel("Default Rate")
    ax.set_title("农户违约率 (Farmer Default Rate)")
    ax.set_ylim(-0.01, 0.5)
    ax.grid(True, alpha=0.3)

    # 3. 社会福利
    ax = axes[1, 0]
    ax.plot(df.index, df["total_welfare"], "g-", linewidth=2)
    ax.set_ylabel("Total Welfare (元)")
    ax.set_title("农户总福利 (Social Welfare)")
    ax.grid(True, alpha=0.3)

    # 4. 保险公司资本
    ax = axes[1, 1]
    ax.plot(df.index, df["insurer_capital"], "b-", linewidth=2)
    ax.axhline(y=600_000, color="r", linestyle="--", alpha=0.5, label="偿付警戒线")
    ax.set_ylabel("Capital (元)")
    ax.set_title("保险公司资本金 (Insurer Capital)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 5. 花椒价格
    ax = axes[2, 0]
    ax.plot(df.index, df["pepper_price"], "orange", linewidth=2)
    ax.set_ylabel("Price (元/斤)")
    ax.set_xlabel("种植季 (Growing Season)")
    ax.set_title("花椒价格波动 (Pepper Price GBM)")
    ax.grid(True, alpha=0.3)

    # 6. 政府补贴支出
    ax = axes[2, 1]
    ax.plot(df.index, df["gov_subsidy_spent"],
            "purple", linewidth=2, label="年支出")
    ax.plot(df.index, df["gov_budget"], "brown", linewidth=1.5, label="剩余预算")
    ax.set_ylabel("Amount (元)")
    ax.set_xlabel("种植季 (Growing Season)")
    ax.set_title("政府财政 (Government Budget)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(save_dir, "hanyuan_pepper_insurance.png")
    fig.savefig(path, dpi=150)
    print(f"  图表已保存: {path}")
    plt.close(fig)

    # 额外：海拔-参保率散点图
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.set_title("海拔与参保率关系 (Altitude vs Insurance)")
    # 使用最后一年的agent数据（从df中获取不到，用模型快照）
    ax2.set_xlabel("海拔 (m)")
    ax2.set_ylabel("是否参保 (0/1)")
    path2 = os.path.join(save_dir, "altitude_insurance_scatter.png")
    fig2.savefig(path2, dpi=150)
    plt.close(fig2)
    print(f"  图表已保存: {path2}")


def plot_scenario_comparison(scenario_df, save_dir="results/"):
    """绘制情景对比柱状图"""
    os.makedirs(save_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("汉源花椒保险 — 情景对比\n(Scenario Comparison)",
                 fontsize=13, fontweight="bold")

    metrics = ["参保率(均值)", "违约率(均值)", "社会福利(均值)"]
    colors = ["steelblue", "indianred", "seagreen"]

    for i, (metric, color) in enumerate(zip(metrics, colors)):
        ax = axes[i]
        bars = ax.barh(scenario_df.index,
                       scenario_df[metric], color=color, alpha=0.8)
        ax.set_title(metric)
        ax.set_xlabel(metric)
        # 在柱子末端标注数值
        for bar in bars:
            w = bar.get_width()
            ax.text(w, bar.get_y() + bar.get_height() / 2,
                    f" {w:.2%}" if "率" in metric else f" {w:.0f}",
                    va="center", fontsize=8)
        ax.grid(True, axis="x", alpha=0.3)

    plt.tight_layout()
    path = os.path.join(save_dir, "scenario_comparison.png")
    fig.savefig(path, dpi=150)
    print(f"  图表已保存: {path}")
    plt.close(fig)


# ============================================================
# 海拔分层分析
# ============================================================
def altitude_analysis(seed=42, steps=30):
    """海拔分层参保率分析"""
    df = run_single(seed=seed, steps=steps, subsidy_rate=0.30)
    print("\n  海拔分层参保率（最终种植季）:")
    print(f"    高海拔参保率: {df['high_alt_insure_rate'].iloc[-1]:.1%}")
    print(f"    低海拔参保率: {df['low_alt_insure_rate'].iloc[-1]:.1%}")
    print(f"    总体参保率:   {df['insure_rate'].iloc[-1]:.1%}")
    return df


# ============================================================
# 主函数
# ============================================================
def main():
    print("=" * 65)
    print("  汉源花椒保险模拟实验 ABM 仿真")
    print("  Hanyuan Pepper Insurance Agent-Based Model Simulation")
    print("=" * 65)

    os.makedirs("results", exist_ok=True)

    # --- [1/4] 单次基准运行 ---
    print("\n[1/4] 单次基准运行 (补贴率=30%, 30个种植季)...")
    df = run_single(seed=42, steps=30, subsidy_rate=0.30)
    print(f"  最终参保率:   {df['insure_rate'].iloc[-1]:.1%}")
    print(f"  最终违约率:   {df['default_rate'].iloc[-1]:.1%}")
    print(f"  社会福利:     {df['total_welfare'].iloc[-1]:,.0f} 元")
    print(f"  保险公司资本: {df['insurer_capital'].iloc[-1]:,.0f} 元")
    print(f"  花椒价格:     {df['pepper_price'].iloc[-1]:.1f} 元/斤")
    df.to_csv("results/baseline_run.csv", index=False)

    # --- [2/4] 海拔分层分析 ---
    print("\n[2/4] 海拔分层参保率分析...")
    altitude_analysis(seed=42, steps=30)

    # --- [3/4] 多情景对比 ---
    print("\n[3/4] 多情景对比实验 (5个情景 × 5次运行)...")
    scenario_df = run_scenarios(steps=30, n_runs=5)
    print("\n情景对比结果:")
    print(scenario_df.to_string(float_format=lambda x: f"{x:.4f}"))
    scenario_df.to_csv("results/scenario_comparison.csv")

    # --- [4/4] 可视化 ---
    print("\n[4/4] 生成可视化图表...")
    plot_results(df)
    plot_scenario_comparison(scenario_df)

    print("\n" + "=" * 65)
    print("  仿真完成！所有结果保存在 results/ 目录。")
    print("=" * 65)


if __name__ == "__main__":
    main()
