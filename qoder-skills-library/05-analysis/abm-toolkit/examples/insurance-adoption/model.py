# -*- coding: utf-8 -*-
"""
农业保险参保决策 ABM 模型 (Mesa 3.x)

主体类型:
    - FarmerAgent: 农户（前景理论+社会学习决策）
    - InsuranceCompany: 保险公司（定价+理赔）
    - Government: 政府（补贴调整）

核心机制:
    1. 农户基于Logit模型+邻里效应决定是否投保
    2. 气候冲击（泊松过程）导致损失，保险提供赔付
    3. 政府根据参保率动态调整补贴率
"""

import numpy as np
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


# ============================================================
# 农户主体
# ============================================================
class FarmerAgent(Agent):
    """农户主体：基于前景理论+社会学习的投保决策"""

    def __init__(self, model, altitude, land_size, risk_aversion):
        super().__init__(model)
        self.altitude = altitude  # 海拔（米）
        self.land_size = land_size  # 土地规模（亩）
        self.risk_aversion = risk_aversion  # CRRA风险厌恶系数

        # 财务状态
        self.cash = float(np.random.lognormal(11.0, 0.5))  # 初始资产
        self.insurance = False  # 是否投保
        self.defaulted = False  # 是否破产

        # 风险感知
        self.frost_risk = self._calc_frost_risk()
        self.loss_experience = 0.0

    def _calc_frost_risk(self):
        """基于海拔计算霜冻风险概率"""
        if self.altitude > 1000:
            return 0.15
        elif self.altitude > 600:
            return 0.08
        else:
            return 0.05

    def _get_neighbor_insurance_rate(self):
        """获取邻居投保率（社会学习信号）"""
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False, radius=2)
        if not neighbors:
            return 0.5
        insured = sum(1 for n in neighbors if hasattr(
            n, "insurance") and n.insurance)
        return insured / len(neighbors)

    def _decide_insurance(self):
        """投保决策：Logit模型 + 邻里效应 + 前景理论概率权重"""
        if self.defaulted:
            return

        # 补贴后的实际保费
        premium = self.model.premium_rate * (1 - self.model.policy_subsidy)

        # 不投保的期望效用（前景理论：高估小概率损失）
        # π(p) = p^γ / (p^γ + (1-p)^γ)^{1/γ}, γ≈0.65 (Tversky & Kahneman, 1992)
        p_loss = self.frost_risk
        gamma = 0.65
        weighted_p = p_loss ** gamma / \
            (p_loss ** gamma + (1 - p_loss) ** gamma) ** (1 / gamma)

        EU_no_insurance = self.cash * (1 - weighted_p * 0.4)
        EU_insurance = self.cash * (1 - premium)

        # 邻里效应
        neighbor_rate = self._get_neighbor_insurance_rate()
        peer_pressure = 0.3 * (neighbor_rate - 0.5)

        # Logit投保概率
        beta0 = -1.5   # 基准倾向
        beta1 = 3.2     # 补贴敏感度
        beta2 = 1.8     # 邻里效应

        subsidy_factor = beta1 * self.model.policy_subsidy
        neighbor_factor = beta2 * peer_pressure
        utility_diff = EU_insurance - EU_no_insurance

        prob_insure = 1.0 / \
            (1.0 + np.exp(-(beta0 + subsidy_factor + neighbor_factor + utility_diff * 0.01)))
        self.insurance = np.random.random() < prob_insure

    def _face_climate_shock(self):
        """遭受气候冲击"""
        if self.defaulted:
            return

        if np.random.random() < self.frost_risk:
            loss_ratio = np.random.uniform(0.1, 0.5)
            loss = self.cash * loss_ratio
            self.cash -= loss
            self.loss_experience = loss_ratio

            if self.insurance:
                indemnity = self.model.insurer.claim(loss)
                self.cash += indemnity

    def _produce_and_sell(self):
        """生产与销售"""
        if self.defaulted:
            return

        base_revenue = self.land_size * 1000
        noise = np.random.normal(1.0, 0.1)
        self.cash += base_revenue * noise

        if self.cash < 0:
            self.defaulted = True

    def step(self):
        """单步执行"""
        if self.defaulted:
            return
        self._decide_insurance()
        self._face_climate_shock()
        self._produce_and_sell()


