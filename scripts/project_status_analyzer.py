#!/usr/bin/env python3
"""
Intelligent Project Status Analyzer
Supporting script for /project status command with health scoring, trend analysis, and insights generation.
"""

import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Import ConfigManager for YAML configuration management
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools import ConfigManager
from tools.schemas import ProjectsConfig

try:
    from project_data_collector import ProjectData, ProjectDataCollector

    DATA_COLLECTOR_AVAILABLE = True
except ImportError:
    DATA_COLLECTOR_AVAILABLE = False
    print("Warning: ProjectDataCollector not available")


@dataclass
class HealthMetrics:
    """Project health metrics"""

    timeline_progress: float  # 0.0-1.0
    activity_level: float  # 0.0-1.0
    blocker_impact: float  # 0.0-1.0 (inverted, 1.0 = no blockers)
    dependency_health: float  # 0.0-1.0
    overall_score: float  # 0.0-1.0
    category: str  # excellent, good, at_risk, critical


@dataclass
class TrendAnalysis:
    """Project trend analysis"""

    velocity: str  # increasing, stable, decreasing
    risk_level: str  # low, medium, high
    activity_trend: str  # increasing, stable, decreasing
    confidence: float  # 0.0-1.0


@dataclass
class ProjectInsight:
    """Individual project insight"""

    project_name: str
    health_metrics: HealthMetrics
    trends: TrendAnalysis
    blockers: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    recent_activity: Dict[str, Any]


@dataclass
class PortfolioAnalysis:
    """Portfolio-wide analysis"""

    total_projects: int
    health_distribution: Dict[str, int]
    portfolio_health_score: float
    critical_actions_needed: int
    portfolio_trends: Dict[str, str]
    strategic_recommendations: Dict[str, List[str]]
    insights: List[str]


