# Panel Data Economic Empowerment Questionnaire Template

## 3-Year Longitudinal Survey Design (2023-2025)

### Design Philosophy

- **Pre-post intervention design**: Measure outcomes before and after treatment
- **Same respondents, multiple waves**: Track changes within individuals
- **Balanced panel preferred**: Same households in all 3 years
- **Stata-ready format**: All questions designed for direct coding

---

## Cover Page Template

```
【研究标题】
小额信贷对巴基斯坦农村小规模稻农经济赋权的影响研究

【研究目的】
了解2023-2025年小额信贷如何帮助提升种稻收入、增强决策能力和应对风险的能力

【保密声明】
您的回答仅用于学术研究，所有信息严格匿名保密，不会泄露给任何第三方

【填写说明】
填写问卷约需30分钟。请根据家里2023-2025年的实际情况，在对应年份的横线上填数字或打"√"即可

【机构】
四川农业大学经济学院研究团队
```

---

## Section 1: Demographics & Controls (Time-Invariant)

| Q# | Item | 2023 | 2024 | 2025 | Stata Var |
|----|------|------|------|------|-----------|
| 1-1 | 性别 | □男□女 | - | - | gender |
| 1-2 | 年龄（周岁） | ___ | ___ | ___ | age |
| 1-3 | 受教育程度 | □未上学□小学□初中□高中及以上 | - | - | education |
| 1-4 | 家庭总人口 | ___ | ___ | ___ | hhsize |
| 1-5 | 水稻种植劳动力 | □1人□2人□3人□4人+ | - | - | labor |
| 1-6 | 水稻种植面积 | □12.5亩以下□12.5-25亩□25亩以上 | ___ | ___ | land_size |
| 1-7 | 是否加入合作社 | □是□否 | □是□否 | □是□否 | coop |
| 1-8 | 水稻品种 | □本地□杂交□其他 | ___ | ___ | rice_var |

---

## Section 2: Core Dependent Variable — Economic Empowerment

### 2.1 Income & Revenue

| Q# | Item | 2023 | 2024 | 2025 | Stata Var |
|----|------|------|------|------|-----------|
| 2-1 | 种子费用（卢比） | ___ | ___ | ___ | cost_seed |
| 2-2 | 化肥农药费用 | ___ | ___ | ___ | cost_fert |
| 2-3 | 灌溉费用 | ___ | ___ | ___ | cost_irrig |
| 2-4 | 雇工费用 | ___ | ___ | ___ | cost_labor |
| 2-5 | 农具费用 | ___ | ___ | ___ | cost_tools |
| 2-6 | 土地租赁费 | ___ | ___ | ___ | cost_land |
| 2-7 | 其他费用 | ___ | ___ | ___ | cost_other |
| 2-8 | **总成本** | *** | *** | *** | cost_total |
| 2-9 | 小额信贷支付额 | ___ | ___ | ___ | cost_mf |
| 2-10 | 水稻总产量（公斤） | ___ | ___ | ___ | output |
| 2-11 | 销售单价（卢比/公斤） | ___ | ___ | ___ | price |
| 2-12 | 销售收入 | ___ | ___ | ___ | revenue |
| 2-13 | 其他收益 | ___ | ___ | ___ | revenue_other |
| 2-14 | **总收益** | *** | *** | *** | revenue_total |
| 2-15 | **净收入** | *** | *** | *** | net_income |

### 2.2 Subjective Income Assessment

| Q# | Item | Scale |
|----|------|-------|
| 2-16 | 与上一年相比净收入变化 | 1=显著增加 2=略有增加 3=基本不变 4=略有减少 5=显著减少 |
| 2-17 | 与同村其他稻农相比收入水平 | 1=非常高 2=比较高 3=中等 4=比较低 5=非常低 |

---

## Section 3: Core Independent Variable — Microfinance Access

| Q# | Item | 2023 | 2024 | 2025 | Stata Var |
|----|------|------|------|------|-----------|
| 3-1 | 是否使用小额信贷 | □是□否 | □是□否 | □是□否 | mf_use |
| 3-2 | 信贷机构名称 | □Kashf□NRSP□其他 | ___ | ___ | mf_inst |
| 3-3 | 贷款金额（卢比） | □<5万□5-10万□10-20万□>20万 | ___ | ___ | mf_amount |
| 3-4 | 还款期限 | □<6月□6-12月□1-2年□>2年 | - | - | mf_term |
| 3-5 | 实际年利率 | □<10%□10-18%□18-25%□>25% | - | - | mf_rate |
| 3-6 | 用于水稻生产比例 | □≥80%□60-80%□40-60%□<40% | ___ | ___ | mf_prod_share |
| 3-7 | 还款状态 | □提前□按时□逾期后还□逾期未还 | ___ | ___ | mf_repay |
| 3-8 | 未来继续申请意愿 | □是□否 | □是□否 | □是□否 | mf_future |

---

