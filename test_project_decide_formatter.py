#!/usr/bin/env python3
"""
Test script for /project-decide OutputFormatter integration.

This script validates that the decision_analysis.md.j2 template works correctly
with structured decision data.
"""

from datetime import datetime, timedelta
from tools import OutputFormatter


def test_decision_analysis_template():
    """Test decision analysis template with comprehensive sample data."""

    # Sample decision data matching the template structure
    decision_data = {
        'decision': {
            'title': 'Technology Stack Selection for New Product Line',
            'description': (
                'We need to choose a modern web framework for our new product line. '
                'The decision impacts team productivity, long-term maintainability, '
                'and time-to-market for our Q1 2025 launch.'
            ),
            'urgency': 'high',
            'deadline': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        },
        'options': [
            {
                'name': 'React with TypeScript',
                'description': 'Modern web framework with strong ecosystem and type safety',
                'score': 0.85,
                'pros': [
                    'Strong ecosystem and community support',
                    'Team already experienced with React',
                    'Excellent tooling and development experience',
                    'TypeScript provides type safety and better IDE support'
                ],
                'cons': [
                    'Higher learning curve for TypeScript',
                    'Requires additional build tooling and configuration',
                    'Larger bundle sizes compared to some alternatives'
                ],
                'criteria_scores': {
                    'strategic_impact': 0.90,
                    'cost_efficiency': 0.80,
                    'implementation_risk': 0.70,
                    'timeline_impact': 0.85,
                    'team_readiness': 0.95
                },
                'estimated_cost': '$50,000 (training and tooling)',
                'estimated_time': '3 months to full productivity'
            },
            {
                'name': 'Vue.js 3',
                'description': 'Progressive framework with gentle learning curve',
                'score': 0.72,
                'pros': [
                    'Gentle learning curve for new team members',
                    'Smaller bundle sizes',
                    'Excellent documentation'
                ],
                'cons': [
                    'Smaller ecosystem compared to React',
                    'Less team experience with Vue',
                    'Fewer enterprise-grade component libraries'
                ],
                'criteria_scores': {
                    'strategic_impact': 0.70,
                    'cost_efficiency': 0.85,
                    'implementation_risk': 0.80,
                    'timeline_impact': 0.65,
                    'team_readiness': 0.60
                },
                'estimated_cost': '$30,000 (training)',
                'estimated_time': '2 months to full productivity'
            },
            {
                'name': 'Status Quo (jQuery + vanilla JS)',
                'description': 'Continue with current tech stack',
                'score': 0.40,
                'pros': [
                    'No learning curve or migration effort',
                    'Team is familiar with current approach',
                    'Zero upfront cost'
                ],
                'cons': [
                    'Technical debt accumulation',
                    'Difficulty attracting new talent',
                    'Limited modern development capabilities',
                    'Slower feature development velocity'
                ],
                'criteria_scores': {
                    'strategic_impact': 0.30,
                    'cost_efficiency': 0.90,
                    'implementation_risk': 0.95,
                    'timeline_impact': 0.20,
                    'team_readiness': 1.0
                },
                'estimated_cost': '$0',
                'estimated_time': 'Immediate'
            }
        ],
        'recommendation': {
            'option': 'React with TypeScript',
            'reasoning': (
                'React with TypeScript offers the best balance of strategic impact, '
                'team readiness, and long-term maintainability. While the initial '
                'learning curve is higher, the team\'s existing React experience '
                'significantly reduces risk. TypeScript\'s type safety will improve '
                'code quality and reduce bugs, leading to faster development cycles '
                'after the initial ramp-up period. The strong ecosystem ensures '
                'long-term viability and access to best-in-class component libraries.'
            ),
            'confidence': 0.85
        },
        'stakeholder_impact': {
            'Engineering Team': {
                'description': 'Positive alignment with existing React skills, TypeScript learning curve manageable',
                'sentiment': 'positive'
            },
            'Product Management': {
                'description': 'Faster time-to-market after initial training period, better feature velocity',
                'sentiment': 'positive'
            },
            'Executive Leadership': {
                'description': 'Higher upfront cost but strong ROI through improved productivity and code quality',
                'sentiment': 'neutral'
            },
            'Recruiting': {
                'description': 'Modern tech stack improves talent attraction and retention',
                'sentiment': 'positive'
            }
        },
        'risks': [
            {
                'title': 'Learning Curve for TypeScript',
                'severity': 'medium',
                'likelihood': 'high',
                'description': (
                    'Team will need 2-3 weeks to become proficient with TypeScript '
                    'patterns and best practices, potentially slowing initial development.'
                ),
                'mitigation': (
                    'Allocate 2 weeks for team training with TypeScript experts. '
                    'Implement pair programming for first month. Start with gradual '
                    'TypeScript adoption, allowing team to learn incrementally.'
                )
            },
            {
                'title': 'Bundle Size Management',
                'severity': 'low',
                'likelihood': 'medium',
                'description': (
                    'React applications can have larger bundle sizes if not properly '
                    'optimized, impacting page load times.'
                ),
                'mitigation': (
                    'Implement code splitting from day one. Use bundle analyzer to '
                    'monitor size. Establish performance budgets and automated checks '
                    'in CI/CD pipeline.'
                )
            },
            {
                'title': 'Migration Complexity',
                'severity': 'high',
                'likelihood': 'low',
                'description': (
                    'If the decision needs to be reversed, migration away from React '
                    'would be costly and time-consuming.'
                ),
                'mitigation': (
                    'Use feature flags for gradual rollout. Keep domain logic separate '
                    'from framework code. Document architecture decisions and maintain '
                    'clean separation of concerns.'
                )
            }
        ],
        'next_steps': [
            {
                'action': 'Approve framework selection and allocate $50K training budget',
                'owner': 'CTO',
                'deadline': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            },
            {
                'action': 'Schedule TypeScript training for engineering team',
                'owner': 'Engineering Manager',
                'deadline': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
            },
            {
                'action': 'Set up development environment and starter templates',
                'owner': 'Tech Lead',
                'deadline': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            },
            {
                'action': 'Create migration plan for existing codebase',
                'owner': 'Senior Developer',
                'deadline': (datetime.now() + timedelta(days=21)).strftime('%Y-%m-%d')
            }
        ]
    }

    # Test OutputFormatter with decision_analysis template
    print("Testing OutputFormatter with decision_analysis template...")
    print("=" * 80)

    try:
        formatter = OutputFormatter()
        output = formatter.format_markdown(
            decision_data,
            template="decision_analysis"
        )

        print(f"\n✅ Template rendering successful!")
        print(f"Processing time: {output.processing_time_ms:.2f}ms")
        print(f"Template used: {output.template_used}")
        print("\n" + "=" * 80)
        print("RENDERED OUTPUT:")
        print("=" * 80)
        print(output.content)
        print("=" * 80)

        # Validation checks
        print("\n" + "=" * 80)
        print("VALIDATION CHECKS:")
        print("=" * 80)

        checks = [
            ("Decision title present", decision_data['decision']['title'] in output.content),
            ("All options rendered", all(opt['name'] in output.content for opt in decision_data['options'])),
            ("Recommendation present", decision_data['recommendation']['option'] in output.content),
            ("Stakeholder impact section", "Stakeholder Impact" in output.content),
            ("Risk section present", "Risks & Mitigation" in output.content),
            ("Next steps included", "Next Steps" in output.content),
            ("Emoji indicators present", any(emoji in output.content for emoji in ['🎯', '📊', '🎓', '👥', '⚠️', '📅'])),
            ("Health scores formatted", any(score in output.content for score in ['85.0%', '72.0%', '40.0%']))
        ]

        all_passed = True
        for check_name, passed in checks:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status}: {check_name}")
            if not passed:
                all_passed = False

        print("\n" + "=" * 80)
        if all_passed:
            print("✅ ALL VALIDATION CHECKS PASSED!")
        else:
            print("❌ SOME VALIDATION CHECKS FAILED")
        print("=" * 80)

        return all_passed

    except Exception as e:
        print(f"\n❌ Template rendering failed with error:")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_decision_analysis_template()
    exit(0 if success else 1)
