"""
Defines relevance strategies for filtering builds based on different criteria.
"""

from typing import Callable, Protocol

from entity.build_response import BuildResponse
from entity.relevance import Relevance
from pokemon_unite_meta_analysis.custom_log import LOG


class RelevanceStrategy(Protocol):
    """
    Relevance strategy interface

    Args:
        builds (list[BuildResponse]): List of builds to filter
        threshold (float): Relevance threshold
        get_builds (Callable[[], list[BuildResponse]]): Function to get all
            builds

    Returns:
        list[BuildResponse]: Filtered list of builds
    """

    def apply(
        self,
        builds: list[BuildResponse],
        threshold: float,
        get_builds: Callable[[], list[BuildResponse]],
    ) -> list[BuildResponse]:
        raise NotImplementedError()


class AnyRelevanceStrategy:
    """Any relevance strategy

    Args:
        builds (list[BuildResponse]): List of builds to filter
        threshold (float): Ignored in this strategy
        get_builds (Callable[[], list[BuildResponse]]): Ignored in this strategy

    Returns:
        list[BuildResponse]: Filtered list of builds
    """

    def apply(
        self,
        builds: list[BuildResponse],
        threshold: float,
        get_builds: Callable[[], list[BuildResponse]],
    ) -> list[BuildResponse]:
        LOG.info("Applying Any Relevance Strategy")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Threshold: %s", threshold)
        LOG.debug("Get Builds: %s", get_builds)

        return builds


class PercentageRelevanceStrategy:
    """
    Percentage relevance strategy

    Pick builds with moveset_item_true_pick_rate >= threshold

    Args:
        builds (list[BuildResponse]): List of builds to filter
        threshold (float): Relevance threshold (0.0 to 100.0)
        get_builds (Callable[[], list[BuildResponse]]): Function to get all
            builds

    Returns:
        list[BuildResponse]: Filtered list of builds
    """

    def apply(
        self,
        builds: list[BuildResponse],
        threshold: float,
        get_builds: Callable[[], list[BuildResponse]],
    ) -> list[BuildResponse]:
        LOG.info("Applying Percentage Relevance Strategy")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Threshold: %s", threshold)
        LOG.debug("Get Builds: %s", get_builds)

        if threshold is None:
            LOG.warning("Threshold is None, returning all builds")
            return builds

        if threshold > 100.0:
            LOG.warning("Threshold > 100.0, returning no builds")
            return []

        if threshold <= 0.0:
            LOG.warning("Threshold <= 0.0, returning all builds")
            return builds

        return [
            build
            for build in builds
            if build.moveset_item_true_pick_rate >= threshold
        ]


class TopNRelevanceStrategy:
    """
    Top N relevance strategy

    Pick top N builds based on moveset_item_true_pick_rate

    Args:
        builds (list[BuildResponse]): List of builds to filter
        threshold (float): Relevance threshold (N)
        get_builds (Callable[[], list[BuildResponse]]): Function to get all
            builds

    Returns:
        list[BuildResponse]: Filtered list of builds
    """

    def apply(
        self,
        builds: list[BuildResponse],
        threshold: float,
        get_builds: Callable[[], list[BuildResponse]],
    ) -> list[BuildResponse]:
        LOG.info("Applying Top N Relevance Strategy")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Threshold: %s", threshold)
        LOG.debug("Get Builds: %s", get_builds)

        if threshold is None:
            LOG.warning("Threshold is None, returning all builds")
            return builds

        if threshold <= 0:
            LOG.warning("Threshold <= 0, returning no builds")
            return []

        if threshold > len(builds):
            LOG.warning("Threshold > number of builds, returning all builds")
            return builds

        position = int(threshold - 1)
        sorted_builds = sorted(
            get_builds(),
            key=lambda build: build.moveset_item_true_pick_rate,
            reverse=True,
        )
        cut_value = sorted_builds[position].moveset_item_true_pick_rate

        return [
            build
            for build in builds
            if build.moveset_item_true_pick_rate >= cut_value
        ]


class CumulativeCoverageRelevanceStrategy:
    """
    Cumulative coverage relevance strategy

    Pick builds until cumulative moveset_item_true_pick_rate >= threshold

    Args:
        builds (list[BuildResponse]): List of builds to filter
        threshold (float): Relevance threshold (0.0 to 1.0)
        get_builds (Callable[[], list[BuildResponse]]): Function to get all
            builds

    Returns:
        list[BuildResponse]: Filtered list of builds
    """

    def apply(
        self,
        builds: list[BuildResponse],
        threshold: float,
        get_builds: Callable[[], list[BuildResponse]],
    ) -> list[BuildResponse]:
        LOG.info("Applying Cumulative Coverage Relevance Strategy")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Threshold: %s", threshold)
        LOG.debug("Get Builds: %s", get_builds)

        if threshold is None:
            LOG.warning("Threshold is None, returning all builds")
            return builds

        if threshold <= 0.0:
            LOG.warning("Threshold <= 0.0, returning no builds")
            return []

        sorted_builds = sorted(
            get_builds(),
            key=lambda build: build.moveset_item_true_pick_rate,
            reverse=True,
        )
        cumulative = 0.0
        selected_builds: list[BuildResponse] = []

        for build in sorted_builds:
            cumulative += build.moveset_item_true_pick_rate
            selected_builds.append(build)

            if cumulative >= threshold:
                LOG.info("Cumulative coverage threshold met")
                break

        return selected_builds


class QuartileRelevanceStrategy:
    """
    Quartile relevance strategy

    Pick builds from most relevant quartiles based on moveset_item_true_pick_rate

    Args:
        builds (list[BuildResponse]): List of builds to filter
        threshold (float): Quartile threshold (1, 2, 3, or 4)
        get_builds (Callable[[], list[BuildResponse]]): Function to get all
            builds

    Returns:
        list[BuildResponse]: Filtered list of builds
    """

    def apply(
        self,
        builds: list[BuildResponse],
        threshold: float,
        get_builds: Callable[[], list[BuildResponse]],
    ) -> list[BuildResponse]:
        LOG.info("Applying Quartile Relevance Strategy")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Threshold: %s", threshold)
        LOG.debug("Get Builds: %s", get_builds)

        sorted_builds = sorted(
            get_builds(),
            key=lambda build: build.moveset_item_true_pick_rate,
            reverse=True,
        )
        n = len(sorted_builds)

        if n == 0:
            LOG.warning("No builds available, returning no builds")
            return []

        if threshold is None:
            LOG.warning("Threshold is None, returning all builds")
            return builds

        if threshold < 1 or threshold > 4:
            LOG.warning(
                "Threshold must be between 1 and 4, returning no builds"
            )
            return []

        quartile_size = n // 4

        if threshold == 1:
            return sorted_builds[:quartile_size]

        if threshold == 2:
            return sorted_builds[: 2 * quartile_size]

        if threshold == 3:
            return sorted_builds[: 3 * quartile_size]

        if threshold == 4:
            return sorted_builds[: 4 * quartile_size]

        LOG.error("Unexpected case, returning no builds.")
        return []  # Fallback, should not reach here


RELEVANCE_STRATEGIES: dict[Relevance, RelevanceStrategy] = {
    Relevance.ANY: AnyRelevanceStrategy(),
    Relevance.PERCENTAGE: PercentageRelevanceStrategy(),
    Relevance.TOP_N: TopNRelevanceStrategy(),
    Relevance.CUMULATIVE_COVERAGE: CumulativeCoverageRelevanceStrategy(),
    Relevance.QUARTILE: QuartileRelevanceStrategy(),
}
