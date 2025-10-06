#!/usr/bin/env python3
"""
Test script for stakeholder commands OutputFormatter integration.

This script validates that the stakeholder_update.md.j2 template works correctly
with stakeholder communication data.
"""

from datetime import datetime, timedelta
from tools import OutputFormatter


def test_stakeholder_update_template():
    """Test stakeholder update template with comprehensive sample data."""

    # Sample stakeholder update data
    stakeholder_data = {
        'period': 'Q4 2024',
        'executive_summary': (
            'Mobile app project progressing on schedule with 75% completion. '
            'Relationship with Executive Team remains strong with consistent engagement '
            'and positive sentiment trends. Key milestones achieved this quarter.'
        ),
        'highlights': [
            'Completed user authentication system',
            'Achieved 95% test coverage across core modules',
            'Deployed beta to internal users with positive feedback',
            'Established weekly technical sync cadence with stakeholder'
        ],
        'progress': {
            'overall': 0.75,
            'milestones': [
                {
                    'name': 'User Authentication',
                    'status': 'completed',
                    'progress': 1.0
                },
                {
                    'name': 'Payment Integration',
                    'status': 'in_progress',
                    'progress': 0.65
                },
                {
                    'name': 'Security Audit',
                    'status': 'pending',
                    'progress': 0.0
                }
            ],
            'on_track': True,
            'target_date': '2025-01-15'
        },
        'accomplishments': [
            'Successfully resolved API integration concerns raised in last meeting',
            'Aligned on Q1 2025 roadmap priorities with full stakeholder buy-in',
            'Established weekly technical sync meetings for improved transparency',
            'Completed beta deployment ahead of schedule'
        ],
        'challenges': [
            {
                'title': 'Third-party API Integration Delays',
                'description': (
                    'Vendor API documentation was incomplete, causing initial integration delays. '
                    'Team spent extra time reverse-engineering API behavior.'
                ),
                'impact': 'Low - Alternative solution identified and implemented',
                'resolution': (
                    'Implemented fallback integration approach using webhook notifications. '
                    'Working with vendor to improve documentation for future projects.'
                )
            },
            {
                'title': 'Resource Allocation Concerns',
                'description': (
                    'Stakeholder expressed concern about team capacity for upcoming Q1 features '
                    'given current workload and parallel projects.'
                ),
                'impact': 'Medium - May affect feature prioritization and timeline',
                'resolution': (
                    'Scheduled dedicated planning session to review resource allocation. '
                    'Exploring options for temporary contractor support.'
                )
            }
        ],
        'upcoming_priorities': [
            'Complete payment integration and testing',
            'Conduct comprehensive security audit',
            'Prepare production deployment infrastructure',
            'Review Q1 2025 feature roadmap with stakeholder input',
            'Discuss team expansion plans for increased capacity'
        ],
        'budget': {
            'utilization': 0.68,
            'remaining': '$125,000',
            'on_track': True
        },
        'resources': [
            {
                'name': 'Engineering Team',
                'status': 'Fully allocated',
                'allocation': 100
            },
            {
                'name': 'QA Resources',
                'status': 'Available',
                'allocation': 75
            },
            {
                'name': 'DevOps Support',
                'status': 'On-demand',
                'allocation': 40
            }
        ],
        'risks': [
            {
                'title': 'Timeline pressure for Q1 launch',
                'severity': 'medium',
                'description': (
                    'Security audit scheduled for December may extend timeline by 1-2 weeks '
                    'if significant issues are discovered.'
                )
            },
            {
                'title': 'Third-party vendor reliability',
                'severity': 'low',
                'description': (
                    'Payment gateway vendor has experienced recent outages. '
                    'Monitoring closely and have backup provider identified.'
                )
            }
        ],
        'support_needed': [
            {
                'description': 'Executive sponsorship for budget increase to hire additional developer',
                'urgency': 'high'
            },
            {
                'description': 'Approval for extended security audit timeline if issues found',
                'urgency': 'medium'
            }
        ],
        'next_steps': [
            {
                'action': 'Complete payment integration and integration testing',
                'owner': 'Engineering Lead',
                'deadline': '2024-12-01'
            },
            {
                'action': 'Schedule Q1 2025 planning meeting with stakeholder',
                'owner': 'Product Manager',
                'deadline': '2024-11-15'
            },
            {
                'action': 'Initiate security audit with external firm',
                'owner': 'Security Team',
                'deadline': '2024-12-10'
            },
            {
                'action': 'Review resource allocation and contractor options',
                'owner': 'Engineering Manager',
                'deadline': '2024-11-20'
            }
        ],
        'contacts': [
            {
                'name': 'Sarah Johnson',
                'role': 'Engineering Lead',
                'email': 'sarah.johnson@company.com'
            },
            {
                'name': 'Mike Chen',
                'role': 'Product Manager',
                'email': 'mike.chen@company.com'
            }
        ]
    }

    # Test OutputFormatter with stakeholder_update template
    print("Testing OutputFormatter with stakeholder_update template...")
    print("=" * 80)

    try:
        formatter = OutputFormatter()
        output = formatter.stakeholder_update(
            stakeholder_data,
            stakeholder="Executive Team"
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
            ("Stakeholder specified", "Executive Team" in output.content),
            ("Period present", "Q4 2024" in output.content),
            ("Executive summary", stakeholder_data['executive_summary'][:50] in output.content),
            ("Highlights section", "Key Highlights" in output.content),
            ("Progress section", "Progress Update" in output.content),
            ("Accomplishments listed", "Accomplishments" in output.content),
            ("Challenges section", "Challenges" in output.content),
            ("Upcoming priorities", "Upcoming Priorities" in output.content),
            ("Budget information", "Budget & Resources" in output.content),
            ("Risks section", "Risks & Issues" in output.content),
            ("Support needed", "Required Support" in output.content),
            ("Next steps", "Next Steps" in output.content),
            ("Contact information", "Contact Information" in output.content),
            ("Emoji indicators", any(emoji in output.content for emoji in ['👥', '🎯', '📊', '📈', '🎉', '🚧', '📅', '💰', '⚠️', '🤝', '📞'])),
            ("Progress percentage", "75.0%" in output.content or "75%" in output.content)
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
    success = test_stakeholder_update_template()
    exit(0 if success else 1)
