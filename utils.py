"""
Utility functions for Job IQ scoring and recommendations
"""

def calculate_jdmi_score(responses):
    """
    Calculate Job IQ score across 7 dimensions based on user responses
    
    Args:
        responses: Dictionary of user responses from the form
        
    Returns:
        Dictionary with dimensional scores and total score
    """
    
    scores = {
        'dim1': 0,  # Coverage
        'dim2': 0,  # Governance
        'dim3': 0,  # Velocity
        'dim4': 0,  # Architecture
        'dim5': 0,  # Integration
        'dim6': 0,  # Controls
        'dim7': 0,  # Ability to Act
        'total': 0
    }
    
    # Dimension 1: Coverage/Completeness
    coverage_map = {
        "<25%": 0,
        "25-49%": 1,
        "50-74%": 2,
        "75-89%": 3,
        "≥90%": 4
    }
    scores['dim1'] = coverage_map.get(responses.get('coverage', ''), 0)
    
    # Dimension 2: Governance/Ownership
    governance_map = {
        "Ongoing governed program with clear ownership and regular reviews": 4,
        "Primarily project-based with temporary ownership": 2,
        "Decentralized — each function manages independently": 1,
        "We do not actively manage job/skills data today": 0
    }
    scores['dim2'] = governance_map.get(responses.get('governance', ''), 0)
    
    # Dimension 3: Freshness/Velocity
    velocity_map = {
        "More than 30 days": 0,
        "15-30 days": 1,
        "8-14 days": 2,
        "3-7 days": 3,
        "Less than 3 days": 4
    }
    scores['dim3'] = velocity_map.get(responses.get('velocity', ''), 0)
    
    # Dimension 4: Architecture Alignment (count selected items, max 4)
    arch_count = sum([
        responses.get('arch_mobility', False),
        responses.get('arch_comp', False),
        responses.get('arch_planning', False)
    ])
    scores['dim4'] = min(arch_count, 4)
    
    # Dimension 5: System Integration
    integration_map = {
        "All core systems fully synchronized (HRIS, ATS, Comp, LMS)": 4,
        "Most systems integrated (3 of 4)": 3,
        "Some systems connected, but significant manual work": 1,
        "Systems operate independently (manual exports/imports)": 0
    }
    scores['dim5'] = integration_map.get(responses.get('integration', ''), 0)
    
    # Dimension 6: Controls/Compliance (count selected items, max 4)
    control_count = sum([
        responses.get('control_ownership', False),
        responses.get('control_approvals', False),
        responses.get('control_lineage', False),
        responses.get('control_bias', False)
    ])
    scores['dim6'] = min(control_count, 4)
    
    # Dimension 7: Ability to Act (count decision drivers + metrics, max 4)
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
    
    # Score = min(4, decisions/2 + metrics)
    # This gives weight to both making decisions AND tracking metrics
    scores['dim7'] = min(4, int(act_decisions / 2) + act_metrics)
    
    # Calculate total
    scores['total'] = sum([
        scores['dim1'], scores['dim2'], scores['dim3'], scores['dim4'],
        scores['dim5'], scores['dim6'], scores['dim7']
    ])
    
    return scores


