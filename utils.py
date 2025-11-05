"""
Utility functions for JDMI scoring and recommendations
"""

def calculate_jdmi_score(responses):
    """Calculate JDMI score across 7 dimensions"""
    scores = {'dim1': 0, 'dim2': 0, 'dim3': 0, 'dim4': 0, 'dim5': 0, 'dim6': 0, 'dim7': 0}
    
    # Dimension 1: Coverage
    coverage_map = {"<25%": 0, "25-49%": 1, "50-74%": 2, "75-89%": 3, "≥90%": 4}
    scores['dim1'] = coverage_map.get(responses.get('coverage', ''), 0)
    
    # Dimension 2: Governance
    governance_map = {
        "Ongoing governed program with clear ownership and regular reviews": 4,
        "Primarily project-based with temporary ownership": 2,
        "Decentralized — each function manages independently": 1,
        "We do not actively manage job/skills data today": 0
    }
    scores['dim2'] = governance_map.get(responses.get('governance', ''), 0)
    
    # Dimension 3: Velocity
    velocity_map = {
        "More than 30 days": 0, "15-30 days": 1, "8-14 days": 2,
        "3-7 days": 3, "Less than 3 days": 4
    }
    scores['dim3'] = velocity_map.get(responses.get('velocity', ''), 0)
    
    # Dimension 4: Architecture (count selected)
    scores['dim4'] = sum([
        responses.get('arch_mobility', False),
        responses.get('arch_comp', False),
        responses.get('arch_planning', False)
    ])
    
    # Dimension 5: Integration
    integration_map = {
        "All core systems fully synchronized (HRIS, ATS, Comp, LMS)": 4,
        "Most systems integrated (3 of 4)": 3,
        "Some systems connected, but significant manual work": 1,
        "Systems operate independently (manual exports/imports)": 0
    }
    scores['dim5'] = integration_map.get(responses.get('integration', ''), 0)
    
    # Dimension 6: Controls (count selected)
    scores['dim6'] = sum([
        responses.get('control_ownership', False),
        responses.get('control_approvals', False),
        responses.get('control_lineage', False),
        responses.get('control_bias', False)
    ])
    
    # Dimension 7: Ability to Act (decisions + metrics)
    act_decisions = sum([
        responses.get('act_reskilling', False),
        responses.get('act_mobility', False),
        responses.get('act_comp', False),
        responses.get('act_hiring', False),
        responses.get('act_planning', False)
    ])
    act_metrics = sum([
        responses.get('metric_cycle', False),
        responses.get('metric_exception', False),
        responses.get('metric_ttp', False),
        responses.get('metric_mobility', False)
    ])
    scores['dim7'] = min(4, int(act_decisions / 2) + act_metrics)
    
    scores['total'] = sum([scores['dim1'], scores['dim2'], scores['dim3'], 
                           scores['dim4'], scores['dim5'], scores['dim6'], scores['dim7']])
    
    return scores


def get_level_info(total_score):
    """Map score to maturity level"""
    if total_score >= 22:
        return {
            'number': 5, 'name': 'Optimized',
            'description': "**Congratulations!** World-class maturity with continuous improvement, predictive analytics, and skills data driving all strategic decisions."
        }
    elif total_score >= 17:
        return {
            'number': 4, 'name': 'Governed',
            'description': "**Well done!** Systematic governance with integrated systems and clear accountability. Your data is trustworthy and actionable."
        }
    elif total_score >= 11:
        return {
            'number': 3, 'name': 'Defined',
            'description': "**Critical juncture.** You likely have good coverage but inconsistent governance—the exact paradox our research uncovered. 91% at this level plan major overhauls."
        }
    elif total_score >= 6:
        return {
            'number': 2, 'name': 'Emerging',
            'description': "**Building momentum.** Foundational elements exist but lack systematic approach. Efforts are reactive and siloed."
        }
    else:
        return {
            'number': 1, 'name': 'Ad Hoc',
            'description': "**Starting point.** Job/skills management is informal. High pain around inconsistent JDs, slow cycles, and lack of data-driven decisions."
        }


def get_recommendations(scores, level):
    """Generate personalized recommendations"""
    recs = []
    dim_scores = [scores['dim1'], scores['dim2'], scores['dim3'], scores['dim4'],
                  scores['dim5'], scores['dim6'], scores['dim7']]
    
    # Level-specific recommendations
    if level <= 2:
        recs.append({
            'title': 'Establish Foundational Governance',
            'description': 'Assign clear owner for job data. Start with 10-20 critical roles and establish governed process.'
        })
    elif level == 3:
        recs.append({
            'title': '⚠️ Address Coverage-Governance Gap',
            'description': 'You likely have decent coverage but weak governance. Implement approval workflows, version control, and system sync before expanding.'
        })
    elif level == 4:
        recs.append({
            'title': 'Build Advanced Analytics',
            'description': 'Move to predictive analytics. Build dashboards for skill gaps, succession risks, and mobility opportunities.'
        })
    
    # Dimension-specific gaps
    dim_recs = [
        {'title': 'Expand Skills Coverage', 'description': 'Start with high-impact roles. Use AI tools to accelerate inventory creation.'},
        {'title': 'Formalize Governance', 'description': 'Assign dedicated owner, define approval workflows with 3-5 day SLAs, implement version control.'},
        {'title': 'Accelerate Velocity', 'description': 'Streamline approvals to <7 days. Current cycle time is slowing hiring and comp decisions.'},
        {'title': 'Build Job Architecture', 'description': 'Define levels, families, career paths. Link skills to progression and comp bands.'},
        {'title': 'Integrate Systems', 'description': 'Connect HRIS, ATS, LMS, Comp to create single source of truth. Eliminate manual sync.'},
        {'title': 'Add Governance Controls', 'description': 'Implement approval workflows, version history, and bias review for quality and compliance.'},
        {'title': 'Enable Data-Driven Decisions', 'description': 'Build analytics dashboards. Link skills data to hiring, promotion, reskilling processes.'}
    ]
    
    # Add top 2 lowest-scoring dimensions
    lowest_dims = sorted(range(7), key=lambda i: dim_scores[i])[:2]
    for dim_idx in lowest_dims:
        if dim_scores[dim_idx] <= 2:
            recs.append(dim_recs[dim_idx])
    
    return recs[:5]
