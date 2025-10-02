"""
StakeholderAnalyzer - Decision Support and Stakeholder Management Tool

Provides stakeholder identification, influence mapping, alignment assessment,
and communication planning for decision support.

Simplifies command implementation from 100+ lines to 15-20 lines:

    analyzer = StakeholderAnalyzer()
    stakeholders = analyzer.identify_stakeholders(decision_context)
    influence = analyzer.map_power_interest(stakeholders, decision_context)
    alignment = analyzer.assess_alignment(stakeholders, options)
    plan = analyzer.generate_communication_plan(stakeholders, decision)
"""

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from tools.config_manager import ConfigManager
from tools.stakeholder_models import (
    AlignmentAnalysis,
    AlignmentStatus,
    CommunicationMessage,
    CommunicationPlan,
    CommunicationPriority,
    InfluenceLevel,
    InfluenceScore,
    InterestLevel,
    PowerInterestGrid,
    PowerInterestPosition,
    PowerInterestQuadrant,
    Stakeholder,
    StakeholderAlignment,
)


class StakeholderAnalyzerError(Exception):
    """Base exception for StakeholderAnalyzer errors."""
    pass


class StakeholderAnalyzer:
    """
    Stakeholder analysis and decision support system.

    Features:
    - Stakeholder discovery from context
    - Power-interest grid calculations
    - Alignment assessment
    - Communication strategy generation
    - Integration with ConfigManager for stakeholder data

    Example:
        >>> analyzer = StakeholderAnalyzer()
        >>> # Identify stakeholders (100 lines → 4 lines)
        >>> stakeholders = analyzer.identify_stakeholders({
        ...     "decision_type": "technical",
        ...     "scope": "mobile_app",
        ...     "impact_areas": ["engineering", "product"]
        ... })
        >>> print(f"Found {len(stakeholders)} stakeholders")
    """

    def __init__(self, config_root: Optional[Path] = None):
        """
        Initialize StakeholderAnalyzer.

        Args:
            config_root: Root directory for configuration files
        """
        self.config_root = config_root or Path.cwd() / ".claude"
        self.config_manager = ConfigManager(config_root=self.config_root)
        self._performance_stats = []

    def identify_stakeholders(
        self,
        decision_context: Dict[str, Any],
        include_indirect: bool = False,
    ) -> List[Stakeholder]:
        """
        Identify relevant stakeholders based on decision context.

        Args:
            decision_context: Context including decision_type, scope, impact_areas
            include_indirect: Whether to include indirectly affected stakeholders

        Returns:
            List of Stakeholder objects

        Example:
            >>> stakeholders = analyzer.identify_stakeholders({
            ...     "decision_type": "technical",
            ...     "scope": "mobile_app",
            ...     "impact_areas": ["engineering", "product"],
            ... })
        """
        start_time = time.time()

        # Load stakeholder database
        stakeholder_db = self._load_stakeholder_database()
        stakeholder_contexts = self._load_stakeholder_contexts()

        # Extract context parameters
        decision_type = decision_context.get("decision_type", "general")
        scope = decision_context.get("scope", "")
        impact_areas = decision_context.get("impact_areas", [])
        specific_stakeholders = decision_context.get("stakeholders", [])

        identified = []

        # If specific stakeholders mentioned, include them
        if specific_stakeholders:
            for stakeholder_id in specific_stakeholders:
                stakeholder = self._get_stakeholder_by_id(
                    stakeholder_id, stakeholder_db, stakeholder_contexts
                )
                if stakeholder:
                    identified.append(stakeholder)

        # Identify by impact areas (departments)
        for sh_data in stakeholder_db.get("stakeholders", []):
            stakeholder_id = sh_data.get("id", "")
            department = sh_data.get("department", "")

            # Match by department/impact area
            if department.lower() in [area.lower() for area in impact_areas]:
                stakeholder = self._create_stakeholder_from_data(sh_data)
                if stakeholder and stakeholder not in identified:
                    identified.append(stakeholder)

        # Identify by interest areas
        for sh_data in stakeholder_db.get("stakeholders", []):
            interest_areas = sh_data.get("interest_areas", [])

            # Check if stakeholder's interests align with scope
            if scope and any(scope.lower() in area.lower() for area in interest_areas):
                stakeholder = self._create_stakeholder_from_data(sh_data)
                if stakeholder and stakeholder not in identified:
                    identified.append(stakeholder)

        # Identify by authority scope (for decision types)
        for sh_data in stakeholder_db.get("stakeholders", []):
            authority_scope = sh_data.get("authority_scope", [])

            # Match decision type to authority
            relevant_authority = [
                "technical_decisions" if decision_type == "technical" else "",
                "strategic_decisions" if decision_type == "strategic" else "",
                "budget_approval" if decision_type == "budget" else "",
            ]

            if any(auth in authority_scope for auth in relevant_authority if auth):
                stakeholder = self._create_stakeholder_from_data(sh_data)
                if stakeholder and stakeholder not in identified:
                    identified.append(stakeholder)

        # Track performance
        duration_ms = (time.time() - start_time) * 1000
        self._performance_stats.append(duration_ms)

        return identified

    def load_stakeholder_profiles(self, stakeholder_ids: List[str]) -> List[Stakeholder]:
        """
        Load detailed stakeholder profiles by IDs.

        Args:
            stakeholder_ids: List of stakeholder IDs to load

        Returns:
            List of Stakeholder objects with full profiles
        """
        stakeholder_db = self._load_stakeholder_database()
        stakeholder_contexts = self._load_stakeholder_contexts()

        profiles = []
        for stakeholder_id in stakeholder_ids:
            stakeholder = self._get_stakeholder_by_id(
                stakeholder_id, stakeholder_db, stakeholder_contexts
            )
            if stakeholder:
                profiles.append(stakeholder)

        return profiles

    def map_power_interest(
        self,
        stakeholders: List[Stakeholder],
        decision_context: Dict[str, Any],
    ) -> PowerInterestGrid:
        """
        Map stakeholders on power-interest grid.

        Args:
            stakeholders: List of stakeholders to map
            decision_context: Context for power/interest calculation

        Returns:
            PowerInterestGrid with all stakeholder positions

        Example:
            >>> grid = analyzer.map_power_interest(stakeholders, {
            ...     "decision_type": "technical",
            ...     "scope": "mobile_app"
            ... })
            >>> high_priority = grid.get_by_quadrant(PowerInterestQuadrant.MANAGE_CLOSELY)
        """
        positions = []

        for stakeholder in stakeholders:
            # Calculate power score
            power_score = self._calculate_power_score(stakeholder, decision_context)

            # Calculate interest score
            interest_score = self._calculate_interest_score(stakeholder, decision_context)

            # Determine quadrant
            quadrant = self._determine_quadrant(power_score, interest_score)

            # Map to influence/interest levels
            influence_level = self._map_to_influence_level(power_score)
            interest_level = self._map_to_interest_level(interest_score)

            # Create position
            position = PowerInterestPosition(
                stakeholder_id=stakeholder.id,
                power_score=power_score,
                interest_score=interest_score,
                quadrant=quadrant,
                influence_level=influence_level,
                interest_level=interest_level,
                reasoning=self._generate_position_reasoning(
                    stakeholder, power_score, interest_score, quadrant
                ),
            )
            positions.append(position)

        # Create grid
        grid = PowerInterestGrid(
            positions=positions,
            decision_context=decision_context.get("scope", "Decision"),
            summary={
                "high_power_high_interest": len([p for p in positions if p.quadrant == PowerInterestQuadrant.MANAGE_CLOSELY]),
                "high_power_low_interest": len([p for p in positions if p.quadrant == PowerInterestQuadrant.KEEP_SATISFIED]),
                "low_power_high_interest": len([p for p in positions if p.quadrant == PowerInterestQuadrant.KEEP_INFORMED]),
                "low_power_low_interest": len([p for p in positions if p.quadrant == PowerInterestQuadrant.MONITOR]),
            },
        )

        return grid

    def calculate_influence_scores(
        self,
        stakeholders: List[Stakeholder],
        decision_type: str = "general",
    ) -> Dict[str, InfluenceScore]:
        """
        Calculate comprehensive influence scores for stakeholders.

        Args:
            stakeholders: List of stakeholders
            decision_type: Type of decision for context-aware scoring

        Returns:
            Dictionary mapping stakeholder IDs to InfluenceScore objects
        """
        scores = {}

        for stakeholder in stakeholders:
            # Calculate components
            power = self._calculate_power_score(stakeholder, {"decision_type": decision_type})
            interest = self._calculate_interest_score(stakeholder, {"decision_type": decision_type})

            # Network influence (simplified - could be expanded with relationship data)
            network = self._estimate_network_influence(stakeholder)

            # Decision authority
            authority = self._calculate_decision_authority(stakeholder, decision_type)

            # Overall score (weighted average)
            overall = (power * 0.35) + (interest * 0.25) + (network * 0.20) + (authority * 0.20)

            score = InfluenceScore(
                stakeholder_id=stakeholder.id,
                overall_score=overall,
                power_component=power,
                interest_component=interest,
                network_component=network,
                decision_authority=authority,
                factors={
                    "role_weight": 0.3 if stakeholder.role and "VP" in stakeholder.role else 0.15,
                    "department_relevance": 0.2,
                    "authority_scope": len(stakeholder.authority_scope) * 0.1,
                },
            )
            scores[stakeholder.id] = score

        return scores

    def assess_alignment(
        self,
        stakeholders: List[Stakeholder],
        decision_options: List[str],
        historical_patterns: Optional[Dict[str, Any]] = None,
    ) -> AlignmentAnalysis:
        """
        Assess stakeholder alignment with decision options.

        Args:
            stakeholders: List of stakeholders to assess
            decision_options: List of decision options being considered
            historical_patterns: Optional historical alignment data

        Returns:
            AlignmentAnalysis with predicted positions and consensus likelihood

        Example:
            >>> alignment = analyzer.assess_alignment(
            ...     stakeholders,
            ...     ["Option A: React Native", "Option B: Flutter"],
            ...     historical_patterns
            ... )
            >>> print(f"Support: {alignment.overall_support_score:.2f}")
        """
        alignments = []

        for stakeholder in stakeholders:
            # Assess alignment based on factors
            alignment_status, confidence = self._assess_stakeholder_alignment(
                stakeholder, decision_options, historical_patterns
            )

            # Identify concerns and supporting factors
            concerns = self._identify_concerns(stakeholder, decision_options)
            supporting = self._identify_supporting_factors(stakeholder, decision_options)
            resistance = self._identify_resistance_factors(stakeholder, decision_options)

            # Estimate influence on others
            influence_on_others = self._estimate_network_influence(stakeholder)

            alignment = StakeholderAlignment(
                stakeholder_id=stakeholder.id,
                alignment_status=alignment_status,
                confidence=confidence,
                key_concerns=concerns,
                supporting_factors=supporting,
                resistance_factors=resistance,
                predicted_position=self._predict_position(stakeholder, decision_options),
                influence_on_others=influence_on_others,
            )
            alignments.append(alignment)

        # Calculate overall metrics
        support_count = len([a for a in alignments if a.alignment_status in [
            AlignmentStatus.STRONG_SUPPORT, AlignmentStatus.SUPPORT
        ]])
        total = len(alignments)
        overall_support = support_count / total if total > 0 else 0.0

        # Calculate consensus likelihood
        consensus_likelihood = self._calculate_consensus_likelihood(alignments)

        # Identify key players
        key_supporters = [a.stakeholder_id for a in alignments if a.alignment_status == AlignmentStatus.STRONG_SUPPORT]
        key_resistors = [a.stakeholder_id for a in alignments if a.alignment_status == AlignmentStatus.OPPOSITION]

        # Identify conflicts and opportunities
        conflicts = self._identify_conflicts(alignments)
        coalitions = self._identify_coalition_opportunities(alignments)

        analysis = AlignmentAnalysis(
            alignments=alignments,
            decision_context=" | ".join(decision_options),
            decision_options=decision_options,
            overall_support_score=overall_support,
            consensus_likelihood=consensus_likelihood,
            key_supporters=key_supporters,
            key_resistors=key_resistors,
            coalition_opportunities=coalitions,
            conflict_areas=conflicts,
        )

        return analysis

    def identify_conflicts(self, alignment_data: AlignmentAnalysis) -> List[str]:
        """
        Identify potential conflicts from alignment analysis.

        Args:
            alignment_data: AlignmentAnalysis object

        Returns:
            List of identified conflicts
        """
        return alignment_data.conflict_areas

    def generate_communication_plan(
        self,
        stakeholders: List[Stakeholder],
        decision: Dict[str, Any],
        templates: Optional[Dict[str, Any]] = None,
    ) -> CommunicationPlan:
        """
        Generate comprehensive communication strategy.

        Args:
            stakeholders: List of stakeholders
            decision: Decision context and details
            templates: Optional message templates

        Returns:
            CommunicationPlan with tailored messages for each stakeholder

        Example:
            >>> plan = analyzer.generate_communication_plan(
            ...     stakeholders,
            ...     {"title": "Mobile Tech Stack", "rationale": "..."},
            ... )
            >>> immediate = plan.get_immediate_communications()
        """
        messages = []
        decision_title = decision.get("title", "Decision")
        decision_rationale = decision.get("rationale", "")

        # Generate messages for each stakeholder
        for stakeholder in stakeholders:
            message = self._generate_stakeholder_message(
                stakeholder, decision, templates
            )
            messages.append(message)

        # Determine communication sequence
        sequence = self._determine_communication_sequence(stakeholders, messages)

        # Generate overall strategy
        overall_strategy = self._generate_overall_strategy(stakeholders, decision)

        # Identify resistance mitigation
        resistance_mitigation = self._generate_resistance_mitigation(stakeholders)

        plan = CommunicationPlan(
            messages=messages,
            decision_context=decision_title,
            overall_strategy=overall_strategy,
            communication_sequence=sequence,
            timing_strategy="Engage high-influence stakeholders first, build coalition before broad announcement",
            key_messages={
                "executive": ["Strategic alignment", "Business impact", "ROI"],
                "technical": ["Technical rationale", "Implementation plan", "Risk mitigation"],
                "operations": ["Process impact", "Timeline", "Support plan"],
            },
            resistance_mitigation=resistance_mitigation,
            success_metrics=[
                "Stakeholder buy-in rate",
                "Time to consensus",
                "Implementation support level",
            ],
        )

        return plan

    def adapt_message(
        self,
        message: str,
        stakeholder: Stakeholder,
        message_type: str = "email",
    ) -> str:
        """
        Adapt message for specific stakeholder communication style.

        Args:
            message: Base message content
            stakeholder: Target stakeholder
            message_type: Type of communication

        Returns:
            Adapted message text
        """
        # Adapt based on communication style
        style = stakeholder.communication_style or "professional"

        if style == "data_driven":
            adapted = f"Data-driven insights: {message}"
        elif style == "technical_deep_dive":
            adapted = f"Technical details: {message}"
        elif style == "user_focused":
            adapted = f"User impact: {message}"
        elif style == "executive_summary":
            adapted = f"Executive summary: {message}"
        else:
            adapted = message

        return adapted

    def sync_with_team_roster(self) -> int:
        """
        Synchronize stakeholder data with team roster.

        Returns:
            Number of stakeholders synchronized
        """
        # Load team roster
        try:
            team_data = self.config_manager.load_config("team_roster.yaml")
            team_members = team_data.get("team_members", {})

            # Load stakeholder contexts
            stakeholder_data = self.config_manager.load_config("stakeholder_contexts.yaml")
            stakeholder_profiles = stakeholder_data.get("stakeholder_profiles", {})

            # Count synchronized entries
            synced = 0
            for email in team_members.keys():
                if email in stakeholder_profiles:
                    synced += 1

            return synced

        except Exception as e:
            return 0

    def sync_with_projects(self) -> Dict[str, List[str]]:
        """
        Synchronize stakeholders with project data.

        Returns:
            Dictionary mapping projects to stakeholder lists
        """
        try:
            projects_data = self.config_manager.load_config("projects.yaml")
            projects = projects_data.get("projects", {})

            project_stakeholders = {}
            for project_name, project_data in projects.items():
                # Owner is primary stakeholder
                stakeholders = [project_data.get("owner", "")]

                # Could expand to include team members, etc.
                project_stakeholders[project_name] = [s for s in stakeholders if s]

            return project_stakeholders

        except Exception as e:
            return {}

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        if not self._performance_stats:
            return {
                "average_time_ms": 0.0,
                "max_time_ms": 0.0,
                "total_operations": 0,
            }

        return {
            "average_time_ms": sum(self._performance_stats) / len(self._performance_stats),
            "max_time_ms": max(self._performance_stats),
            "total_operations": len(self._performance_stats),
        }

    # Private helper methods

    def _load_stakeholder_database(self) -> Dict[str, Any]:
        """Load stakeholder database from YAML."""
        try:
            return self.config_manager.load_config("stakeholder_database.yaml")
        except Exception:
            return {"stakeholders": []}

    def _load_stakeholder_contexts(self) -> Dict[str, Any]:
        """Load stakeholder contexts from YAML."""
        try:
            return self.config_manager.load_config("stakeholder_contexts.yaml")
        except Exception:
            return {"stakeholder_profiles": {}}

    def _get_stakeholder_by_id(
        self,
        stakeholder_id: str,
        database: Dict[str, Any],
        contexts: Dict[str, Any],
    ) -> Optional[Stakeholder]:
        """Get stakeholder by ID from combined data sources."""
        # Try database first
        for sh_data in database.get("stakeholders", []):
            if sh_data.get("id") == stakeholder_id or sh_data.get("email") == stakeholder_id:
                return self._create_stakeholder_from_data(sh_data)

        # Try contexts
        profiles = contexts.get("stakeholder_profiles", {})
        if stakeholder_id in profiles:
            profile_data = profiles[stakeholder_id]
            return Stakeholder(
                id=stakeholder_id,
                name=profile_data.get("name", ""),
                role=profile_data.get("role", ""),
                email=stakeholder_id,
                department=profile_data.get("department", ""),
            )

        return None

    def _create_stakeholder_from_data(self, data: Dict[str, Any]) -> Stakeholder:
        """Create Stakeholder object from dictionary data."""
        influence_str = data.get("influence_level", "medium")
        influence_level = None
        try:
            influence_level = InfluenceLevel(influence_str)
        except ValueError:
            pass

        return Stakeholder(
            id=data.get("id", ""),
            name=data.get("name", ""),
            role=data.get("role", ""),
            email=data.get("email", ""),
            department=data.get("department"),
            influence_level=influence_level,
            interest_areas=data.get("interest_areas", []),
            communication_style=data.get("communication_style"),
            decision_factors=data.get("decision_factors", []),
            authority_scope=data.get("authority_scope", []),
            relationship_strength=data.get("relationship_strength"),
            last_interaction=data.get("last_interaction"),
            metadata=data,
        )

    def _calculate_power_score(
        self,
        stakeholder: Stakeholder,
        context: Dict[str, Any],
    ) -> float:
        """Calculate power score (0.0-1.0) based on role, authority, influence."""
        score = 0.0

        # Base score from influence level
        if stakeholder.influence_level:
            influence_map = {
                InfluenceLevel.VERY_HIGH: 0.9,
                InfluenceLevel.HIGH: 0.7,
                InfluenceLevel.MEDIUM: 0.5,
                InfluenceLevel.LOW: 0.3,
                InfluenceLevel.MINIMAL: 0.1,
            }
            score = influence_map.get(stakeholder.influence_level, 0.5)
        else:
            # Estimate from role
            role = stakeholder.role.lower() if stakeholder.role else ""
            if any(title in role for title in ["ceo", "president", "chief"]):
                score = 0.9
            elif any(title in role for title in ["vp", "director", "head"]):
                score = 0.7
            elif any(title in role for title in ["manager", "lead"]):
                score = 0.5
            else:
                score = 0.3

        # Adjust based on authority scope
        if len(stakeholder.authority_scope) > 3:
            score = min(1.0, score + 0.1)

        return score

    def _calculate_interest_score(
        self,
        stakeholder: Stakeholder,
        context: Dict[str, Any],
    ) -> float:
        """Calculate interest score (0.0-1.0) based on relevance to decision."""
        score = 0.5  # Default neutral interest

        scope = context.get("scope", "").lower()
        decision_type = context.get("decision_type", "").lower()

        # Check if stakeholder's interest areas match scope
        if scope and stakeholder.interest_areas:
            matching = sum(1 for area in stakeholder.interest_areas if scope in area.lower())
            if matching > 0:
                score = min(1.0, 0.6 + (matching * 0.1))

        # Check if decision type matches department
        if decision_type and stakeholder.department:
            if decision_type in stakeholder.department.lower():
                score = min(1.0, score + 0.2)

        return score

    def _determine_quadrant(self, power: float, interest: float) -> PowerInterestQuadrant:
        """Determine power-interest quadrant."""
        high_power = power >= 0.6
        high_interest = interest >= 0.6

        if high_power and high_interest:
            return PowerInterestQuadrant.MANAGE_CLOSELY
        elif high_power and not high_interest:
            return PowerInterestQuadrant.KEEP_SATISFIED
        elif not high_power and high_interest:
            return PowerInterestQuadrant.KEEP_INFORMED
        else:
            return PowerInterestQuadrant.MONITOR

    def _map_to_influence_level(self, power_score: float) -> InfluenceLevel:
        """Map power score to influence level."""
        if power_score >= 0.85:
            return InfluenceLevel.VERY_HIGH
        elif power_score >= 0.65:
            return InfluenceLevel.HIGH
        elif power_score >= 0.45:
            return InfluenceLevel.MEDIUM
        elif power_score >= 0.25:
            return InfluenceLevel.LOW
        else:
            return InfluenceLevel.MINIMAL

    def _map_to_interest_level(self, interest_score: float) -> InterestLevel:
        """Map interest score to interest level."""
        if interest_score >= 0.85:
            return InterestLevel.VERY_HIGH
        elif interest_score >= 0.65:
            return InterestLevel.HIGH
        elif interest_score >= 0.45:
            return InterestLevel.MEDIUM
        elif interest_score >= 0.25:
            return InterestLevel.LOW
        else:
            return InterestLevel.MINIMAL

    def _generate_position_reasoning(
        self,
        stakeholder: Stakeholder,
        power: float,
        interest: float,
        quadrant: PowerInterestQuadrant,
    ) -> str:
        """Generate reasoning for stakeholder position."""
        return f"{stakeholder.name} ({stakeholder.role}) - Power: {power:.2f}, Interest: {interest:.2f}, Quadrant: {quadrant.value}"

    def _estimate_network_influence(self, stakeholder: Stakeholder) -> float:
        """Estimate stakeholder's influence on others."""
        # Simplified - could be expanded with relationship data
        score = 0.5

        if stakeholder.relationship_strength == "strong":
            score = 0.8
        elif stakeholder.relationship_strength == "collaborative":
            score = 0.7
        elif stakeholder.relationship_strength == "professional":
            score = 0.5

        # Adjust for role
        if stakeholder.role and any(title in stakeholder.role.lower() for title in ["vp", "director", "lead"]):
            score = min(1.0, score + 0.2)

        return score

    def _calculate_decision_authority(self, stakeholder: Stakeholder, decision_type: str) -> float:
        """Calculate decision authority for specific decision type."""
        if not stakeholder.authority_scope:
            return 0.3

        relevant_authority = {
            "technical": ["technical_decisions", "architecture_approval"],
            "strategic": ["strategic_decisions", "budget_approval"],
            "budget": ["budget_approval"],
            "hiring": ["hiring_approval"],
        }

        relevant = relevant_authority.get(decision_type, [])
        matches = sum(1 for auth in stakeholder.authority_scope if auth in relevant)

        return min(1.0, 0.3 + (matches * 0.2))

    def _assess_stakeholder_alignment(
        self,
        stakeholder: Stakeholder,
        options: List[str],
        historical: Optional[Dict[str, Any]],
    ) -> Tuple[AlignmentStatus, float]:
        """Assess stakeholder alignment with options."""
        # Simplified - could use historical patterns
        # Default to neutral with medium confidence
        return AlignmentStatus.NEUTRAL, 0.6

    def _identify_concerns(self, stakeholder: Stakeholder, options: List[str]) -> List[str]:
        """Identify stakeholder concerns."""
        concerns = []

        # Use decision factors as proxy for concerns
        for factor in stakeholder.decision_factors[:3]:  # Top 3 factors
            concerns.append(f"Impact on {factor}")

        return concerns

    def _identify_supporting_factors(self, stakeholder: Stakeholder, options: List[str]) -> List[str]:
        """Identify supporting factors."""
        return ["Aligns with expertise areas", "Supports team goals"]

    def _identify_resistance_factors(self, stakeholder: Stakeholder, options: List[str]) -> List[str]:
        """Identify resistance factors."""
        return []

    def _predict_position(self, stakeholder: Stakeholder, options: List[str]) -> str:
        """Predict stakeholder position."""
        return f"Likely to support if {stakeholder.decision_factors[0] if stakeholder.decision_factors else 'key concerns'} are addressed"

    def _calculate_consensus_likelihood(self, alignments: List[StakeholderAlignment]) -> float:
        """Calculate likelihood of reaching consensus."""
        if not alignments:
            return 0.0

        support_weight = 0.0
        total_weight = 0.0

        for alignment in alignments:
            weight = alignment.influence_on_others
            total_weight += weight

            if alignment.alignment_status in [AlignmentStatus.STRONG_SUPPORT, AlignmentStatus.SUPPORT]:
                support_weight += weight

        return support_weight / total_weight if total_weight > 0 else 0.5

    def _identify_conflicts(self, alignments: List[StakeholderAlignment]) -> List[str]:
        """Identify conflicts from alignments."""
        conflicts = []

        # Check for opposing positions
        supporters = [a for a in alignments if a.alignment_status in [AlignmentStatus.STRONG_SUPPORT, AlignmentStatus.SUPPORT]]
        opposers = [a for a in alignments if a.alignment_status == AlignmentStatus.OPPOSITION]

        if supporters and opposers:
            conflicts.append(f"Conflict between {len(supporters)} supporters and {len(opposers)} opposers")

        return conflicts

    def _identify_coalition_opportunities(self, alignments: List[StakeholderAlignment]) -> List[str]:
        """Identify coalition building opportunities."""
        opportunities = []

        high_influence_supporters = [
            a for a in alignments
            if a.alignment_status in [AlignmentStatus.STRONG_SUPPORT, AlignmentStatus.SUPPORT]
            and a.influence_on_others >= 0.7
        ]

        if high_influence_supporters:
            opportunities.append(f"Build coalition with {len(high_influence_supporters)} high-influence supporters")

        return opportunities

    def _generate_stakeholder_message(
        self,
        stakeholder: Stakeholder,
        decision: Dict[str, Any],
        templates: Optional[Dict[str, Any]],
    ) -> CommunicationMessage:
        """Generate communication message for stakeholder."""
        # Determine priority based on influence
        if stakeholder.influence_level in [InfluenceLevel.VERY_HIGH, InfluenceLevel.HIGH]:
            priority = CommunicationPriority.IMMEDIATE
        else:
            priority = CommunicationPriority.MEDIUM

        # Determine message type based on communication style
        message_type = "email"
        if stakeholder.communication_style == "technical_deep_dive":
            message_type = "technical_review_meeting"
        elif stakeholder.communication_style == "executive_summary":
            message_type = "executive_briefing"

        return CommunicationMessage(
            stakeholder_id=stakeholder.id,
            message_type=message_type,
            priority=priority,
            subject=f"Decision: {decision.get('title', 'Important Update')}",
            key_points=[
                f"Relevance to {', '.join(stakeholder.interest_areas[:2])}",
                "Impact assessment",
                "Next steps and timeline",
            ],
            tone=stakeholder.communication_style or "professional",
            timing="immediate" if priority == CommunicationPriority.IMMEDIATE else "this_week",
        )

    def _determine_communication_sequence(
        self,
        stakeholders: List[Stakeholder],
        messages: List[CommunicationMessage],
    ) -> List[str]:
        """Determine optimal communication sequence."""
        # Sort by influence level (high influence first)
        sorted_stakeholders = sorted(
            stakeholders,
            key=lambda s: (
                0 if s.influence_level == InfluenceLevel.VERY_HIGH else
                1 if s.influence_level == InfluenceLevel.HIGH else
                2
            )
        )

        return [s.id for s in sorted_stakeholders]

    def _generate_overall_strategy(
        self,
        stakeholders: List[Stakeholder],
        decision: Dict[str, Any],
    ) -> str:
        """Generate overall communication strategy."""
        high_influence = len([s for s in stakeholders if s.influence_level in [InfluenceLevel.VERY_HIGH, InfluenceLevel.HIGH]])

        return f"Engage {high_influence} high-influence stakeholders first to build coalition, then cascade to broader stakeholder base"

    def _generate_resistance_mitigation(self, stakeholders: List[Stakeholder]) -> List[str]:
        """Generate resistance mitigation strategies."""
        return [
            "Address key concerns proactively in initial communications",
            "Provide data to support decision rationale",
            "Offer channels for feedback and questions",
            "Schedule follow-up sessions for deep dives",
        ]