def get_level_info(total_score):
    """
    Map total score to maturity level
    
    Args:
        total_score: Total Job IQ score (0-28)
        
    Returns:
        Dictionary with level information
    """
    
    if total_score >= 22:
        return {
            'number': 5,
            'name': 'Optimized',
            'description': """
            **Congratulations!** Your organization demonstrates world-class job data maturity. You have 
            continuous improvement cycles, predictive analytics, and skills data that drives strategic 
            workforce decisions. Your data is a competitive advantage.
            
            **Characteristics:**
            - Real-time data synchronization across all systems
            - Predictive analytics and AI-driven insights
            - Skills data drives all major talent decisions
            - Continuous improvement with tracked ROI
            - Industry leadership in governance practices
            """
        }
    elif total_score >= 17:
        return {
            'number': 4,
            'name': 'Governed',
            'description': """
            **Well done!** You have systematic governance with integrated systems and clear accountability. 
            Your job data is trustworthy and actionable. Focus now shifts to optimization and advanced 
            analytics capabilities.
            
            **Characteristics:**
            - Comprehensive governance controls in place
            - Systems fully integrated with automated sync
            - Clear ownership and approval workflows
            - Data actively drives talent decisions
            - Regular audits and continuous improvement
            
            **Next Step:** Move from reactive to predictive—build advanced analytics and forecasting capabilities.
            """
        }
    elif total_score >= 11:
        return {
            'number': 3,
            'name': 'Defined',
            'description': """
            **You're at a critical juncture.** You likely have good coverage but inconsistent governance—
            the exact paradox our research uncovered. 91% of organizations at this level are planning major 
            overhauls because their data has become static technical debt rather than a strategic asset.
            
            **Characteristics:**
            - Moderate to high skills coverage (50-75%+)
            - Project-based or informal governance
            - Manual processes and fragmented systems
            - Data exists but isn't driving decisions
            - Planning governance overhauls
            
            **Critical Risk:** Without governance, your coverage becomes stale and untrustworthy.
            
            **Next Step:** Establish formal governance—ownership, approval workflows, system integration—
            before expanding coverage further.
            """
        }
    elif total_score >= 6:
        return {
            'number': 2,
            'name': 'Emerging',
            'description': """
            **You're building momentum.** You have some foundational elements in place but lack the 
            systematic approach needed for scale. Your job data efforts are reactive and siloed.
            
            **Characteristics:**
            - Limited skills coverage (25-50%)
            - Primarily ad-hoc or project-based efforts
            - Decentralized ownership across functions
            - Systems operate independently
            - Minimal governance controls
            
            **Key Challenge:** Scaling without governance will create the coverage paradox—more data, 
            but no control over quality or consistency.
            
            **Next Step:** Define an operating model and assign clear ownership before expanding coverage.
            """
        }
    else:
        return {
            'number': 1,
            'name': 'Ad Hoc',
            'description': """
            **You're at the beginning.** Job and skills data management is informal or non-existent. 
            You're likely feeling pain around inconsistent job descriptions, lengthy hiring cycles, 
            and inability to make data-driven workforce decisions.
            
            **Characteristics:**
            - Minimal skills coverage (<25%)
            - No formal governance or ownership
            - Each function manages independently
            - Systems completely disconnected
            - High cycle times and manual work
            
            **Key Challenge:** Without foundational structure, every talent initiative starts from scratch.
            
            **Next Step:** Start with a pilot—define ownership, establish a small governed inventory, 
            and demonstrate quick wins to build executive support.
            """
        }


