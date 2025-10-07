"""
DecisionAnalyzer - Intelligent Decision Analysis and Framework Application Tool

Provides structured decision-making capabilities with framework application, option scoring,
stakeholder impact analysis, and template-based reporting.

Simplifies command implementation from 500+ lines to 15-20 lines:

    analyzer = DecisionAnalyzer()
    analysis = analyzer.apply_framework(
        decision_title="Technology Stack Selection",
        options=options_list,
        framework_type="technical"
    )
    print(analysis.formatted_output)
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Literal

from tools.config_manager import ConfigManager
from tools.stakeholder_analyzer import StakeholderAnalyzer
from tools.output_formatter import OutputFormatter


class DecisionAnalyzerError(Exception):
    """Base exception for DecisionAnalyzer errors."""
    pass


class UrgencyLevel(str, Enum):
    """Decision urgency levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SentimentType(str, Enum):
    """Stakeholder sentiment types."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@dataclass
class DecisionOption:
    """
    Represents a single decision option with scoring and analysis.

    Attributes:
        name: Option identifier/title
        description: Detailed option description
        pros: List of advantages
        cons: List of disadvantages
        criteria_scores: Dictionary of criterion_name -> score (0.0-1.0)
        estimated_cost: Cost estimate (as string, e.g., "$50,000")
        estimated_time: Time estimate (as string, e.g., "3 months")
        overall_score: Weighted overall score (0.0-1.0)
    """
    name: str
    description: str = ""
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    criteria_scores: Dict[str, float] = field(default_factory=dict)
    estimated_cost: Optional[str] = None
    estimated_time: Optional[str] = None
    overall_score: float = 0.0


@dataclass
class DecisionContext:
    """
    Decision metadata and constraints.

    Attributes:
        title: Decision title/identifier
        description: Detailed decision description
        urgency: Urgency level (critical, high, medium, low)
        deadline: Decision deadline (datetime or string)
        success_criteria: List of measurable success criteria
        constraints: Dictionary of constraint_name -> constraint_description
        decision_type: Type of decision (technical, business, strategic, etc.)
    """
    title: str
    description: str = ""
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    deadline: Optional[Any] = None
    success_criteria: List[str] = field(default_factory=list)
    constraints: Dict[str, str] = field(default_factory=dict)
    decision_type: str = "general"


@dataclass
class DecisionRecommendation:
    """
    Decision recommendation with reasoning.

    Attributes:
        option: Recommended option name
        reasoning: Detailed recommendation rationale
        confidence: Confidence score (0.0-1.0)
        implementation_notes: Implementation guidance
    """
    option: str
    reasoning: str
    confidence: float = 0.0
    implementation_notes: str = ""


@dataclass
class DecisionRisk:
    """
    Decision risk with mitigation strategy.

    Attributes:
        title: Risk identifier/title
        description: Detailed risk description
        severity: Risk severity (critical, high, medium, low)
        likelihood: Risk likelihood (high, medium, low)
        mitigation: Mitigation strategy description
    """
    title: str
    description: str
    severity: str = "medium"
    likelihood: str = "medium"
    mitigation: str = ""


@dataclass
class DecisionAnalysis:
    """
    Complete decision analysis results.

    Attributes:
        decision: Decision context and metadata
        options: List of analyzed options
        recommendation: Recommended option with reasoning
        stakeholder_impact: Dictionary of stakeholder -> impact analysis
        risks: List of identified risks
        next_steps: List of action items
        framework_applied: Framework name/type used
        analysis_metadata: Additional analysis metadata
        formatted_output: Formatted output string (if generated)
    """
    decision: DecisionContext
    options: List[DecisionOption]
    recommendation: DecisionRecommendation
    stakeholder_impact: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    risks: List[DecisionRisk] = field(default_factory=list)
    next_steps: List[Dict[str, Any]] = field(default_factory=list)
    framework_applied: str = "general"
    analysis_metadata: Dict[str, Any] = field(default_factory=dict)
    formatted_output: str = ""


class DecisionAnalyzer:
    """
    Intelligent decision analysis and framework application tool.

    Features:
    - Framework-based decision analysis with criterion scoring
    - Multi-criteria decision analysis (MCDA) algorithms
    - Stakeholder impact assessment integration
    - Risk identification and mitigation planning
    - Template-based output formatting

    Example:
        >>> analyzer = DecisionAnalyzer()
        >>> # Apply decision framework
        >>> analysis = analyzer.apply_framework(
        ...     decision_title="Technology Stack Selection",
        ...     options=[
        ...         {"name": "React", "description": "Modern JS framework"},
        ...         {"name": "Vue", "description": "Progressive framework"}
        ...     ],
        ...     framework_type="technical"
        ... )
        >>> print(analysis.formatted_output)
        >>>
        >>> # Analyze stakeholder impact
        >>> impact = analyzer.analyze_stakeholder_impact(
        ...     decision_title="API Redesign",
        ...     options=options_list,
        ...     stakeholders=["engineering", "product"]
        ... )
        >>>
        >>> # Compare options with custom criteria
        >>> comparison = analyzer.compare_options(
        ...     options=options_list,
        ...     criteria=[
        ...         {"name": "cost", "weight": 0.3},
        ...         {"name": "time", "weight": 0.4},
        ...         {"name": "quality", "weight": 0.3}
        ...     ]
        ... )
    """

    def __init__(self, config_root: Optional[Path] = None):
        """
        Initialize DecisionAnalyzer.

        Args:
            config_root: Root directory for configuration files
        """
        self.config_root = config_root or Path.cwd() / ".claude"
        self.config_manager = ConfigManager(config_root=self.config_root)
        self.stakeholder_analyzer = StakeholderAnalyzer(config_root=self.config_root)
        self.output_formatter = OutputFormatter()

    def apply_framework(
        self,
        decision_title: str,
        options: List[Dict[str, Any]],
        framework_type: str = "general",
        description: str = "",
        urgency: str = "medium",
        deadline: Optional[Any] = None,
        output_format: str = "markdown",
    ) -> DecisionAnalysis:
        """
        Apply decision framework to analyze options and generate recommendation.

        Args:
            decision_title: Decision title/identifier
            options: List of option dictionaries (name, description, pros, cons)
            framework_type: Framework type (technical, business, strategic, etc.)
            description: Detailed decision description
            urgency: Urgency level (critical, high, medium, low)
            deadline: Decision deadline
            output_format: Output format (markdown or json)

        Returns:
            DecisionAnalysis with complete analysis and recommendation

        Raises:
            DecisionAnalyzerError: If framework application fails

        Example:
            >>> analysis = analyzer.apply_framework(
            ...     decision_title="Database Selection",
            ...     options=[
            ...         {"name": "PostgreSQL", "description": "Relational DB"},
            ...         {"name": "MongoDB", "description": "Document DB"}
            ...     ],
            ...     framework_type="technical"
            ... )
        """
        try:
            # Create decision context
            decision = DecisionContext(
                title=decision_title,
                description=description,
                urgency=UrgencyLevel(urgency.lower()),
                deadline=deadline,
                decision_type=framework_type
            )

            # Load framework configuration
            framework = self._load_framework(framework_type)

            # Score options using framework criteria
            scored_options = self._score_options(options, framework)

            # Generate recommendation
            recommendation = self._generate_recommendation(scored_options, framework)

            # Identify risks
            risks = self._identify_risks(scored_options, framework)

            # Generate next steps
            next_steps = self._generate_next_steps(recommendation, framework)

            # Create analysis result
            analysis = DecisionAnalysis(
                decision=decision,
                options=scored_options,
                recommendation=recommendation,
                risks=risks,
                next_steps=next_steps,
                framework_applied=framework.get("name", framework_type),
                analysis_metadata={
                    "framework_type": framework_type,
                    "options_analyzed": len(scored_options),
                    "analysis_date": datetime.now().isoformat()
                }
            )

            # Format output
            if output_format == "markdown":
                analysis.formatted_output = self._format_analysis(analysis)

            return analysis

        except Exception as e:
            raise DecisionAnalyzerError(
                f"Failed to apply framework to decision '{decision_title}': {str(e)}"
            ) from e

    def analyze_stakeholder_impact(
        self,
        decision_title: str,
        options: List[Dict[str, Any]],
        stakeholders: Optional[List[str]] = None,
        decision_type: str = "general",
    ) -> Dict[str, Any]:
        """
        Analyze stakeholder impact for decision options.

        Args:
            decision_title: Decision title/identifier
            options: List of option dictionaries
            stakeholders: Optional list of stakeholder identifiers
            decision_type: Type of decision for stakeholder identification

        Returns:
            Dictionary with stakeholder impact analysis

        Example:
            >>> impact = analyzer.analyze_stakeholder_impact(
            ...     decision_title="API Redesign",
            ...     options=[{"name": "REST"}, {"name": "GraphQL"}],
            ...     stakeholders=["engineering", "product"]
            ... )
        """
        try:
            # Identify stakeholders if not provided
            if not stakeholders:
                context = {
                    "decision_type": decision_type,
                    "decision_title": decision_title
                }
                identified = self.stakeholder_analyzer.identify_stakeholders(context)
                stakeholders = [s.get("id", s.get("name")) for s in identified]

            # Analyze impact for each stakeholder
            impact_analysis = {}
            for stakeholder in stakeholders:
                impact_analysis[stakeholder] = {
                    "description": f"Impact of {decision_title} on {stakeholder}",
                    "sentiment": self._assess_stakeholder_sentiment(
                        stakeholder, options, decision_type
                    ),
                    "concerns": self._identify_stakeholder_concerns(
                        stakeholder, options
                    ),
                    "communication_priority": "high" if decision_type == "strategic" else "medium"
                }

            return impact_analysis

        except Exception as e:
            # Graceful degradation
            return {
                stakeholder: {
                    "description": f"Impact assessment for {stakeholder}",
                    "sentiment": "neutral",
                    "concerns": [],
                    "communication_priority": "medium"
                }
                for stakeholder in (stakeholders or [])
            }

    def compare_options(
        self,
        options: List[Dict[str, Any]],
        criteria: List[Dict[str, float]],
    ) -> Dict[str, Any]:
        """
        Compare options using multi-criteria decision analysis (MCDA).

        Args:
            options: List of option dictionaries
            criteria: List of criterion dictionaries (name, weight)

        Returns:
            Dictionary with comparison matrix and scores

        Example:
            >>> comparison = analyzer.compare_options(
            ...     options=[{"name": "Option A"}, {"name": "Option B"}],
            ...     criteria=[
            ...         {"name": "cost", "weight": 0.4},
            ...         {"name": "time", "weight": 0.6}
            ...     ]
            ... )
        """
        # Normalize weights
        total_weight = sum(c.get("weight", 0) for c in criteria)
        if total_weight == 0:
            total_weight = 1.0

        normalized_criteria = [
            {**c, "weight": c.get("weight", 0) / total_weight}
            for c in criteria
        ]

        # Build comparison matrix
        comparison_matrix = []
        for option in options:
            option_name = option.get("name", "Unknown")
            option_scores = {}
            total_score = 0.0

            for criterion in normalized_criteria:
                criterion_name = criterion.get("name", "criterion")
                weight = criterion.get("weight", 0)

                # Get criterion score (0.0-1.0) from option or use default
                score = option.get(f"{criterion_name}_score", 0.5)
                option_scores[criterion_name] = score
                total_score += score * weight

            comparison_matrix.append({
                "option": option_name,
                "scores": option_scores,
                "weighted_score": total_score
            })

        # Sort by weighted score
        comparison_matrix.sort(key=lambda x: x["weighted_score"], reverse=True)

        return {
            "criteria": normalized_criteria,
            "comparison_matrix": comparison_matrix,
            "recommended": comparison_matrix[0]["option"] if comparison_matrix else None
        }

    def generate_decision_report(
        self,
        analysis: DecisionAnalysis,
        template: str = "decision_analysis",
        include_stakeholders: bool = True,
    ) -> str:
        """
        Generate formatted decision report from analysis.

        Args:
            analysis: DecisionAnalysis object
            template: Template name to use
            include_stakeholders: Whether to include stakeholder impact

        Returns:
            Formatted decision report string
        """
        # Prepare data for template
        template_data = {
            "decision": {
                "title": analysis.decision.title,
                "description": analysis.decision.description,
                "urgency": analysis.decision.urgency.value,
                "deadline": analysis.decision.deadline
            },
            "options": [
                {
                    "name": opt.name,
                    "description": opt.description,
                    "score": opt.overall_score,
                    "pros": opt.pros,
                    "cons": opt.cons,
                    "criteria_scores": opt.criteria_scores,
                    "estimated_cost": opt.estimated_cost,
                    "estimated_time": opt.estimated_time
                }
                for opt in analysis.options
            ],
            "recommendation": {
                "option": analysis.recommendation.option,
                "reasoning": analysis.recommendation.reasoning,
                "confidence": analysis.recommendation.confidence
            },
            "risks": [
                {
                    "title": risk.title,
                    "description": risk.description,
                    "severity": risk.severity,
                    "likelihood": risk.likelihood,
                    "mitigation": risk.mitigation
                }
                for risk in analysis.risks
            ],
            "next_steps": analysis.next_steps
        }

        if include_stakeholders:
            template_data["stakeholder_impact"] = analysis.stakeholder_impact

        # Format with OutputFormatter
        result = self.output_formatter.format_markdown(
            data=template_data,
            template=template
        )

        return result.content

    # Private helper methods

    def _load_framework(self, framework_type: str) -> Dict[str, Any]:
        """Load decision framework configuration."""
        # Default framework if configuration not available
        default_framework = {
            "name": framework_type.title(),
            "criteria": [
                {"name": "strategic_impact", "weight": 0.3, "description": "Strategic alignment"},
                {"name": "cost_efficiency", "weight": 0.3, "description": "Cost effectiveness"},
                {"name": "implementation_risk", "weight": 0.2, "description": "Implementation risk"},
                {"name": "timeline", "weight": 0.2, "description": "Timeline feasibility"}
            ]
        }

        try:
            # Try to load from configuration
            frameworks_config = self.config_manager.load_config("decision_frameworks.yaml")
            framework_key = f"{framework_type}_decision"

            if framework_key in frameworks_config.get("frameworks", {}):
                return frameworks_config["frameworks"][framework_key]

        except Exception:
            # Use default framework if configuration unavailable
            pass

        return default_framework

    def _score_options(
        self,
        options: List[Dict[str, Any]],
        framework: Dict[str, Any]
    ) -> List[DecisionOption]:
        """Score options using framework criteria."""
        scored_options = []
        criteria = framework.get("criteria", [])

        for option_dict in options:
            # Create DecisionOption
            option = DecisionOption(
                name=option_dict.get("name", "Unknown"),
                description=option_dict.get("description", ""),
                pros=option_dict.get("pros", []),
                cons=option_dict.get("cons", []),
                estimated_cost=option_dict.get("estimated_cost"),
                estimated_time=option_dict.get("estimated_time")
            )

            # Calculate criterion scores
            for criterion in criteria:
                criterion_name = criterion.get("name", "criterion")
                weight = criterion.get("weight", 0)

                # Get score from option dict or calculate default
                score = option_dict.get(f"{criterion_name}_score", 0.5)
                option.criteria_scores[criterion_name] = score

            # Calculate weighted overall score
            total_weight = sum(c.get("weight", 0) for c in criteria) or 1.0
            option.overall_score = sum(
                option.criteria_scores.get(c.get("name", ""), 0.5) * c.get("weight", 0)
                for c in criteria
            ) / total_weight

            scored_options.append(option)

        # Sort by overall score
        scored_options.sort(key=lambda x: x.overall_score, reverse=True)

        return scored_options

    def _generate_recommendation(
        self,
        options: List[DecisionOption],
        framework: Dict[str, Any]
    ) -> DecisionRecommendation:
        """Generate recommendation based on scored options."""
        if not options:
            return DecisionRecommendation(
                option="None",
                reasoning="No options available",
                confidence=0.0
            )

        # Recommend highest scoring option
        best_option = options[0]

        # Calculate confidence based on score gap
        confidence = best_option.overall_score
        if len(options) > 1:
            score_gap = best_option.overall_score - options[1].overall_score
            confidence = min(1.0, confidence + score_gap * 0.5)

        # Generate reasoning
        reasoning = f"Based on {framework.get('name', 'framework')} analysis, "
        reasoning += f"{best_option.name} scores highest ({best_option.overall_score:.2f}) "
        reasoning += f"across evaluation criteria. "

        if best_option.pros:
            reasoning += f"Key strengths: {', '.join(best_option.pros[:2])}. "

        return DecisionRecommendation(
            option=best_option.name,
            reasoning=reasoning,
            confidence=confidence
        )

    def _identify_risks(
        self,
        options: List[DecisionOption],
        framework: Dict[str, Any]
    ) -> List[DecisionRisk]:
        """Identify risks from option analysis."""
        risks = []

        # Check for low-scoring options (potential regret)
        for option in options:
            if option.overall_score < 0.5:
                risks.append(DecisionRisk(
                    title=f"Low viability of {option.name}",
                    description=f"{option.name} scores below threshold ({option.overall_score:.2f})",
                    severity="medium",
                    likelihood="medium",
                    mitigation="Further analysis or elimination from consideration"
                ))

        # Check for cons in recommended option
        if options and options[0].cons:
            for con in options[0].cons[:2]:  # Top 2 cons
                risks.append(DecisionRisk(
                    title=f"Concern with recommended option",
                    description=con,
                    severity="medium",
                    likelihood="medium",
                    mitigation="Plan mitigation strategy during implementation"
                ))

        return risks

    def _generate_next_steps(
        self,
        recommendation: DecisionRecommendation,
        framework: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate next steps based on recommendation."""
        return [
            {
                "action": f"Review and approve {recommendation.option} recommendation",
                "owner": "Decision Maker",
                "deadline": "Within 1 week"
            },
            {
                "action": "Develop detailed implementation plan",
                "owner": "Project Team",
                "deadline": "Within 2 weeks"
            },
            {
                "action": "Communicate decision to stakeholders",
                "owner": "Communication Lead",
                "deadline": "Within 3 days"
            }
        ]

    def _format_analysis(self, analysis: DecisionAnalysis) -> str:
        """Format analysis using OutputFormatter."""
        return self.generate_decision_report(
            analysis=analysis,
            template="decision_analysis",
            include_stakeholders=bool(analysis.stakeholder_impact)
        )

    def _assess_stakeholder_sentiment(
        self,
        stakeholder: str,
        options: List[Dict[str, Any]],
        decision_type: str
    ) -> str:
        """Assess stakeholder sentiment (simplified heuristic)."""
        # Simple heuristic based on decision type
        if decision_type == "technical" and "engineering" in stakeholder.lower():
            return "positive"
        elif decision_type == "strategic" and "executive" in stakeholder.lower():
            return "positive"
        else:
            return "neutral"

    def _identify_stakeholder_concerns(
        self,
        stakeholder: str,
        options: List[Dict[str, Any]]
    ) -> List[str]:
        """Identify stakeholder concerns (simplified)."""
        concerns = []

        # Extract cons from all options as potential concerns
        for option in options:
            cons = option.get("cons", [])
            concerns.extend(cons[:1])  # Take first con from each option

        return concerns[:3]  # Limit to 3 concerns
