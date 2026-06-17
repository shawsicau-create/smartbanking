---
name: questionnaire-design
description: "Design and analyze academic survey questionnaires for economics, finance, and rural development research."
workflow_stage: data
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - survey
  - questionnaire
  - data-collection
  - rural-development
---

# Questionnaire Design Skill

Comprehensive toolkit for designing academic survey questionnaires in economics, finance, and rural development domains.

## Core Workflow

### Step 1: Define Research Framework

Before writing questions, establish:

1. **Dependent Variable(s)** — What outcome are you measuring?
   - Economic empowerment: income, decision-making power, risk coping capacity
   - Financial inclusion: access, usage, quality of services
   - Agricultural productivity: yield, cost, revenue

2. **Independent Variable(s)** — Key treatment/exposure
   - Microfinance, credit access, insurance participation
   - Policy interventions, technology adoption

3. **Control Variables** — Demographic & contextual
   - Age, education, household size, land size, region

4. **Mediators/Moderators** — Pathways & boundary conditions
   - Social capital, technology adoption, risk attitude
   - Government support, market access

### Step 2: Select Question Types

| Type | Use Case | Example |
|------|----------|---------|
| Closed single-choice | Demographic, categorical | Gender, education level |
| Closed multi-choice | Behaviors, services used | "Which of the following apply?" |
| Numeric fill-in | Continuous variables | Income (元), area (亩) |
| 5-point Likert scale | Attitudes, satisfaction | "Very dissatisfied → Very satisfied" |
| 7-point Likert scale | Psychological constructs | Self-efficacy, empowerment |
| Ranking | Preferences | "Rank 1-5 by importance" |
| Yes/No + follow-up | Conditional branching | "Yes → Fill table; No → Skip to QX" |

### Step 3: Structure Questionnaire Sections

Standard academic questionnaire structure:

```
1. Cover & Introduction (purpose, anonymity, consent)
2. Respondent Demographics (individual + household)
3. Core Independent Variable (treatment exposure)
4. Dependent Variables (outcomes)
5. Mediating Variables (pathway mechanisms)
6. Moderating Variables (contextual factors)
7. Open-ended feedback
8. Thank you note
```

### Step 4: Design Panel Data Questions (3-Year Tracking)

For longitudinal studies (e.g., 2023-2025), use **column-per-year** format:

| Q# | Item | 2023 | 2024 | 2025 |
|----|------|------|------|------|
| 2-1 | Seed cost (PKR) | ___ | ___ | ___ |
| 2-2 | Fertilizer cost (PKR) | ___ | ___ | ___ |

**Critical**: Always include year indicator and allow N/A for non-respondents in early waves.

### Step 5: Ensure Measurement Validity

**Construct Validity:**
- Use established scales where available (e.g., financial literacy from Lusardi & Mitchell)
- For new constructs, follow Churchill (1979) paradigm: generate 10+ items per dimension, purify via pilot

**Content Validity:**
- Expert review (3+ academics)
- Pre-test with 20-30 target respondents

**Reliability:**
- Cronbach's α ≥ 0.70 for multi-item scales
- Test-retest for stable constructs

### Step 6: Write Questions — Best Practices

**DO:**
- Use simple, jargon-free language (readability ≤ Grade 8)
- Be specific with time frames ("2023年" vs. "最近")
- Include skip logic clearly
- Group related topics together
- Number questions systematically (1.1, 1.2 or Section-Question)

**DON'T:**
- Use double-barreled questions ("Do you use and prefer microfinance?")
- Use leading questions ("Don't you agree that microfinance helps...?")
- Ask about sensitive topics without proper framing
- Use abstract terms without definition ("economic empowerment" → operationalize)

## Output: Questionnaire Document

Generate a complete `.docx` questionnaire with:

1. **Cover page** — Title, institution, purpose, anonymity statement, estimated time
2. **Instructions for interviewers**
3. **Question sections** with proper formatting
4. **Conditional branching** clearly marked (e.g., "If Yes → Answer Q7; If No → Skip to Q12")
5. **Table templates** for economic data (cost, revenue, assets)
6. **5-point Likert scales** with labeled endpoints
7. **Thank you page**

## Stata-Pready Data Design

Design questions so answers can be directly coded for Stata:

```stata
* Example variable coding
gen gender = 1 if Q1 == "男" | Q1 == "男（1）"
replace gender = 0 if Q1 == "女" | Q1 == "女（2）"

* Likert scale coding (1-5)
recode Q_satisfaction (1=1) (2=2) (3=3) (4=4) (5=5), gen(satisfaction)

* Panel data long format
encode year, gen(year_id)
reshape long cost_, i(household_id) j(year)
```

## Example: Rural Financial Services Questionnaire (Reference)

See [references/rural-finance-template.md](references/rural-finance-template.md) for a complete 40+ question template covering:

- Household demographics
- Land & agriculture
- Income & expenditure
- Savings & credit access
- Insurance
- Payment services
- Investment
- Property rights

## Example: Panel Data Economic Empowerment Questionnaire (Reference)

See [references/panel-empowerment-template.md](references/panel-empowerment-template.md) for a 3-year tracking questionnaire with:

- Pre-post intervention design
- Mediator measurement (tech adoption, social capital, risk coping)
- Moderator measurement (policy, geography)
- Stata-ready coding scheme

## Example: Ghana Rice Farmers Financial Inclusion Questionnaire (Reference)

See [references/ghana-rice-financial-inclusion-template.md](references/ghana-rice-financial-inclusion-template.md) for a full English-language questionnaire on:

- **Research gap**: Digital financial services + agricultural training joint effect; social capital mediation; food security outcomes
- **Study**: Smallholder rice farmers in Northern/North East Ghana
- **Key constructs**: Digital FI (mobile money, credit, savings, insurance), training & extension, technology adoption index, social capital network, food security (FIES module, FCS, HDDS), ABM behavioral parameters (risk aversion, time preference, herding)
- **Sampling**: Cochran formula n=640 with 1.5 Deff cluster design
- **Stata code**: Full variable coding, mediation analysis, fixed effects, ABM parameter extraction

## Scripts

- `scripts/generate_qnaire.py` — Generate structured questionnaire from template
- `scripts/code_stata.do` — Auto-generate Stata coding script from question list

## Quality Checklist

Before finalizing:

- [ ] All questions have unique identifiers
- [ ] Skip logic is complete and consistent
- [ ] Time reference is clear (which year/period?)
- [ ] Sensitive questions are properly framed
- [ ] Economic data tables have units specified
- [ ] Likert scales are balanced (equal positive/negative)
- [ ] Expert review completed (≥3 reviewers)
- [ ] Pilot test with 20-30 respondents
- [ ] Reliability statistics calculated (Cronbach's α)
- [ ] Stata coding scheme documented