def get_recommendations(scores, level):
    """
    Generate personalized recommendations based on scores and level
    
    Args:
        scores: Dictionary of dimensional scores
        level: Maturity level (1-5)
        
    Returns:
        List of recommendation dictionaries
    """
    
    recommendations = []
    
    # Get dimension scores as list
    dim_scores = [
        scores['dim1'], scores['dim2'], scores['dim3'], scores['dim4'],
        scores['dim5'], scores['dim6'], scores['dim7']
    ]
    
    dim_names = [
        "Coverage/Completeness",
        "Governance/Ownership",
        "Freshness/Velocity",
        "Architecture Alignment",
        "System Integration",
        "Controls/Compliance",
        "Ability to Act"
    ]
    
    # Find lowest scoring dimensions (priority gaps)
    lowest_score = min(dim_scores)
    lowest_dims = [i for i, score in enumerate(dim_scores) if score == lowest_score]
    
    # Level-specific strategic recommendations
    if level == 1:
        recommendations.append({
            'title': 'Establish Foundational Governance',
            'description': 'Assign a clear owner for job data governance. Start with 10-20 critical roles and establish a governed process for maintaining them. This creates the foundation for scaling.'
        })
        recommendations.append({
            'title': 'Build Your Pilot',
            'description': 'Choose one high-value use case (e.g., critical hiring roles or equity audit). Define skills, implement basic approval workflow, and track cycle time improvement. Use this to build executive support.'
        })
    
    elif level == 2:
        recommendations.append({
            'title': 'Formalize Your Operating Model',
            'description': 'Move from ad-hoc projects to an ongoing governed program. Define ownership across HR, Talent Acquisition, and Comp. Establish regular review cadences (quarterly minimum).'
        })
        recommendations.append({
            'title': 'Integrate Your Core Systems',
            'description': 'Connect HRIS, ATS, and Compensation systems to ensure job data flows automatically. This eliminates manual rework and ensures consistency across recruiting, hiring, and comp decisions.'
        })
    
    elif level == 3:
        recommendations.append({
            'title': '⚠️ Address the Coverage-Governance Gap',
            'description': 'You likely have decent coverage but weak governance—the exact trap our research identified. Before expanding coverage further, implement formal approval workflows, version control, and system synchronization. Otherwise your data becomes stale technical debt.'
        })
        recommendations.append({
            'title': 'Implement Change Management Process',
            'description': 'Establish SLAs for job updates (target: <7 days from request to publish). Create lightweight approval workflows that balance control with velocity. Track time-to-publish as a key metric.'
        })
    
    elif level == 4:
        recommendations.append({
            'title': 'Build Advanced Analytics Capabilities',
            'description': 'Move from descriptive to predictive analytics. Build dashboards that surface skill gaps, succession risks, and mobility opportunities. Empower business leaders with self-service insights.'
        })
        recommendations.append({
            'title': 'Expand to Strategic Workforce Planning',
            'description': 'Link your job architecture to 3-year workforce planning. Model future skill needs, identify build-vs-buy decisions, and quantify cost of skill gaps. Your governance foundation enables this.'
        })
    
    else:  # level == 5
        recommendations.append({
            'title': 'Drive Industry Leadership',
            'description': 'Share your practices at conferences and with industry peers. Your maturity model can influence how the broader market approaches job data governance. Consider publishing case studies.'
        })
        recommendations.append({
            'title': 'Continuous Innovation',
            'description': 'Explore AI-driven job description generation, real-time labor market intelligence integration, and predictive skill obsolescence modeling. Stay at the forefront of the field.'
        })
    
    # Dimension-specific recommendations (add top 2-3 gaps)
    dim_recommendations = {
        0: {  # Coverage
            'title': 'Expand Skills Coverage Strategically',
            'description': 'Start with high-impact roles: critical hiring needs, executive positions, or roles with equity concerns. Use JDX\'s AI-assisted tools to accelerate inventory creation while maintaining quality.'
        },
        1: {  # Governance
            'title': 'Establish Governance Program',
            'description': 'Assign a dedicated owner (e.g., Talent Management, HRBP lead). Define approval workflows with 3-5 day SLAs. Implement version control and audit trails. Move from projects to program.'
        },
        2: {  # Velocity
            'title': 'Accelerate Time-to-Publish',
            'description': 'Your current cycle time is slowing hiring and comp decisions. Streamline approvals, automate status notifications, and implement async review processes. Target: <7 days for standard updates, <3 days for urgent.'
        },
        3: {  # Architecture
            'title': 'Build Job Architecture Framework',
            'description': 'Define job levels, families, and career paths. Link skills to career progression and compensation bands. This scaffolding enables mobility, equity, and workforce planning initiatives.'
        },
        4: {  # Integration
            'title': 'Integrate HR Systems',
            'description': 'Connect HRIS, ATS, LMS, and Compensation systems to create a single source of truth. Automate data propagation when jobs are updated. Eliminate manual exports/imports and version conflicts.'
        },
        5: {  # Controls
            'title': 'Implement Governance Controls',
            'description': 'Add formal approval workflows, version history, and bias review checks. These controls ensure quality, compliance, and auditability—critical for legal defensibility and AI readiness.'
        },
        6: {  # Ability to Act
            'title': 'Enable Data-Driven Decisions',
            'description': 'Build analytics dashboards and link skills data to business processes (hiring, promotion, reskilling). Track metrics like cycle time, mobility rate, and time-to-fill. Demonstrate ROI to sustain investment.'
        }
    }
    
    # Add top 2 dimension-specific recommendations
    for dim_idx in lowest_dims[:2]:
        if dim_scores[dim_idx] <= 2:  # Only add if significant gap
            recommendations.append(dim_recommendations[dim_idx])
    
    # Add cross-cutting recommendation if system integration is low
    if scores['dim5'] <= 1 and 4 not in lowest_dims:
        recommendations.append({
            'title': 'Prioritize System Integration',
            'description': 'Siloed systems create version conflicts and manual rework. Integrating HRIS, ATS, and Comp systems will have outsized impact on data quality and operational efficiency.'
        })
    
    # Add AI readiness recommendation for Level 3+ organizations
    if level >= 3 and (scores['dim6'] <= 2 or scores['dim7'] <= 2):
        recommendations.append({
            'title': 'Prepare for AI-Driven Workforce Decisions',
            'description': 'AI tools require clean, governed skills data. Without strong controls and analytics, AI will amplify existing data quality issues. Treat governance as a prerequisite for AI adoption—not an afterthought.'
        })
    
    return recommendations[:5]  # Return top 5 recommendations