## Section 4: Mediators — Pathways

### 4.1 Technology Adoption

| Q# | Item | 2023 | 2024 | 2025 | Stata Var |
|----|------|------|------|------|-----------|
| 4-1 | 是否购买改良农具 | □是□否 | □是□否 | □是□否 | tech_tool |
| 4-2 | 是否购买良种 | □是□否 | □是□否 | □是□否 | tech_seed |
| 4-3 | 是否参加技术培训 | □是□否 | □是□否 | □是□否 | tech_train |
| 4-4 | 采用科学种植技术（项数） | ___ | ___ | ___ | tech_count |
| 4-5 | 技术水平自我评估 | 1=显著提升 2=略有提升 3=不变 4=下降 | - | - | tech_self |

### 4.2 Risk Coping Capacity

| Q# | Item | 2023 | 2024 | 2025 | Stata Var |
|----|------|------|------|------|-----------|
| 4-6 | 是否建设抗灾设施 | □是□否 | □是□否 | □是□否 | risk_facility |
| 4-7 | 是否遭遇灾害 | □是□否 | □是□否 | □是□否 | risk_disaster |
| 4-8 | 小额信贷帮助恢复 | □是□否 | □是□否 | □是□否 | risk_mf_help |
| 4-9 | 突发需求应对能力 | 1=完全可以 2=基本可以 3=较难 4=完全不能 | - | - | risk_coping |
| 4-10 | 农业保险作用 | 1=显著减少 2=略有减少 3=没减少 4=未购买 | - | - | risk_insurance |

### 4.3 Social Capital

| Q# | Item | 2023 | 2024 | 2025 | Stata Var |
|----|------|------|------|------|-----------|
| 4-11 | 是否加入互助小组 | □是□否 | □是□否 | □是□否 | social_group |
| 4-12 | 每月求助次数 | ___ | ___ | ___ | social_help |
| 4-13 | 获得其他农户信任 | □是□否 | □是□否 | □是□否 | social_trust |
| 4-14 | 社交网络规模变化 | 1=显著扩大 2=略有扩大 3=不变 4=缩小 | - | - | social_network |

---

## Section 5: Moderators — Context

### 5.1 Government Policy

| Q# | Item | 2023 | 2024 | 2025 | Stata Var |
|----|------|------|------|------|-----------|
| 5-1 | 是否获得农业补贴 | □是□否 | □是□否 | □是□否 | policy_subsidy |
| 5-2 | 补贴金额（卢比） | ___ | ___ | ___ | policy_amount |
| 5-3 | 是否参加农业培训 | □是□否 | □是□否 | □是□否 | policy_train |

### 5.2 Regional Infrastructure

| Q# | Item | 2023 | 2024 | 2025 | Stata Var |
|----|------|------|------|------|-----------|
| 5-4 | 主要灌溉方式 | □运河□井水□雨水□其他 | - | - | irrig_type |
| 5-5 | 到最近市场距离（公里） | ___ | ___ | ___ | market_dist |

---

## Stata Panel Data Analysis Code

```stata
* Wide to Long Conversion
reshape long cost_ revenue_ net_income_ mf_, i(household_id) j(year)

* Describe the panel
xtset household_id year
xtdescribe

* Summary statistics
xtsum net_income mf_use cost_total

* Fixed Effects Regression (within estimator)
xtreg net_income mf_use tech_* risk_* social_*, fe robust

* Random Effects for time-invariant controls
xtreg net_income mf_use age education land_size, re robust

* Between-before within comparison
gen mf_post = (year >= 2024) & mf_use == 1
xtreg net_income c.mf_post##c.tech_count, fe robust

* Mediation Analysis
* Step 1: Total effect
xtreg net_income mf_use, fe robust

* Step 2: Mediator models
xtreg tech_count mf_use, fe robust
xtreg risk_coping mf_use, fe robust

* Step 3: Joint model
xtreg net_income mf_use tech_count risk_coping social_network, fe robust

* Moderation Analysis
gen mf_x_policy = mf_use * policy_subsidy
xtreg net_income c.mf_use##c.policy_subsidy, fe robust
```

## Reliability & Validity Checklist

| Check | Standard |
|-------|----------|
| Cronbach's α (multi-item scales) | ≥ 0.70 |
| Test-retest correlation | ≥ 0.80 |
| Expert content validity | ≥ 3 reviewers, CVR ≥ 0.62 |
| Pilot reliability (n=30) | No floor/ceiling effects |
| Missing data | < 5% per variable |
| Panel attrition | < 10% across waves |

## Panel Questionnaire Design Principles

1. **Time-invariant items** (gender, education): Asked once, carried forward
2. **Time-varying items**: Asked each wave
3. **Same metric across waves**: Consistency in scales and units
4. **Recall period**: Reference specific year (2023/2024/2025)
5. **Unique ID**: household_id + year for merge
6. **Stata var naming**: `section_item_year` (e.g., `cost_seed_2023`)
