# -*- coding: utf-8 -*-
"""
汉源花椒保险模拟实验 ABM 模型 (Mesa 3.x)

研究区域: 四川省雅安市汉源县（花椒/贡椒主产区）
主体类型:
    - PepperFarmer: 椒农（前景理论+社会学习+多重气候风险）
    - Insurer: 保险公司（定价+理赔+偿付能力管理）
    - Government: 政府（阶梯式/统一式保费补贴）

核心机制:
    1. 椒农基于Logit模型+邻里效应+损失经历决定是否投保
    2. 三重气候冲击：倒春寒(霜冻)、春旱、收获期暴雨
    3. 花椒产量模型：海拔×树龄×管理水平
    4. 花椒价格波动：几何布朗运动(GBM)
    5. 政府阶梯式补贴：按海拔分层差异化补贴
"""

import numpy as np
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


# ============================================================
# 常量与默认参数
# ============================================================
# 气候风险参数（汉源县特征）
FROST_BASE_PROB = 0.20        # 倒春寒基准概率
DROUGHT_BASE_PROB = 0.12      # 干旱基准概率
RAIN_BASE_PROB = 0.15         # 收获期暴雨概率

# 花椒生产参数
PEPPER_BASE_PRICE = 80.0      # 花椒基准价格（元/斤，贡椒品质）
MAX_YIELD_PER_MU = 150.0      # 丰产期亩产（斤，干椒）
COST_PER_MU = 800.0           # 每亩物化成本（元）

# 保险参数
# 保费基于产值计算：精算公平保费 ≈ 损失概率 × 赔付比例 = 0.25 × 0.75 = 0.1875
# 实际费率设为 0.08（政府补贴后农户自付约 5.6%~4%）
PREMIUM_RATE = 0.08           # 保费率（占期望产值）
INDEMNITY_RATIO = 0.75        # 赔付比例
DEFAULT_SUBSIDY = 0.30        # 基准补贴率30%

# 投保决策Logit参数
BETA0 = -2.0                  # 基准倾向
BETA1 = 3.5                   # 补贴敏感度
BETA2 = 2.0                   # 邻里效应
BETA3 = 0.6                   # 损失经历效应
BETA4 = 0.3                   # 海拔风险感知

# 前景理论参数
LOSS_AVERSION = 2.25          # 损失厌恶系数λ
PROB_WEIGHT_GAMMA = 0.65      # 概率权重参数γ


