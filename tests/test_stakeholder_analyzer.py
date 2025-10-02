#!/usr/bin/env python3
"""
Comprehensive tests for StakeholderAnalyzer tool.

Tests stakeholder discovery, power-interest mapping, alignment assessment,
and communication planning.
Target: >80% code coverage
"""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from tools.stakeholder_analyzer import StakeholderAnalyzer, StakeholderAnalyzerError
from tools.stakeholder_models import (
    AlignmentStatus,
    CommunicationPriority,
    InfluenceLevel,
    InterestLevel,
    PowerInterestQuadrant,
    Stakeholder,
)


class TestStakeholderAnalyzer(unittest.TestCase):
    """Test suite for StakeholderAnalyzer."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = StakeholderAnalyzer()

        self.sample_stakeholders = [
            Stakeholder(
                id="ceo-jane",
                name="Jane Smith",
                role="CEO",
                email="jane@company.com",
                department="Executive",
                influence_level=InfluenceLevel.VERY_HIGH,
                interest_areas=["revenue", "strategic_direction"],
                communication_style="data_driven",
                decision_factors=["roi", "strategic_alignment"],
                authority_scope=["budget_approval", "strategic_decisions"],
                relationship_strength="strong",
            ),
            Stakeholder(
                id="cto-mike",
                name="Mike Johnson",
                role="CTO",
                email="mike@company.com",
                department="Engineering",
                influence_level=InfluenceLevel.HIGH,
                interest_areas=["technical_architecture", "team_capability"],
                communication_style="technical_deep_dive",
                decision_factors=["scalability", "maintainability"],
                authority_scope=["technical_decisions"],
                relationship_strength="collaborative",
            ),
            Stakeholder(
                id="dev-sarah",
                name="Sarah Johnson",
                role="Senior Developer",
                email="sarah@company.com",
                department="Engineering",
                influence_level=InfluenceLevel.MEDIUM,
                interest_areas=["mobile_development", "react_native"],
                communication_style="technical",
                decision_factors=["technical_feasibility"],
                authority_scope=[],
            ),
        ]

    @patch.object(StakeholderAnalyzer, "_load_stakeholder_database")
    @patch.object(StakeholderAnalyzer, "_load_stakeholder_contexts")
    def test_identify_stakeholders_by_impact_area(self, mock_contexts, mock_database):
        """Test stakeholder identification by impact area."""
        mock_database.return_value = {
            "stakeholders": [
                {
                    "id": "ceo-jane",
                    "name": "Jane Smith",
                    "role": "CEO",
                    "email": "jane@company.com",
                    "department": "Executive",
                    "influence_level": "very_high",
                },
                {
                    "id": "cto-mike",
                    "name": "Mike Johnson",
                    "role": "CTO",
                    "email": "mike@company.com",
                    "department": "Engineering",
                    "influence_level": "high",
                },
            ]
        }
        mock_contexts.return_value = {"stakeholder_profiles": {}}

        decision_context = {
            "decision_type": "technical",
            "scope": "mobile_app",
            "impact_areas": ["Engineering"],
        }

        stakeholders = self.analyzer.identify_stakeholders(decision_context)

        self.assertGreater(len(stakeholders), 0)
        # Should find CTO since department matches
        engineering_stakeholders = [s for s in stakeholders if s.department == "Engineering"]
        self.assertGreater(len(engineering_stakeholders), 0)

    @patch.object(StakeholderAnalyzer, "_load_stakeholder_database")
    @patch.object(StakeholderAnalyzer, "_load_stakeholder_contexts")
    def test_identify_stakeholders_by_interest_area(self, mock_contexts, mock_database):
        """Test stakeholder identification by interest area."""
        mock_database.return_value = {
            "stakeholders": [
                {
                    "id": "dev-sarah",
                    "name": "Sarah",
                    "role": "Developer",
                    "email": "sarah@company.com",
                    "department": "Engineering",
                    "interest_areas": ["mobile_development", "react_native"],
                },
            ]
        }
        mock_contexts.return_value = {"stakeholder_profiles": {}}

        decision_context = {
            "decision_type": "technical",
            "scope": "mobile",
            "impact_areas": [],
        }

        stakeholders = self.analyzer.identify_stakeholders(decision_context)

        self.assertGreater(len(stakeholders), 0)

    def test_map_power_interest_grid(self):
        """Test power-interest grid mapping."""
        decision_context = {
            "decision_type": "technical",
            "scope": "mobile_app",
        }

        grid = self.analyzer.map_power_interest(
            self.sample_stakeholders,
            decision_context,
        )

        # Verify grid structure
        self.assertEqual(len(grid.positions), 3)
        self.assertIn("decision_context", grid.to_dict())

        # Check that positions are calculated
        for position in grid.positions:
            self.assertGreaterEqual(position.power_score, 0.0)
            self.assertLessEqual(position.power_score, 1.0)
            self.assertGreaterEqual(position.interest_score, 0.0)
            self.assertLessEqual(position.interest_score, 1.0)
            self.assertIsInstance(position.quadrant, PowerInterestQuadrant)

    def test_map_power_interest_quadrants(self):
        """Test quadrant assignment logic."""
        grid = self.analyzer.map_power_interest(
            self.sample_stakeholders,
            {"decision_type": "strategic"},
        )

        # CEO should be high power
        ceo_positions = [p for p in grid.positions if p.stakeholder_id == "ceo-jane"]
        self.assertEqual(len(ceo_positions), 1)
        self.assertGreaterEqual(ceo_positions[0].power_score, 0.7)

        # Check quadrant counts
        manage_closely = grid.get_by_quadrant(PowerInterestQuadrant.MANAGE_CLOSELY)
        self.assertIsInstance(manage_closely, list)

    def test_calculate_influence_scores(self):
        """Test influence score calculation."""
        scores = self.analyzer.calculate_influence_scores(
            self.sample_stakeholders,
            decision_type="technical",
        )

        # Verify scores for all stakeholders
        self.assertEqual(len(scores), 3)

        # Check CEO has high influence
        ceo_score = scores.get("ceo-jane")
        self.assertIsNotNone(ceo_score)
        self.assertGreater(ceo_score.overall_score, 0.6)
        self.assertGreaterEqual(ceo_score.power_component, 0.0)
        self.assertLessEqual(ceo_score.overall_score, 1.0)

        # Check components
        for stakeholder_id, score in scores.items():
            self.assertGreaterEqual(score.power_component, 0.0)
            self.assertLessEqual(score.power_component, 1.0)
            self.assertGreaterEqual(score.interest_component, 0.0)
            self.assertLessEqual(score.interest_component, 1.0)

    def test_assess_alignment(self):
        """Test alignment assessment."""
        decision_options = ["Option A: React Native", "Option B: Flutter"]

        alignment = self.analyzer.assess_alignment(
            self.sample_stakeholders,
            decision_options,
        )

        # Verify alignment structure
        self.assertEqual(len(alignment.alignments), 3)
        self.assertGreaterEqual(alignment.overall_support_score, 0.0)
        self.assertLessEqual(alignment.overall_support_score, 1.0)
        self.assertGreaterEqual(alignment.consensus_likelihood, 0.0)
        self.assertLessEqual(alignment.consensus_likelihood, 1.0)

        # Check alignment details
        for stakeholder_alignment in alignment.alignments:
            self.assertIsInstance(stakeholder_alignment.alignment_status, AlignmentStatus)
            self.assertGreaterEqual(stakeholder_alignment.confidence, 0.0)
            self.assertLessEqual(stakeholder_alignment.confidence, 1.0)

    def test_assess_alignment_identifies_supporters(self):
        """Test that alignment identifies key supporters and resistors."""
        decision_options = ["Option A: React Native"]

        alignment = self.analyzer.assess_alignment(
            self.sample_stakeholders,
            decision_options,
        )

        # Should have identified stakeholders
        self.assertIsInstance(alignment.key_supporters, list)
        self.assertIsInstance(alignment.key_resistors, list)
        self.assertIsInstance(alignment.coalition_opportunities, list)

    def test_generate_communication_plan(self):
        """Test communication plan generation."""
        decision = {
            "title": "Mobile Tech Stack Decision",
            "rationale": "Need to choose between React Native and Flutter",
        }

        plan = self.analyzer.generate_communication_plan(
            self.sample_stakeholders,
            decision,
        )

        # Verify plan structure
        self.assertEqual(len(plan.messages), 3)
        self.assertEqual(plan.decision_context, "Mobile Tech Stack Decision")
        self.assertIsNotNone(plan.overall_strategy)
        self.assertIsInstance(plan.communication_sequence, list)

        # Check messages
        for message in plan.messages:
            self.assertIn(message.stakeholder_id, ["ceo-jane", "cto-mike", "dev-sarah"])
            self.assertIsInstance(message.priority, CommunicationPriority)
            self.assertGreater(len(message.key_points), 0)

    def test_generate_communication_plan_priorities(self):
        """Test that high-influence stakeholders get immediate priority."""
        decision = {"title": "Important Decision"}

        plan = self.analyzer.generate_communication_plan(
            self.sample_stakeholders,
            decision,
        )

        # CEO should have immediate priority
        ceo_messages = [m for m in plan.messages if m.stakeholder_id == "ceo-jane"]
        self.assertEqual(len(ceo_messages), 1)
        self.assertEqual(ceo_messages[0].priority, CommunicationPriority.IMMEDIATE)

    def test_adapt_message_data_driven(self):
        """Test message adaptation for data-driven style."""
        stakeholder = self.sample_stakeholders[0]  # CEO with data_driven style
        base_message = "We need to make a decision"

        adapted = self.analyzer.adapt_message(
            base_message,
            stakeholder,
            message_type="email",
        )

        self.assertIn("data", adapted.lower())

    def test_adapt_message_technical(self):
        """Test message adaptation for technical style."""
        stakeholder = self.sample_stakeholders[1]  # CTO with technical_deep_dive style
        base_message = "Technical solution proposed"

        adapted = self.analyzer.adapt_message(
            base_message,
            stakeholder,
            message_type="email",
        )

        self.assertIn("technical", adapted.lower())

    def test_load_stakeholder_profiles(self):
        """Test loading specific stakeholder profiles."""
        with patch.object(self.analyzer, "_load_stakeholder_database") as mock_db, \
             patch.object(self.analyzer, "_load_stakeholder_contexts") as mock_ctx:

            mock_db.return_value = {
                "stakeholders": [
                    {
                        "id": "ceo-jane",
                        "name": "Jane Smith",
                        "role": "CEO",
                        "email": "jane@company.com",
                        "department": "Executive",
                        "influence_level": "very_high",
                    }
                ]
            }
            mock_ctx.return_value = {"stakeholder_profiles": {}}

            profiles = self.analyzer.load_stakeholder_profiles(["ceo-jane"])

            self.assertEqual(len(profiles), 1)
            self.assertEqual(profiles[0].name, "Jane Smith")

    def test_sync_with_team_roster(self):
        """Test synchronization with team roster."""
        with patch.object(self.analyzer.config_manager, "load_config") as mock_load:
            mock_load.side_effect = [
                {"team_members": {"jane@company.com": {}}},  # team_roster.yaml
                {"stakeholder_profiles": {"jane@company.com": {}}},  # stakeholder_contexts.yaml
            ]

            count = self.analyzer.sync_with_team_roster()

            self.assertGreaterEqual(count, 0)

    def test_sync_with_projects(self):
        """Test synchronization with projects."""
        with patch.object(self.analyzer.config_manager, "load_config") as mock_load:
            mock_load.return_value = {
                "projects": {
                    "mobile-app": {"owner": "jane@company.com"},
                }
            }

            project_stakeholders = self.analyzer.sync_with_projects()

            self.assertIsInstance(project_stakeholders, dict)
            if "mobile-app" in project_stakeholders:
                self.assertIsInstance(project_stakeholders["mobile-app"], list)

    def test_identify_conflicts(self):
        """Test conflict identification."""
        # Create alignment with conflicts
        alignment = self.analyzer.assess_alignment(
            self.sample_stakeholders,
            ["Option A"],
        )

        conflicts = self.analyzer.identify_conflicts(alignment)

        self.assertIsInstance(conflicts, list)

    def test_get_performance_stats(self):
        """Test performance statistics tracking."""
        # Run some operations
        self.analyzer.identify_stakeholders({"decision_type": "technical", "impact_areas": []})
        self.analyzer.identify_stakeholders({"decision_type": "strategic", "impact_areas": []})

        stats = self.analyzer.get_performance_stats()

        self.assertIn("average_time_ms", stats)
        self.assertIn("max_time_ms", stats)
        self.assertIn("total_operations", stats)
        self.assertEqual(stats["total_operations"], 2)

    def test_power_score_calculation(self):
        """Test power score calculation logic."""
        # Test with different influence levels
        high_influence = Stakeholder(
            id="test1",
            name="Test",
            role="VP",
            email="test@example.com",
            influence_level=InfluenceLevel.VERY_HIGH,
        )

        low_influence = Stakeholder(
            id="test2",
            name="Test2",
            role="Developer",
            email="test2@example.com",
            influence_level=InfluenceLevel.LOW,
        )

        power_high = self.analyzer._calculate_power_score(high_influence, {})
        power_low = self.analyzer._calculate_power_score(low_influence, {})

        self.assertGreater(power_high, power_low)
        self.assertGreaterEqual(power_high, 0.7)
        self.assertLessEqual(power_low, 0.5)

    def test_interest_score_calculation(self):
        """Test interest score calculation logic."""
        stakeholder = Stakeholder(
            id="test",
            name="Test",
            role="Developer",
            email="test@example.com",
            interest_areas=["mobile_development", "react_native"],
        )

        context_relevant = {
            "scope": "mobile_development",
            "decision_type": "technical",
        }

        context_irrelevant = {
            "scope": "backend_architecture",
            "decision_type": "technical",
        }

        interest_relevant = self.analyzer._calculate_interest_score(stakeholder, context_relevant)
        interest_irrelevant = self.analyzer._calculate_interest_score(stakeholder, context_irrelevant)

        self.assertGreater(interest_relevant, interest_irrelevant)

    def test_quadrant_determination(self):
        """Test quadrant determination logic."""
        # High power, high interest -> Manage Closely
        quadrant1 = self.analyzer._determine_quadrant(0.8, 0.8)
        self.assertEqual(quadrant1, PowerInterestQuadrant.MANAGE_CLOSELY)

        # High power, low interest -> Keep Satisfied
        quadrant2 = self.analyzer._determine_quadrant(0.8, 0.3)
        self.assertEqual(quadrant2, PowerInterestQuadrant.KEEP_SATISFIED)

        # Low power, high interest -> Keep Informed
        quadrant3 = self.analyzer._determine_quadrant(0.3, 0.8)
        self.assertEqual(quadrant3, PowerInterestQuadrant.KEEP_INFORMED)

        # Low power, low interest -> Monitor
        quadrant4 = self.analyzer._determine_quadrant(0.3, 0.3)
        self.assertEqual(quadrant4, PowerInterestQuadrant.MONITOR)

    def test_stakeholder_to_dict(self):
        """Test stakeholder serialization."""
        stakeholder = self.sample_stakeholders[0]
        stakeholder_dict = stakeholder.to_dict()

        self.assertIn("id", stakeholder_dict)
        self.assertIn("name", stakeholder_dict)
        self.assertIn("role", stakeholder_dict)
        self.assertEqual(stakeholder_dict["name"], "Jane Smith")

    def test_power_interest_grid_get_by_quadrant(self):
        """Test getting stakeholders by quadrant."""
        grid = self.analyzer.map_power_interest(
            self.sample_stakeholders,
            {"decision_type": "technical"},
        )

        for quadrant in PowerInterestQuadrant:
            stakeholders = grid.get_by_quadrant(quadrant)
            self.assertIsInstance(stakeholders, list)

    def test_power_interest_grid_get_high_influence(self):
        """Test getting high influence stakeholders."""
        grid = self.analyzer.map_power_interest(
            self.sample_stakeholders,
            {"decision_type": "strategic"},
        )

        high_influence = grid.get_high_influence(threshold=0.6)
        self.assertIsInstance(high_influence, list)

        # CEO should be in high influence
        ceo_in_list = any(p.stakeholder_id == "ceo-jane" for p in high_influence)
        self.assertTrue(ceo_in_list)

    def test_alignment_analysis_get_by_status(self):
        """Test getting alignments by status."""
        alignment = self.analyzer.assess_alignment(
            self.sample_stakeholders,
            ["Option A"],
        )

        for status in AlignmentStatus:
            stakeholders = alignment.get_by_status(status)
            self.assertIsInstance(stakeholders, list)

    def test_communication_plan_get_immediate(self):
        """Test getting immediate communications."""
        plan = self.analyzer.generate_communication_plan(
            self.sample_stakeholders,
            {"title": "Decision"},
        )

        immediate = plan.get_immediate_communications()
        self.assertIsInstance(immediate, list)

        # CEO should have immediate communication
        ceo_immediate = any(m.stakeholder_id == "ceo-jane" for m in immediate)
        self.assertTrue(ceo_immediate)

    def test_communication_plan_get_by_stakeholder(self):
        """Test getting messages for specific stakeholder."""
        plan = self.analyzer.generate_communication_plan(
            self.sample_stakeholders,
            {"title": "Decision"},
        )

        ceo_messages = plan.get_by_stakeholder("ceo-jane")
        self.assertEqual(len(ceo_messages), 1)
        self.assertEqual(ceo_messages[0].stakeholder_id, "ceo-jane")


class TestStakeholderModels(unittest.TestCase):
    """Test suite for stakeholder models."""

    def test_stakeholder_creation(self):
        """Test stakeholder object creation."""
        stakeholder = Stakeholder(
            id="test-id",
            name="Test User",
            role="Manager",
            email="test@example.com",
        )

        self.assertEqual(stakeholder.id, "test-id")
        self.assertEqual(stakeholder.name, "Test User")
        self.assertEqual(stakeholder.role, "Manager")

    def test_power_interest_position_to_dict(self):
        """Test power interest position serialization."""
        from tools.stakeholder_models import PowerInterestPosition

        position = PowerInterestPosition(
            stakeholder_id="test",
            power_score=0.8,
            interest_score=0.7,
            quadrant=PowerInterestQuadrant.MANAGE_CLOSELY,
            influence_level=InfluenceLevel.HIGH,
            interest_level=InterestLevel.HIGH,
            reasoning="Test reasoning",
        )

        position_dict = position.to_dict()

        self.assertEqual(position_dict["power_score"], 0.8)
        self.assertEqual(position_dict["interest_score"], 0.7)
        self.assertEqual(position_dict["quadrant"], "manage_closely")

    def test_alignment_analysis_to_dict(self):
        """Test alignment analysis serialization."""
        from tools.stakeholder_models import AlignmentAnalysis, StakeholderAlignment

        alignment = AlignmentAnalysis(
            alignments=[],
            decision_context="Test Decision",
            decision_options=["Option A", "Option B"],
            overall_support_score=0.75,
        )

        alignment_dict = alignment.to_dict()

        self.assertEqual(alignment_dict["decision_context"], "Test Decision")
        self.assertEqual(alignment_dict["overall_support_score"], 0.75)
        self.assertIn("alignment_distribution", alignment_dict)


if __name__ == "__main__":
    unittest.main()