class ProjectStatusAnalyzer:
    """
    Intelligent project status analyzer that provides health scoring,
    trend analysis, and actionable insights for project management.
    """

    def __init__(self, config_dir: str = ".claude"):
        self.config_dir = Path(config_dir)

        # Initialize ConfigManager for YAML configuration management
        self.config_manager = ConfigManager(config_root=Path(config_dir))

        # Load projects configuration with schema validation and caching
        self.projects_config = self.config_manager.load_config(
            "projects.yaml", schema=ProjectsConfig
        )

        # Initialize data collector if available
        if DATA_COLLECTOR_AVAILABLE:
            self.data_collector = ProjectDataCollector(config_dir)
        else:
            self.data_collector = None

        # Health scoring weights
        self.health_weights = {
            "timeline_progress": 0.30,
            "activity_level": 0.25,
            "blocker_impact": 0.25,
            "dependency_health": 0.20,
        }

    def _calculate_timeline_progress(
        self, project_config: Dict[str, Any], project_data: Optional[ProjectData] = None
    ) -> float:
        """Calculate timeline progress score (0.0-1.0)"""
        try:
            # Get milestone information
            milestones = project_config.get("milestones", [])
            if not milestones:
                return 0.5  # Default for projects without milestones

            completed_milestones = sum(1 for m in milestones if m.get("status") == "completed")
            total_milestones = len(milestones)
            milestone_progress = (
                completed_milestones / total_milestones if total_milestones > 0 else 0
            )

            # Calculate time progress
            start_date = datetime.fromisoformat(
                project_config.get("start_date", datetime.now().isoformat()[:10])
            )
            target_date = datetime.fromisoformat(
                project_config.get(
                    "target_date", (datetime.now() + timedelta(days=90)).isoformat()[:10]
                )
            )
            current_date = datetime.now()

            total_duration = (target_date - start_date).days
            elapsed_days = (current_date - start_date).days
            time_progress = elapsed_days / total_duration if total_duration > 0 else 0

            # Timeline health: ideally milestone_progress >= time_progress
            if time_progress <= 0:
                return 1.0
            elif time_progress >= 1.0:
                return milestone_progress * 0.5  # Penalize overdue projects
            else:
                # Score based on whether milestones are ahead/on track/behind schedule
                ratio = milestone_progress / time_progress
                return min(1.0, max(0.0, ratio))

        except Exception as e:
            print(f"Warning: Error calculating timeline progress: {e}")
            return 0.5

    def _calculate_activity_level(self, project_data: Optional[ProjectData] = None) -> float:
        """Calculate activity level score based on recent GitHub/notes activity"""
        if not project_data:
            return 0.5  # Default when no data available

        activity_score = 0.0
        activity_count = 0

        try:
            # GitHub activity (last 7 days)
            if project_data.github_data:
                recent_commits = len(
                    [
                        c
                        for c in project_data.github_data.commits
                        if datetime.fromisoformat(c["date"].replace("Z", "+00:00"))
                        > datetime.now() - timedelta(days=7)
                    ]
                )
                recent_prs = len(
                    [
                        pr
                        for pr in project_data.github_data.pull_requests
                        if datetime.fromisoformat(pr["updated_at"].replace("Z", "+00:00"))
                        > datetime.now() - timedelta(days=7)
                    ]
                )
                recent_issues = len(
                    [
                        issue
                        for issue in project_data.github_data.issues
                        if datetime.fromisoformat(issue["updated_at"].replace("Z", "+00:00"))
                        > datetime.now() - timedelta(days=7)
                    ]
                )

                github_activity = recent_commits + recent_prs + recent_issues
                activity_score += min(1.0, github_activity / 10.0)  # Normalize to 0-1
                activity_count += 1

            # Notes activity
            if project_data.notes_data:
                notes_count = len(project_data.notes_data.project_notes)
                actions_count = len(project_data.notes_data.action_items)

                notes_activity = (notes_count + actions_count) / 10.0
                activity_score += min(1.0, notes_activity)
                activity_count += 1

            return activity_score / activity_count if activity_count > 0 else 0.5

        except Exception as e:
            print(f"Warning: Error calculating activity level: {e}")
            return 0.5

    def _identify_blockers(
        self, project_config: Dict[str, Any], project_data: Optional[ProjectData] = None
    ) -> Tuple[List[Dict[str, Any]], float]:
        """Identify blockers and calculate blocker impact score"""
        blockers = []
        blocker_impact_score = 1.0  # Start with perfect score, reduce for each blocker

        try:
            # Check for dependency blockers
            dependencies = project_config.get("dependencies", [])
            for dep in dependencies:
                dep_config = self.projects_config.get("projects", {}).get(dep)
                if dep_config:
                    dep_status = dep_config.get("status", "unknown")
                    if dep_status in ["blocked", "on_hold", "cancelled"]:
                        blockers.append(
                            {
                                "type": "dependency",
                                "description": f'Dependency "{dep}" is {dep_status}',
                                "severity": "high",
                                "source": "project_config",
                            }
                        )
                        blocker_impact_score -= 0.3

            # Check for overdue milestones
            milestones = project_config.get("milestones", [])
            current_date = datetime.now()
            for milestone in milestones:
                if milestone.get("status") != "completed":
                    milestone_date = datetime.fromisoformat(milestone.get("date", "2024-12-31"))
                    if milestone_date < current_date:
                        days_overdue = (current_date - milestone_date).days
                        blockers.append(
                            {
                                "type": "overdue_milestone",
                                "description": f'Milestone "{milestone.get("name")}" is {days_overdue} days overdue',
                                "severity": "medium" if days_overdue < 7 else "high",
                                "days_overdue": days_overdue,
                                "source": "milestones",
                            }
                        )
                        blocker_impact_score -= 0.2 if days_overdue < 7 else 0.4

            # Check GitHub data for issues/blockers
            if project_data and project_data.github_data:
                high_priority_issues = len(
                    [
                        issue
                        for issue in project_data.github_data.issues
                        if issue["state"] == "open"
                        and any(
                            label.lower() in ["bug", "critical", "blocker", "urgent"]
                            for label in issue.get("labels", [])
                        )
                    ]
                )
                if high_priority_issues > 0:
                    blockers.append(
                        {
                            "type": "critical_issues",
                            "description": f"{high_priority_issues} critical/urgent GitHub issues open",
                            "severity": "medium",
                            "count": high_priority_issues,
                            "source": "github",
                        }
                    )
                    blocker_impact_score -= min(0.3, high_priority_issues * 0.1)

                # Check for stale repositories (no commits in 7+ days for active projects)
                if project_config.get("status") in ["active", "in_progress"]:
                    if project_data.github_data.commits:
                        latest_commit_date = max(
                            [
                                datetime.fromisoformat(c["date"].replace("Z", "+00:00"))
                                for c in project_data.github_data.commits
                            ]
                        )
                        days_since_commit = (datetime.now() - latest_commit_date).days
                        if days_since_commit > 7:
                            blockers.append(
                                {
                                    "type": "stale_activity",
                                    "description": f"No GitHub commits in {days_since_commit} days",
                                    "severity": "medium",
                                    "days_stale": days_since_commit,
                                    "source": "github",
                                }
                            )
                            blocker_impact_score -= 0.2

            return blockers, max(0.0, blocker_impact_score)

        except Exception as e:
            print(f"Warning: Error identifying blockers: {e}")
            return [], 0.5

    def _calculate_dependency_health(self, project_config: Dict[str, Any]) -> float:
        """Calculate health score based on dependency status"""
        try:
            dependencies = project_config.get("dependencies", [])
            if not dependencies:
                return 1.0  # Perfect score if no dependencies

            dependency_scores = []
            for dep in dependencies:
                dep_config = self.projects_config.get("projects", {}).get(dep)
                if dep_config:
                    dep_status = dep_config.get("status", "unknown")
                    # Score based on dependency status
                    if dep_status == "completed":
                        dependency_scores.append(1.0)
                    elif dep_status in ["active", "in_progress"]:
                        dependency_scores.append(0.7)
                    elif dep_status == "planning":
                        dependency_scores.append(0.5)
                    elif dep_status in ["blocked", "on_hold"]:
                        dependency_scores.append(0.2)
                    else:
                        dependency_scores.append(0.3)
                else:
                    # External dependency not in config
                    dependency_scores.append(0.5)

            return sum(dependency_scores) / len(dependency_scores) if dependency_scores else 1.0

        except Exception as e:
            print(f"Warning: Error calculating dependency health: {e}")
            return 0.5

    def _calculate_health_metrics(
        self, project_config: Dict[str, Any], project_data: Optional[ProjectData] = None
    ) -> HealthMetrics:
        """Calculate comprehensive health metrics for a project"""
        timeline_progress = self._calculate_timeline_progress(project_config, project_data)
        activity_level = self._calculate_activity_level(project_data)
        blockers, blocker_impact = self._identify_blockers(project_config, project_data)
        dependency_health = self._calculate_dependency_health(project_config)

        # Calculate weighted overall score
        overall_score = (
            timeline_progress * self.health_weights["timeline_progress"]
            + activity_level * self.health_weights["activity_level"]
            + blocker_impact * self.health_weights["blocker_impact"]
            + dependency_health * self.health_weights["dependency_health"]
        )

        # Determine category
        if overall_score >= 0.8:
            category = "excellent"
        elif overall_score >= 0.6:
            category = "good"
        elif overall_score >= 0.4:
            category = "at_risk"
        else:
            category = "critical"

        return HealthMetrics(
            timeline_progress=timeline_progress,
            activity_level=activity_level,
            blocker_impact=blocker_impact,
            dependency_health=dependency_health,
            overall_score=overall_score,
            category=category,
        )

    def _analyze_trends(
        self, project_config: Dict[str, Any], project_data: Optional[ProjectData] = None
    ) -> TrendAnalysis:
        """Analyze project trends"""
        # For now, simplified trend analysis based on available data
        velocity = "stable"
        activity_trend = "stable"
        risk_level = "medium"
        confidence = 0.7

        try:
            if project_data and project_data.github_data:
                # Simple activity trend based on recent commits
                recent_commits = len(
                    [
                        c
                        for c in project_data.github_data.commits
                        if datetime.fromisoformat(c["date"].replace("Z", "+00:00"))
                        > datetime.now() - timedelta(days=7)
                    ]
                )

                if recent_commits > 5:
                    activity_trend = "increasing"
                    velocity = "increasing"
                elif recent_commits < 2:
                    activity_trend = "decreasing"
                    velocity = "decreasing"

            # Risk level based on project status and blockers
            project_status = project_config.get("status", "unknown")
            if project_status in ["blocked", "on_hold"]:
                risk_level = "high"
            elif project_status in ["active", "in_progress"]:
                risk_level = "low"

        except Exception as e:
            print(f"Warning: Error analyzing trends: {e}")

        return TrendAnalysis(
            velocity=velocity,
            risk_level=risk_level,
            activity_trend=activity_trend,
            confidence=confidence,
        )

    def _generate_recommendations(
        self,
        project_name: str,
        project_config: Dict[str, Any],
        health_metrics: HealthMetrics,
        blockers: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        recommendations = []

        try:
            # High priority blockers
            for blocker in blockers:
                if blocker.get("severity") == "high":
                    if blocker["type"] == "dependency":
                        recommendations.append(
                            {
                                "priority": "high",
                                "action": f"Resolve dependency blocker: {blocker['description']}",
                                "impact": "Unblocks project progression",
                                "category": "blocker_resolution",
                            }
                        )
                    elif blocker["type"] == "overdue_milestone":
                        recommendations.append(
                            {
                                "priority": "high",
                                "action": f"Address overdue milestone: {blocker['description']}",
                                "impact": "Gets project back on schedule",
                                "category": "timeline_recovery",
                            }
                        )

            # Health-based recommendations
            if health_metrics.overall_score < 0.4:
                recommendations.append(
                    {
                        "priority": "high",
                        "action": f"Conduct project health review for {project_name}",
                        "impact": "Identifies root causes of project issues",
                        "category": "health_intervention",
                    }
                )

            if health_metrics.activity_level < 0.3:
                recommendations.append(
                    {
                        "priority": "medium",
                        "action": "Increase development activity and team engagement",
                        "impact": "Improves project momentum",
                        "category": "activity_boost",
                    }
                )

            if health_metrics.timeline_progress < 0.3:
                recommendations.append(
                    {
                        "priority": "medium",
                        "action": "Review and adjust project timeline and milestones",
                        "impact": "Realigns expectations with reality",
                        "category": "timeline_adjustment",
                    }
                )

        except Exception as e:
            print(f"Warning: Error generating recommendations: {e}")

        return recommendations

    def analyze_project(self, project_name: str) -> Optional[ProjectInsight]:
        """Analyze a single project"""
        project_config = self.projects_config.get("projects", {}).get(project_name)
        if not project_config:
            return None

        # Collect data if available
        project_data = None
        if self.data_collector:
            try:
                project_data = self.data_collector.collect_project_data(project_name)
            except Exception as e:
                print(f"Warning: Could not collect data for {project_name}: {e}")

        # Calculate metrics
        health_metrics = self._calculate_health_metrics(project_config, project_data)
        trends = self._analyze_trends(project_config, project_data)
        blockers, _ = self._identify_blockers(project_config, project_data)
        recommendations = self._generate_recommendations(
            project_name, project_config, health_metrics, blockers
        )

        # Summarize recent activity
        recent_activity = {"github": {}, "notes": {}}
        if project_data:
            if project_data.github_data:
                recent_activity["github"] = {
                    "commits_last_week": len(
                        [
                            c
                            for c in project_data.github_data.commits
                            if datetime.fromisoformat(c["date"].replace("Z", "+00:00"))
                            > datetime.now() - timedelta(days=7)
                        ]
                    ),
                    "prs_last_week": len(
                        [
                            pr
                            for pr in project_data.github_data.pull_requests
                            if datetime.fromisoformat(pr["updated_at"].replace("Z", "+00:00"))
                            > datetime.now() - timedelta(days=7)
                        ]
                    ),
                    "open_issues": len(
                        [
                            issue
                            for issue in project_data.github_data.issues
                            if issue["state"] == "open"
                        ]
                    ),
                }
            if project_data.notes_data:
                recent_activity["notes"] = {
                    "recent_notes": len(project_data.notes_data.project_notes),
                    "action_items_open": len(
                        [
                            a
                            for a in project_data.notes_data.action_items
                            if a.get("status") != "completed"
                        ]
                    ),
                }

        return ProjectInsight(
            project_name=project_name,
            health_metrics=health_metrics,
            trends=trends,
            blockers=blockers,
            recommendations=recommendations,
            recent_activity=recent_activity,
        )

    def analyze_portfolio(self, project_names: Optional[List[str]] = None) -> PortfolioAnalysis:
        """Analyze entire project portfolio"""
        if project_names is None:
            project_names = list(self.projects_config.get("projects", {}).keys())

        project_insights = []
        for project_name in project_names:
            insight = self.analyze_project(project_name)
            if insight:
                project_insights.append(insight)

        # Calculate portfolio metrics
        health_distribution = {"excellent": 0, "good": 0, "at_risk": 0, "critical": 0}
        total_health_score = 0
        critical_actions = 0

        for insight in project_insights:
            health_distribution[insight.health_metrics.category] += 1
            total_health_score += insight.health_metrics.overall_score
            if insight.health_metrics.category in ["critical", "at_risk"]:
                critical_actions += len(insight.blockers)

        portfolio_health_score = (
            total_health_score / len(project_insights) if project_insights else 0
        )

        # Generate strategic recommendations
        strategic_recommendations = {"immediate": [], "short_term": [], "long_term": []}

        # Immediate actions for critical projects
        for insight in project_insights:
            if insight.health_metrics.category == "critical":
                for rec in insight.recommendations:
                    if rec["priority"] == "high":
                        strategic_recommendations["immediate"].append(rec["action"])

        # Portfolio-level insights
        insights = []
        if health_distribution["critical"] > 0:
            insights.append(
                f"{health_distribution['critical']} projects in critical state requiring immediate intervention"
            )

        if portfolio_health_score < 0.5:
            insights.append("Portfolio health is below average, consider resource reallocation")

        active_projects = sum(health_distribution.values())
        if active_projects > 5:
            insights.append("High number of active projects may be diluting focus and resources")

        return PortfolioAnalysis(
            total_projects=len(project_insights),
            health_distribution=health_distribution,
            portfolio_health_score=portfolio_health_score,
            critical_actions_needed=critical_actions,
            portfolio_trends={"velocity_trend": "stable", "risk_trend": "stable"},
            strategic_recommendations=strategic_recommendations,
            insights=insights,
        )


def main():
    """CLI interface for project status analysis"""
    import argparse
    import contextlib
    import io

    parser = argparse.ArgumentParser(description="Intelligent Project Status Analyzer")
    parser.add_argument("--project", type=str, help="Analyze specific project")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument(
        "--focus", type=str, choices=["health", "risks", "trends"], help="Focus analysis area"
    )

    args = parser.parse_args()

    analyzer = ProjectStatusAnalyzer()

    try:
        # For JSON output, suppress warnings from data collector
        if args.json:
            # Capture stdout during analysis to suppress warnings
            captured_output = io.StringIO()
            with contextlib.redirect_stdout(captured_output):
                if args.project:
                    insight = analyzer.analyze_project(args.project)
                    if insight:
                        result = asdict(insight)
                    else:
                        print(f"Error: Project '{args.project}' not found", file=sys.stderr)
                        return 1
                else:
                    portfolio = analyzer.analyze_portfolio()
                    result = asdict(portfolio)

            # Print clean JSON to stdout
            print(json.dumps(result, indent=2, default=str))

        else:
            # Normal output with warnings visible
            if args.project:
                insight = analyzer.analyze_project(args.project)
                if insight:
                    print(f"Project: {insight.project_name}")
                    print(
                        f"Health Score: {insight.health_metrics.overall_score:.2f} ({insight.health_metrics.category})"
                    )
                    print(f"Blockers: {len(insight.blockers)}")
                    print(f"Recommendations: {len(insight.recommendations)}")
                else:
                    print(f"Project '{args.project}' not found")
                    return 1
            else:
                portfolio = analyzer.analyze_portfolio()
                print(f"Portfolio Health: {portfolio.portfolio_health_score:.2f}")
                print(f"Total Projects: {portfolio.total_projects}")
                print(f"Health Distribution: {portfolio.health_distribution}")
                print(f"Critical Actions Needed: {portfolio.critical_actions_needed}")

    except Exception as e:
        if args.json:
            print(f'{{"error": "{str(e)}"}}')
        else:
            print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
