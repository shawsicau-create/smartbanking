#!/usr/bin/env python3
"""
Stata Code Generator from Questionnaire Variable List
Generates ready-to-use Stata do-file for variable coding and analysis
"""

import argparse
import re
from pathlib import Path

def parse_variables(var_list_path):
    """Parse variable definitions from markdown or text file"""
    with open(var_list_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    variables = []
    # Pattern: | Q# | Item | Scale/Options | Stata Var |
    pattern = r'\|\s*\d+[-.]?\d*\s*\|.+?\|\s*(\w+)\s*\|'
    
    for match in re.finditer(pattern, content):
        var_name = match.group(1)
        if var_name and not var_name.startswith('---'):
            variables.append(var_name)
    
    return variables

def generate_stata_code(variables, output_path, panel=False):
    """Generate Stata do-file for variable coding"""
    
    output = []
    output.append("* ============================================")
    output.append("* Questionnaire Variable Coding: Auto-generated")
    output.append("* ============================================")
    output.append("")
    output.append("clear all")
    output.append("cap log close")
    output.append("")
    output.append('log using "coding_log.txt", text replace')
    output.append("")
    
    # Section 1: Data Entry Setup
    output.append("* ----------------------------------------")
    output.append("* SECTION 1: Import/Coding Setup")
    output.append("* ----------------------------------------")
    output.append("")
    output.append('* Import from Excel:')
    output.append('* import excel "questionnaire_data.xlsx", sheet("Sheet1") firstrow clear')
    output.append("")
    
    # Section 2: Variable Labels
    output.append("* ----------------------------------------")
    output.append("* SECTION 2: Variable Labels")
    output.append("* ----------------------------------------")
    output.append("")
    
    for var in variables:
        var_clean = var.replace('_', ' ').title()
        output.append(f'label var {var} "{var_clean}"')
    
    output.append("")
    
    # Section 3: Value Labels
    output.append("* ----------------------------------------")
    output.append("* SECTION 3: Value Labels")
    output.append("* ----------------------------------------")
    output.append("")
    
    # Common value labels for rural finance questionnaires
    common_labels = {
        'gender': '1 "Male" 0 "Female"',
        'education': '0 "No schooling" 1 "Primary" 2 "Middle" 3 "High" 4 "Vocational" 5 "College+"',
        'yes_no': '1 "Yes" 0 "No"',
        'likert5': '1 "Very dissatisfied" 2 "Dissatisfied" 3 "Neutral" 4 "Satisfied" 5 "Very satisfied"',
        'income_change': '1 "Significantly increased" 2 "Slightly increased" 3 "Unchanged" 4 "Slightly decreased" 5 "Significantly decreased"',
        'repay_status': '1 "Early repayment" 2 "On-time" 3 "Late repayment" 4 "Default"',
    }
    
    for var in variables:
        for key, values in common_labels.items():
            if key in var.lower():
                output.append(f'#delim ;')
                output.append(f'la def {key} {values};')
                output.append(f'la val {var} {key};')
                output.append(f'#delim cr')
                output.append("")
                break
    
    # Section 4: Recoding & Transformation
    output.append("* ----------------------------------------")
    output.append("* SECTION 4: Recoding & Transformation")
    output.append("* ----------------------------------------")
    output.append("")
    
    # Log transformation for skewed variables
    output.append("* Log transformation for income/cost variables (add 1 to handle zeros)")
    for var in variables:
        if any(x in var.lower() for x in ['income', 'cost', 'revenue', 'amount', 'fee']):
            output.append(f'gen ln_{var} = ln({var} + 1)')
    
    output.append("")
    
    # Section 5: Index Construction
    output.append("* ----------------------------------------")
    output.append("* SECTION 5: Index Construction")
    output.append("* ----------------------------------------")
    output.append("")
    
    output.append("* Satisfaction index (average of multiple items)")
    output.append("* alpha [varlist], gen(index_name) - for reliability")
    output.append("")
    
    output.append("* Financial inclusion index")
    output.append('egen fin_include = rowtotal(has_account has_credit has_insurance), missing')
    output.append("")
    
    output.append("* Technology adoption score")
    output.append('egen tech_score = rowtotal(tech_tool tech_seed tech_train), missing')
    output.append("")
    
    # Section 6: Panel Data Commands
    if panel:
        output.append("* ----------------------------------------")
        output.append("* SECTION 6: Panel Data Setup")
        output.append("* ----------------------------------------")
        output.append("")
        output.append("* Declare panel structure")
        output.append('xtset household_id year')
        output.append("")
        output.append("* Wide to Long (if data is in wide format)")
        output.append('reshape long [variables with suffix _2023 _2024 _2025], i(household_id) j(year)')
        output.append("")
        
        output.append("* Panel summary statistics")
        output.append('xtsum net_income mf_use cost_total')
        output.append("")
        
        output.append("* Fixed Effects Regression")
        output.append('xtreg net_income mf_use tech_score risk_coping, fe robust')
        output.append("")
        
        output.append("* Random Effects for time-invariant controls")
        output.append('xtreg net_income mf_use age education land_size, re robust')
        output.append("")
        
        output.append("* Hausman test for FE vs RE")
        output.append('xtreg net_income mf_use, fe')
        output.append('estimates store fe')
        output.append('xtreg net_income mf_use, re')
        output.append('estimates store re')
        output.append('hausman fe re')
        output.append("")
    
    # Section 7: Summary Statistics
    output.append("* ----------------------------------------")
    output.append("* SECTION 7: Summary Statistics")
    output.append("* ----------------------------------------")
    output.append("")
    output.append("summarize " + " ".join(variables[:10]) + ", detail")
    output.append("")
    
    # Section 8: Export
    output.append("* ----------------------------------------")
    output.append("* SECTION 8: Export Clean Data")
    output.append("* ----------------------------------------")
    output.append("")
    output.append('save "questionnaire_coded.dta", replace')
    output.append('export excel using "questionnaire_coded.xlsx", replace firstrow(varlabels)')
    output.append("")
    output.append("log close")
    output.append("")
    output.append("* ============================================")
    output.append("* END OF AUTO-GENERATED CODE")
    output.append("* ============================================")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"Stata code generated: {output_path}")
    print(f"Total variables: {len(variables)}")

def main():
    parser = argparse.ArgumentParser(description='Generate Stata code from variable list')
    parser.add_argument('--vars', '-v', required=True, help='Path to variable list file (markdown)')
    parser.add_argument('--output', '-o', required=True, help='Output .do file')
    parser.add_argument('--panel', '-p', action='store_true', help='Include panel data commands')
    
    args = parser.parse_args()
    
    variables = parse_variables(args.vars)
    generate_stata_code(variables, args.output, panel=args.panel)

if __name__ == '__main__':
    main()
