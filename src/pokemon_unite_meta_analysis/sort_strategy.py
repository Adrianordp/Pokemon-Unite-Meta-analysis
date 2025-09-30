# src/pokemon_unite_meta_analysis/sort_by.py
from typing import List

from entity.build_response import BuildResponse
from entity.sort_by import SortBy
from pokemon_unite_meta_analysis.custom_log import LOG


class SortStrategy:
    def apply(
        self, builds: List[BuildResponse], reverse: bool = True
    ) -> List[BuildResponse]:
        raise NotImplementedError()


class PokemonSortStrategy(SortStrategy):
    def apply(
        self, builds: List[BuildResponse], reverse: bool = False
    ) -> List[BuildResponse]:
        LOG.info("Sorting by Pokemon")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Reverse: %s", reverse)

        return sorted(builds, key=lambda b: b.pokemon, reverse=reverse)


class RoleSortStrategy(SortStrategy):
    def apply(
        self, builds: List[BuildResponse], reverse: bool = False
    ) -> List[BuildResponse]:
        LOG.info("Sorting by Role")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Reverse: %s", reverse)

        return sorted(builds, key=lambda b: b.role, reverse=reverse)


class PokemonWinRateSortStrategy(SortStrategy):
    def apply(
        self, builds: List[BuildResponse], reverse: bool = True
    ) -> List[BuildResponse]:
        LOG.info("Sorting by Pokemon Win Rate")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Reverse: %s", reverse)

        return sorted(builds, key=lambda b: b.pokemon_win_rate, reverse=reverse)


class PokemonPickRateSortStrategy(SortStrategy):
    def apply(
        self, builds: List[BuildResponse], reverse: bool = True
    ) -> List[BuildResponse]:
        LOG.info("Sorting by Pokemon Pick Rate")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Reverse: %s", reverse)

        return sorted(
            builds, key=lambda b: b.pokemon_pick_rate, reverse=reverse
        )


class MovesetWinRateSortStrategy(SortStrategy):
    def apply(
        self, builds: List[BuildResponse], reverse: bool = True
    ) -> List[BuildResponse]:
        LOG.info("Sorting by Moveset Win Rate")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Reverse: %s", reverse)

        return sorted(builds, key=lambda b: b.moveset_win_rate, reverse=reverse)


class MovesetPickRateSortStrategy(SortStrategy):
    def apply(
        self, builds: List[BuildResponse], reverse: bool = True
    ) -> List[BuildResponse]:
        LOG.info("Sorting by Moveset Pick Rate")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Reverse: %s", reverse)

        return sorted(
            builds, key=lambda b: b.moveset_pick_rate, reverse=reverse
        )


class MovesetTruePickRateSortStrategy(SortStrategy):
    def apply(
        self, builds: List[BuildResponse], reverse: bool = True
    ) -> List[BuildResponse]:
        LOG.info("Sorting by Moveset True Pick Rate")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Reverse: %s", reverse)

        return sorted(
            builds, key=lambda b: b.moveset_true_pick_rate, reverse=reverse
        )


class ItemSortStrategy(SortStrategy):
    def apply(
        self, builds: List[BuildResponse], reverse: bool = False
    ) -> List[BuildResponse]:
        LOG.info("Sorting by Item")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Reverse: %s", reverse)

        return sorted(builds, key=lambda b: b.item, reverse=reverse)


class MovesetItemWinRateSortStrategy(SortStrategy):
    def apply(
        self, builds: List[BuildResponse], reverse: bool = True
    ) -> List[BuildResponse]:
        LOG.info("Sorting by Moveset Item Win Rate")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Reverse: %s", reverse)

        return sorted(
            builds, key=lambda b: b.moveset_item_win_rate, reverse=reverse
        )


class MovesetItemPickRateSortStrategy(SortStrategy):
    def apply(
        self, builds: List[BuildResponse], reverse: bool = True
    ) -> List[BuildResponse]:
        LOG.info("Sorting by Moveset Item Pick Rate")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Reverse: %s", reverse)

        return sorted(
            builds, key=lambda b: b.moveset_item_pick_rate, reverse=reverse
        )


class MovesetItemTruePickRateSortStrategy(SortStrategy):
    def apply(
        self, builds: List[BuildResponse], reverse: bool = True
    ) -> List[BuildResponse]:
        LOG.info("Sorting by Moveset Item True Pick Rate")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Reverse: %s", reverse)

        return sorted(
            builds, key=lambda b: b.moveset_item_true_pick_rate, reverse=reverse
        )


SORT_STRATEGIES = {
    SortBy.POKEMON: PokemonSortStrategy(),
    SortBy.ROLE: RoleSortStrategy(),
    SortBy.POKEMON_WIN_RATE: PokemonWinRateSortStrategy(),
    SortBy.POKEMON_PICK_RATE: PokemonPickRateSortStrategy(),
    SortBy.MOVESET_WIN_RATE: MovesetWinRateSortStrategy(),
    SortBy.MOVESET_PICK_RATE: MovesetPickRateSortStrategy(),
    SortBy.MOVESET_TRUE_PICK_RATE: MovesetTruePickRateSortStrategy(),
    SortBy.ITEM: ItemSortStrategy(),
    SortBy.MOVESET_ITEM_WIN_RATE: MovesetItemWinRateSortStrategy(),
    SortBy.MOVESET_ITEM_PICK_RATE: MovesetItemPickRateSortStrategy(),
    SortBy.MOVESET_ITEM_TRUE_PICK_RATE: MovesetItemTruePickRateSortStrategy(),
}