# ============================================================
# 椒农主体
# ============================================================
class PepperFarmer(Agent):
    """
    汉源花椒种植户主体

    属性:
        altitude: 海拔（米），700-2500m
        tree_age: 花椒树龄（年），1-20年
        land_size: 土地规模（亩）
        risk_aversion: CRRA风险厌恶系数
    """

    def __init__(self, model, altitude, tree_age, land_size, risk_aversion):
        super().__init__(model)
        self.altitude = altitude
        self.tree_age = tree_age
        self.land_size = land_size
        self.risk_aversion = risk_aversion

        # 财务状态
        self.cash = float(np.random.lognormal(10.5, 0.5))
        self.insurance = False
        self.defaulted = False

        # 风险与经历
        self.frost_prob = self._calc_frost_prob()
        self.loss_experience = 0.0
        self.claim_count = 0  # 历史获赔次数
        self.annual_income = 0.0

    def _calc_frost_prob(self):
        """基于海拔计算倒春寒概率（高海拔风险更大）"""
        if self.altitude > 1800:
            return FROST_BASE_PROB * 1.4  # 高山带：28%
        elif self.altitude > 1200:
            return FROST_BASE_PROB * 1.15  # 中山带：23%
        else:
            return FROST_BASE_PROB * 0.7   # 低山带：14%

    def _calc_base_yield(self):
        """
        计算基准亩产（斤/亩）
        海拔1200-1800m最优，树龄5-15年丰产
        """
        # 海拔因子：抛物线，1500m最优
        alt_factor = max(0.3, 1.0 - ((self.altitude - 1500) / 1000) ** 2)

        # 树龄因子：3年挂果，5-15年丰产，15年后衰退
        if self.tree_age < 3:
            age_factor = 0.0  # 未挂果
        elif self.tree_age < 5:
            age_factor = (self.tree_age - 3) / 2 * 0.7 + 0.3
        elif self.tree_age <= 15:
            age_factor = 1.0
        else:
            age_factor = max(0.4, 1.0 - (self.tree_age - 15) * 0.08)

        return MAX_YIELD_PER_MU * alt_factor * age_factor

    def _get_neighbor_insurance_rate(self):
        """获取邻居投保率（社会学习信号）"""
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False, radius=2)
        if not neighbors:
            return 0.0
        insured = sum(1 for n in neighbors
                      if isinstance(n, PepperFarmer) and n.insurance)
        return insured / len(neighbors)

    def _get_neighbor_claim_rate(self):
        """获取邻居获赔率（邻居获赔→投保意愿上升）"""
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False, radius=2)
        if not neighbors:
            return 0.0
        claimed = sum(1 for n in neighbors
                      if isinstance(n, PepperFarmer) and n.claim_count > 0)
        return claimed / len(neighbors)

    def _get_subsidy_rate(self):
        """获取适用于本户的补贴率（阶梯式或统一式）"""
        if self.model.subsidy_mode == "tiered":
            if self.altitude > 1800:
                return 0.50
            elif self.altitude > 1200:
                return 0.35
            else:
                return 0.20
        else:
            return self.model.policy_subsidy

    def _decide_insurance(self):
        """
        投保决策：Logit模型 + 邻里效应 + 前景理论概率权重
        """
        if self.defaulted or self.tree_age < 3 or self.model.no_insurance:
            self.insurance = False
            return

        subsidy = self._get_subsidy_rate()
        premium = PREMIUM_RATE * (1 - subsidy)

        # 前景理论概率权重：高估小概率灾害
        p_loss = min(self.frost_prob + DROUGHT_BASE_PROB * 0.5, 0.8)
        gamma = PROB_WEIGHT_GAMMA
        weighted_p = (p_loss ** gamma /
                      (p_loss ** gamma + (1 - p_loss) ** gamma) ** (1 / gamma))

        # 不投保的期望效用（考虑加权灾害概率）
        EU_no = self.cash * (1 - weighted_p * 0.35)
        # 投保的期望效用（扣除保费）
        EU_in = self.cash * (1 - premium)

        # 邻里效应
        neighbor_rate = self._get_neighbor_insurance_rate()
        neighbor_claim = self._get_neighbor_claim_rate()
        peer_pressure = BETA2 * (neighbor_rate - 0.5)

        # 获赔经历的邻里示范效应
        claim_demo = 0.4 * neighbor_claim

        # Logit投保概率
        utility_diff = EU_in - EU_no
        logit_input = (BETA0 +
                       BETA1 * subsidy +
                       peer_pressure +
                       BETA3 * self.loss_experience +
                       BETA4 * (self.frost_prob - 0.15) +
                       claim_demo +
                       utility_diff * 0.005)

        prob_insure = 1.0 / (1.0 + np.exp(-np.clip(logit_input, -10, 10)))
        self.insurance = np.random.random() < prob_insure

    def _face_climate_shocks(self):
        """遭受三重气候冲击：倒春寒、干旱、暴雨"""
        if self.defaulted:
            return

        total_loss_ratio = 0.0

        # 1. 倒春寒（3-4月花期冻害）
        frost_multiplier = self.model.climate_shock_multiplier
        if np.random.random() < self.frost_prob * frost_multiplier:
            loss = np.random.uniform(0.2, 0.7)
            total_loss_ratio += loss * 0.6  # 花期冻害主要影响挂果

        # 2. 春旱（4-5月）
        if np.random.random() < DROUGHT_BASE_PROB * frost_multiplier:
            loss = np.random.uniform(0.1, 0.4)
            total_loss_ratio += loss * 0.3

        # 3. 收获期暴雨（7-8月，影响晾晒品质）
        if np.random.random() < RAIN_BASE_PROB * frost_multiplier:
            loss = np.random.uniform(0.15, 0.5)
            total_loss_ratio += loss * 0.25

        total_loss_ratio = min(total_loss_ratio, 0.95)  # 最多损失95%

        if total_loss_ratio > 0:
            loss_amount = self.annual_income * total_loss_ratio
            self.cash -= loss_amount
            self.loss_experience = total_loss_ratio

            # 保险理赔
            if self.insurance and self.model.insurer:
                indemnity = self.model.insurer.claim(loss_amount)
                self.cash += indemnity
                if indemnity > 0:
                    self.claim_count += 1

    def _produce_and_sell(self):
        """花椒生产与销售"""
        if self.defaulted or self.tree_age < 3:
            # 未挂果树无收入，但有维护成本
            if self.tree_age < 3:
                self.cash -= self.land_size * COST_PER_MU * 0.5
            if self.cash < 0:
                self.defaulted = True
            return

        base_yield = self._calc_base_yield()
        management = max(0.5, np.random.normal(1.0, 0.1))
        yield_per_mu = base_yield * management

        # 花椒价格波动（GBM）
        revenue = yield_per_mu * self.land_size * self.model.pepper_price
        cost = self.land_size * COST_PER_MU

        # 保险保费支出（基于期望产值）
        if self.insurance:
            subsidy = self._get_subsidy_rate()
            expected_value = self._calc_base_yield() * self.model.pepper_price
            premium_cost = (PREMIUM_RATE * (1 - subsidy) *
                            self.land_size * expected_value)
            self.cash -= premium_cost

        self.annual_income = revenue
        self.cash += revenue - cost

        # 树龄增长
        self.tree_age = min(self.tree_age + 1, 30)

        if self.cash < -self.land_size * COST_PER_MU * 2:
            self.defaulted = True

    def step(self):
        """单步执行（一个种植季）"""
        if self.defaulted:
            return
        self._decide_insurance()
        self._face_climate_shocks()
        self._produce_and_sell()


