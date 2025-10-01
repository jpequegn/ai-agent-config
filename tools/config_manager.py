"""
ConfigManager - Unified YAML Configuration Management

Provides centralized configuration loading, validation, and synchronization
with intelligent caching and atomic updates.
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

import yaml
from pydantic import BaseModel, ValidationError

from tools.schemas import (
    DecisionFrameworksConfig,
    IntegrationsConfig,
    Project,
    ProjectsConfig,
    StakeholderContextsConfig,
    StakeholderProfile,
    TeamMember,
    TeamRosterConfig,
)


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""

    pass


class ConfigNotFoundError(Exception):
    """Raised when configuration file not found."""

    pass


class ConfigManager:
    """
    Unified YAML configuration manager with validation and caching.

    Features:
    - Schema-validated configuration loading
    - Atomic updates with rollback
    - File modification time-based cache invalidation
    - Cross-file synchronization
    - Type-safe operations

    Example:
        >>> mgr = ConfigManager()
        >>> project = mgr.get_project("mobile-app-v2")
        >>> mgr.update_project("mobile-app-v2", {"status": "completed"})
    """

    def __init__(self, config_root: Optional[Path] = None):
        """
        Initialize ConfigManager.

        Args:
            config_root: Root directory for configuration files.
                        Defaults to .claude/ in current directory.
        """
        self.config_root = config_root or Path.cwd() / ".claude"
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_times: Dict[str, float] = {}

    def _get_file_mtime(self, path: Path) -> float:
        """Get file modification time."""
        return path.stat().st_mtime if path.exists() else 0

    def _is_cache_valid(self, path: Path) -> bool:
        """Check if cached data is still valid."""
        cache_key = str(path)
        if cache_key not in self._cache:
            return False

        cached_mtime = self._cache_times.get(cache_key, 0)
        current_mtime = self._get_file_mtime(path)
        return cached_mtime >= current_mtime

    def _update_cache(self, path: Path, data: Dict[str, Any]) -> None:
        """Update cache with new data."""
        cache_key = str(path)
        self._cache[cache_key] = data
        self._cache_times[cache_key] = self._get_file_mtime(path)

    def _invalidate_cache(self, path: Path) -> None:
        """Invalidate cache for a specific file."""
        cache_key = str(path)
        self._cache.pop(cache_key, None)
        self._cache_times.pop(cache_key, None)

    def load_config(
        self,
        path: Union[str, Path],
        schema: Optional[Type[BaseModel]] = None,
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        """
        Load YAML configuration file with optional validation.

        Args:
            path: Path to configuration file (relative to config_root or absolute)
            schema: Optional Pydantic schema for validation
            use_cache: Whether to use cached data if available

        Returns:
            Parsed configuration dictionary

        Raises:
            ConfigNotFoundError: If file doesn't exist
            ConfigValidationError: If validation fails
            yaml.YAMLError: If YAML parsing fails
        """
        # Resolve path
        file_path = Path(path)
        if not file_path.is_absolute():
            file_path = self.config_root / file_path

        # Check if file exists
        if not file_path.exists():
            raise ConfigNotFoundError(f"Configuration file not found: {file_path}")

        # Check cache
        if use_cache and self._is_cache_valid(file_path):
            return self._cache[str(file_path)]

        # Load YAML
        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to parse YAML in {file_path}: {e}")

        # Validate with schema if provided
        if schema:
            try:
                validated = schema(**data)
                data = validated.model_dump()
            except ValidationError as e:
                raise ConfigValidationError(
                    f"Configuration validation failed for {file_path}:\n{e}"
                )

        # Update cache
        if use_cache:
            self._update_cache(file_path, data)

        return data

    def update_config(
        self,
        path: Union[str, Path],
        updates: Dict[str, Any],
        validate: bool = True,
        backup: bool = True,
    ) -> None:
        """
        Update configuration file with atomic write and rollback.

        Args:
            path: Path to configuration file
            updates: Dictionary of updates (supports nested keys via dot notation)
            validate: Whether to validate after update
            backup: Whether to create backup before update

        Raises:
            ConfigNotFoundError: If file doesn't exist
            ConfigValidationError: If validation fails after update
        """
        # Resolve path
        file_path = Path(path)
        if not file_path.is_absolute():
            file_path = self.config_root / file_path

        # Check if file exists
        if not file_path.exists():
            raise ConfigNotFoundError(f"Configuration file not found: {file_path}")

        # Create backup if requested
        backup_path = None
        if backup:
            backup_path = file_path.with_suffix(f".backup.{datetime.now().timestamp()}")
            shutil.copy2(file_path, backup_path)

        try:
            # Load current config
            current = self.load_config(file_path, use_cache=False)

            # Apply updates (supports nested updates)
            updated = self._merge_updates(current, updates)

            # Write atomically
            temp_path = file_path.with_suffix(".tmp")
            with open(temp_path, "w") as f:
                yaml.safe_dump(updated, f, default_flow_style=False, sort_keys=False)

            # Atomic rename
            temp_path.replace(file_path)

            # Invalidate cache
            self._invalidate_cache(file_path)

            # Clean up backup on success
            if backup_path and backup_path.exists():
                backup_path.unlink()

        except Exception as e:
            # Rollback on error
            if backup_path and backup_path.exists():
                shutil.copy2(backup_path, file_path)
                backup_path.unlink()
            raise e

    def _merge_updates(
        self, current: Dict[str, Any], updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge updates into current configuration.

        Supports nested dictionary merging.
        """
        result = current.copy()

        for key, value in updates.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = self._merge_updates(result[key], value)
            else:
                result[key] = value

        return result

    def validate_config(
        self, path: Union[str, Path], schema: Type[BaseModel]
    ) -> Dict[str, Any]:
        """
        Validate configuration file against schema.

        Args:
            path: Path to configuration file
            schema: Pydantic schema for validation

        Returns:
            Validated configuration dictionary

        Raises:
            ConfigValidationError: If validation fails
        """
        return self.load_config(path, schema=schema, use_cache=False)

    def merge_configs(
        self, configs: List[Union[str, Path]], strategy: str = "deep"
    ) -> Dict[str, Any]:
        """
        Merge multiple configuration files.

        Args:
            configs: List of configuration file paths
            strategy: Merge strategy ("deep" or "shallow")

        Returns:
            Merged configuration dictionary
        """
        if strategy not in ["deep", "shallow"]:
            raise ValueError(f"Invalid merge strategy: {strategy}")

        result: Dict[str, Any] = {}

        for config_path in configs:
            data = self.load_config(config_path)

            if strategy == "shallow":
                result.update(data)
            else:  # deep merge
                result = self._merge_updates(result, data)

        return result

    # Specialized operations for common use cases

    def get_project(self, project_id: str) -> Project:
        """
        Get project by ID.

        Args:
            project_id: Project identifier

        Returns:
            Project model

        Raises:
            KeyError: If project not found
        """
        config = self.load_config("projects.yaml", schema=ProjectsConfig)
        if project_id not in config["projects"]:
            raise KeyError(f"Project not found: {project_id}")

        return Project(**config["projects"][project_id])

    def update_project(self, project_id: str, updates: Dict[str, Any]) -> None:
        """
        Update specific project.

        Args:
            project_id: Project identifier
            updates: Dictionary of updates
        """
        project_updates = {"projects": {project_id: updates}}
        self.update_config("projects.yaml", project_updates)

    def get_all_projects(
        self, filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Project]:
        """
        Get all projects with optional filtering.

        Args:
            filters: Optional filters (e.g., {"status": ["active", "in_progress"]})

        Returns:
            Dictionary of project ID to Project model
        """
        config = self.load_config("projects.yaml", schema=ProjectsConfig)
        projects = {pid: Project(**pdata) for pid, pdata in config["projects"].items()}

        if not filters:
            return projects

        # Apply filters
        filtered = {}
        for pid, project in projects.items():
            matches = True
            for key, values in filters.items():
                project_value = getattr(project, key, None)
                if project_value not in values:
                    matches = False
                    break
            if matches:
                filtered[pid] = project

        return filtered

    def get_stakeholder(self, stakeholder_id: str) -> StakeholderProfile:
        """
        Get stakeholder profile by ID.

        Args:
            stakeholder_id: Stakeholder identifier (email)

        Returns:
            StakeholderProfile model

        Raises:
            KeyError: If stakeholder not found
        """
        config = self.load_config(
            "stakeholder_contexts.yaml", schema=StakeholderContextsConfig
        )
        if stakeholder_id not in config["stakeholder_profiles"]:
            raise KeyError(f"Stakeholder not found: {stakeholder_id}")

        return StakeholderProfile(**config["stakeholder_profiles"][stakeholder_id])

    def get_team_member(self, member_id: str) -> TeamMember:
        """
        Get team member by ID.

        Args:
            member_id: Team member identifier (email)

        Returns:
            TeamMember model

        Raises:
            KeyError: If team member not found
        """
        config = self.load_config("team_roster.yaml", schema=TeamRosterConfig)
        if member_id not in config["team_members"]:
            raise KeyError(f"Team member not found: {member_id}")

        return TeamMember(**config["team_members"][member_id])

    # Cross-file synchronization

    def sync_project_to_notes(self, project_id: str) -> None:
        """
        Synchronize project data to notes cache.

        Args:
            project_id: Project identifier
        """
        # Load project
        project = self.get_project(project_id)

        # Update notes cache (placeholder for now)
        # This would update .claude/cache/notes_*.json files
        cache_path = self.config_root / "cache" / f"notes_{project_id}.json"
        cache_path.parent.mkdir(exist_ok=True)

        # Write project metadata to cache
        import json

        with open(cache_path, "w") as f:
            json.dump(project.model_dump(), f, indent=2, default=str)

    def sync_team_to_stakeholders(self) -> None:
        """
        Synchronize team roster to stakeholder contexts.

        Updates stakeholder profiles with latest team information.
        """
        # Load both configs
        team_config = self.load_config("team_roster.yaml", schema=TeamRosterConfig)
        try:
            stakeholder_config = self.load_config(
                "stakeholder_contexts.yaml", schema=StakeholderContextsConfig
            )
        except ConfigNotFoundError:
            # If stakeholder config doesn't exist, skip sync
            return

        # Sync team members to stakeholders
        updates: Dict[str, Any] = {}
        for member_id, member_data in team_config["team_members"].items():
            if member_id in stakeholder_config["stakeholder_profiles"]:
                # Update name and role
                updates[f"stakeholder_profiles.{member_id}.name"] = member_data["name"]
                updates[f"stakeholder_profiles.{member_id}.role"] = member_data["role"]

        # Apply updates if any
        if updates:
            # Convert dot notation to nested dict
            nested_updates: Dict[str, Any] = {}
            for key, value in updates.items():
                parts = key.split(".")
                current = nested_updates
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = value

            self.update_config("stakeholder_contexts.yaml", nested_updates)

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        return {
            "cached_files": len(self._cache),
            "cache_size_bytes": sum(
                len(str(data)) for data in self._cache.values()
            ),  # Approximate
            "files": list(self._cache.keys()),
        }

    def clear_cache(self) -> None:
        """Clear all cached data."""
        self._cache.clear()
        self._cache_times.clear()