def get_dimension_descriptions():
    """
    Return detailed descriptions of each dimension for reference
    
    Returns:
        Dictionary of dimension descriptions
    """
    
    return {
        'dim1': {
            'name': 'Coverage/Completeness',
            'description': 'What percentage of your job descriptions include defined skills or competencies? Coverage is the foundation—but our research shows coverage ≠ maturity.',
            'why_it_matters': 'Without baseline coverage, you can\'t execute on skills-based initiatives. However, high coverage without governance leads to stale, untrustworthy data.'
        },
        'dim2': {
            'name': 'Governance/Ownership',
            'description': 'Do you have a repeatable process with clear accountability for managing job data? Or is it ad-hoc and project-based?',
            'why_it_matters': 'Governance determines whether your data is an asset or liability. Without it, coverage becomes technical debt.'
        },
        'dim3': {
            'name': 'Freshness/Velocity',
            'description': 'How quickly can you respond to business needs by updating job descriptions? Measured as time from request to publication.',
            'why_it_matters': 'Lengthy approval cycles bottleneck hiring, compensation changes, and workforce planning. Velocity indicates operational maturity.'
        },
        'dim4': {
            'name': 'Architecture Alignment',
            'description': 'Is there a coherent framework—job levels, families, career paths—that scaffolds your job data and enables consistency?',
            'why_it_matters': 'Architecture enables mobility, equity, and workforce planning. Without it, every job is an island.'
        },
        'dim5': {
            'name': 'System Integration',
            'description': 'Are job data updates automatically propagated across HR systems? Or do systems operate independently with manual syncing?',
            'why_it_matters': 'Fragmentation creates version conflicts, manual rework, and "which system is right?" debates. Integration ensures single source of truth.'
        },
        'dim6': {
            'name': 'Controls/Compliance',
            'description': 'Do you have guardrails—approval workflows, version history, bias review—to ensure quality and compliance?',
            'why_it_matters': 'Controls mitigate legal risk, ensure equity, and prepare you for AI. Without them, you can\'t defend your job data in an audit or lawsuit.'
        },
        'dim7': {
            'name': 'Ability to Act',
            'description': 'Can stakeholders extract insights and drive decisions from your job/skills data? Or is data trapped in spreadsheets?',
            'why_it_matters': 'Data only delivers ROI when it drives action. Analytics, dashboards, and process integration turn inventory into impact.'
        }
    }