# ============================================================
# 保险公司主体
# ============================================================
class Insurer(Agent):
    """
    保险公司：花椒保险承保、理赔与偿付能力管理
    """

    def __init__(self, model, initial_capital=3_000_000):
        super().__init__(model)
        self.capital = initial_capital
        self.initial_capital = initial_capital
        self.premium_income = 0.0
        self.claims_paid = 0.0
        self.claim_count = 0
        self.loss_ratio_history = []

    def claim(self, loss_amount):
        """理赔：按赔付比例赔付，不超过资本金"""
        if loss_amount <= 0 or self.capital <= 0:
            return 0.0
        payout = min(loss_amount * INDEMNITY_RATIO, self.capital)
        self.claims_paid += payout
        self.capital -= payout
        self.claim_count += 1
        return payout

    def check_solvency(self):
        """偿付能力检查：资本金是否充足"""
        return self.capital > self.initial_capital * 0.2

    def step(self):
        """收取保费，更新损失率"""
        farmers = [a for a in self.model.agents
                   if isinstance(a, PepperFarmer) and a.insurance and not a.defaulted]

        self.premium_income = sum(
            PREMIUM_RATE * (1 - self.model.policy_subsidy) *
            f.land_size * f._calc_base_yield() * self.model.pepper_price
            for f in farmers
        )
        self.capital += self.premium_income

        # 损失率
        if self.premium_income > 0:
            loss_ratio = self.claims_paid / max(self.premium_income, 1)
            self.loss_ratio_history.append(loss_ratio)


# ============================================================
# 政府主体
# ============================================================
class Government(Agent):
    """
    政府：保费补贴政策制定与财政管理
    """

    def __init__(self, model, budget=5_000_000):
        super().__init__(model)
        self.budget = budget
        self.subsidy_spent = 0.0
        self.catastrophe_fund = 2_000_000  # 大灾风险准备金

    def step(self):
        """政策执行：计算补贴支出"""
        farmers = [a for a in self.model.agents
                   if isinstance(a, PepperFarmer) and not a.defaulted]

        if not farmers:
            return

        # 计算总保费补贴支出
        total_subsidy = 0.0
        for f in farmers:
            if f.insurance:
                sub_rate = f._get_subsidy_rate()
                expected_value = f._calc_base_yield() * self.model.pepper_price
                total_subsidy += PREMIUM_RATE * sub_rate * f.land_size * expected_value

        self.subsidy_spent = total_subsidy
        self.budget -= total_subsidy

        # 大灾兜底：保险公司资本金低于阈值时注入
        if (self.model.insurer and
                not self.model.insurer.check_solvency() and
                self.catastrophe_fund > 0):
            injection = min(1_000_000, self.catastrophe_fund)
            self.model.insurer.capital += injection
            self.catastrophe_fund -= injection