# ============================================================
# 保险公司主体
# ============================================================
class InsuranceCompany(Agent):
    """保险公司：定价、理赔、偿付能力管理"""

    def __init__(self, model):
        super().__init__(model)
        self.capital = 5_000_000
        self.premium_income = 0
        self.claims_paid = 0

    def claim(self, loss_amount):
        """理赔：80%赔付率"""
        if loss_amount > 0 and self.capital > 0:
            payout = min(loss_amount * 0.8, self.capital)
            self.claims_paid += payout
            self.capital -= payout
            return payout
        return 0.0

    def step(self):
        """收取保费"""
        self.premium_income = sum(
            self.model.premium_rate *
            (1 - self.model.policy_subsidy) * f.land_size * 200
            for f in self.model.agents
            if isinstance(f, FarmerAgent) and f.insurance and not f.defaulted
        )
        self.capital += self.premium_income


# ============================================================
# 政府主体
# ============================================================
class Government(Agent):
    """政府：根据参保率动态调整补贴"""

    def __init__(self, model):
        super().__init__(model)
        self.budget = 10_000_000
        self.subsidy_spent = 0

    def step(self):
        """政策调整"""
        farmers = [a for a in self.model.agents if isinstance(a, FarmerAgent)]
        active_farmers = [f for f in farmers if not f.defaulted]

        if not active_farmers:
            return

        insurance_rate = sum(
            1 for f in active_farmers if f.insurance) / len(active_farmers)

        if insurance_rate < 0.4:
            self.model.policy_subsidy = min(
                self.model.policy_subsidy + 0.02, 0.5)
        elif insurance_rate > 0.8:
            self.model.policy_subsidy = max(
                self.model.policy_subsidy - 0.02, 0.1)

        self.subsidy_spent = sum(
            self.model.premium_rate * self.model.policy_subsidy * f.land_size * 200
            for f in active_farmers if f.insurance
        )
        self.budget -= self.subsidy_spent


# ============================================================
# 主模型
# ============================================================
class AgriculturalInsuranceModel(Model):
    """农业保险参保决策ABM主模型 (Mesa 3.x)"""

    def __init__(self, num_farmers=200, grid_width=20, grid_height=20,
                 subsidy_rate=0.25, premium_rate=0.06, seed=None):
        super().__init__(seed=seed)

        self.num_farmers = num_farmers
        self.policy_subsidy = subsidy_rate
        self.premium_rate = premium_rate

        # 空间结构
        self.grid = MultiGrid(grid_width, grid_height, torus=False)

        # 创建农户（Mesa 3.x中Agent自动注册到model.agents）
        for i in range(self.num_farmers):
            altitude = int(np.random.randint(200, 1500))
            land_size = float(np.random.exponential(5)) + 1
            risk_aversion = float(np.random.uniform(0.5, 2.0))

            farmer = FarmerAgent(self, altitude=altitude,
                                 land_size=land_size, risk_aversion=risk_aversion)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(farmer, (x, y))

        # 保险公司
        self.insurer = InsuranceCompany(self)

        # 政府
        self.government = Government(self)

        # 数据收集器
        self.datacollector = DataCollector(
            model_reporters={
                "insure_rate": self._calc_insurance_rate,
                "default_rate": self._calc_default_rate,
                "total_welfare": self._calc_welfare,
                "insurer_capital": lambda m: m.insurer.capital,
                "subsidy_rate": lambda m: m.policy_subsidy,
            }
        )
        self.datacollector.collect(self)

    def _calc_insurance_rate(self):
        farmers = [a for a in self.agents if isinstance(
            a, FarmerAgent) and not a.defaulted]
        if not farmers:
            return 0.0
        return sum(1 for f in farmers if f.insurance) / len(farmers)

    def _calc_default_rate(self):
        farmers = [a for a in self.agents if isinstance(a, FarmerAgent)]
        if not farmers:
            return 0.0
        return sum(1 for f in farmers if f.defaulted) / len(farmers)

    def _calc_welfare(self):
        return sum(a.cash for a in self.agents if isinstance(a, FarmerAgent))

    def step(self):
        """推进一个时间步：随机顺序激活所有Agent"""
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