# ============================================================
# 主模型
# ============================================================
class HanyuanPepperInsuranceModel(Model):
    """
    汉源花椒保险模拟实验主模型 (Mesa 3.x)

    参数:
        num_farmers: 椒农数量
        grid_width/height: 空间网格大小
        subsidy_rate: 统一补贴率
        subsidy_mode: 补贴模式 ("uniform" / "tiered" / "none")
        climate_shock_multiplier: 气候冲击乘数（>1为极端气候情景）
        seed: 随机种子
    """

    def __init__(self, num_farmers=300, grid_width=20, grid_height=20,
                 subsidy_rate=DEFAULT_SUBSIDY, subsidy_mode="uniform",
                 climate_shock_multiplier=1.0, seed=None):
        super().__init__(seed=seed)

        self.num_farmers = num_farmers
        self.policy_subsidy = subsidy_rate
        self.subsidy_mode = subsidy_mode
        self.no_insurance = (subsidy_mode == "none")  # 无保险对照组
        self.climate_shock_multiplier = climate_shock_multiplier

        # 花椒价格（GBM过程）
        self.pepper_price = PEPPER_BASE_PRICE

        # 空间结构
        self.grid = MultiGrid(grid_width, grid_height, torus=False)

        # 创建椒农
        for _ in range(num_farmers):
            altitude = float(np.random.uniform(700, 2500))
            tree_age = int(np.random.randint(1, 21))
            land_size = float(np.random.exponential(5)) + 1
            risk_aversion = float(np.random.uniform(0.5, 2.0))

            farmer = PepperFarmer(
                self, altitude=altitude, tree_age=tree_age,
                land_size=land_size, risk_aversion=risk_aversion)

            x = self.random.randrange(grid_width)
            y = self.random.randrange(grid_height)
            self.grid.place_agent(farmer, (x, y))

        # 保险公司
        self.insurer = Insurer(self)

        # 政府
        self.government = Government(self)

        # 数据收集器
        self.datacollector = DataCollector(
            model_reporters={
                "insure_rate": self._calc_insurance_rate,
                "default_rate": self._calc_default_rate,
                "total_welfare": self._calc_welfare,
                "avg_income": self._calc_avg_income,
                "insurer_capital": lambda m: m.insurer.capital,
                "insurer_claims": lambda m: m.insurer.claims_paid,
                "gov_subsidy_spent": lambda m: m.government.subsidy_spent,
                "gov_budget": lambda m: m.government.budget,
                "pepper_price": lambda m: m.pepper_price,
                "claim_count": lambda m: m.insurer.claim_count,
                "high_alt_insure_rate": self._calc_high_alt_insurance_rate,
                "low_alt_insure_rate": self._calc_low_alt_insurance_rate,
            },
            agent_reporters={
                "cash": lambda a: a.cash if isinstance(a, PepperFarmer) else None,
                "insurance": lambda a: a.insurance if isinstance(a, PepperFarmer) else None,
                "altitude": lambda a: a.altitude if isinstance(a, PepperFarmer) else None,
                "tree_age": lambda a: a.tree_age if isinstance(a, PepperFarmer) else None,
            }
        )
        self.datacollector.collect(self)

    def _update_pepper_price(self):
        """花椒价格更新：几何布朗运动"""
        mu = 0.02   # 年漂移率2%
        sigma = 0.15  # 年波动率15%
        dt = 1.0
        dw = np.random.normal(0, np.sqrt(dt))
        self.pepper_price *= np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * dw)
        self.pepper_price = np.clip(self.pepper_price, 30, 200)  # 价格区间约束

    def _calc_insurance_rate(self):
        farmers = [a for a in self.agents
                   if isinstance(a, PepperFarmer) and not a.defaulted and a.tree_age >= 3]
        if not farmers:
            return 0.0
        return sum(1 for f in farmers if f.insurance) / len(farmers)

    def _calc_high_alt_insurance_rate(self):
        """高海拔（>1500m）参保率"""
        farmers = [a for a in self.agents
                   if isinstance(a, PepperFarmer) and not a.defaulted
                   and a.tree_age >= 3 and a.altitude > 1500]
        if not farmers:
            return 0.0
        return sum(1 for f in farmers if f.insurance) / len(farmers)

    def _calc_low_alt_insurance_rate(self):
        """低海拔（<=1500m）参保率"""
        farmers = [a for a in self.agents
                   if isinstance(a, PepperFarmer) and not a.defaulted
                   and a.tree_age >= 3 and a.altitude <= 1500]
        if not farmers:
            return 0.0
        return sum(1 for f in farmers if f.insurance) / len(farmers)

    def _calc_default_rate(self):
        farmers = [
            a for a in self.agents if isinstance(a, PepperFarmer)]
        if not farmers:
            return 0.0
        return sum(1 for f in farmers if f.defaulted) / len(farmers)

    def _calc_welfare(self):
        return sum(a.cash for a in self.agents
                   if isinstance(a, PepperFarmer))

    def _calc_avg_income(self):
        active = [a for a in self.agents
                  if isinstance(a, PepperFarmer) and not a.defaulted]
        if not active:
            return 0.0
        return np.mean([a.annual_income for a in active])

    def step(self):
        """推进一个种植季"""
        self._update_pepper_price()
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

    def run_model(self, steps=30):
        """运行指定步数"""
        for _ in range(steps):
            self.step()
        return self.datacollector.get_model_vars_dataframe()
