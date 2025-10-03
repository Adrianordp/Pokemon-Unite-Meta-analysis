from typing import List, Optional

from entity.build_response import BuildResponse
from pokemon_unite_meta_analysis.custom_log import LOG


class FilterStrategy:
    def apply(self, builds: List[BuildResponse], value: Optional[str]):
        raise NotImplementedError()


class PokemonFilterStrategy(FilterStrategy):
    def apply(self, builds: List[BuildResponse], value: Optional[str]):
        LOG.info("Applying Pokemon Filter Strategy")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Value: %s", value)

        if not value:
            return builds

        pokemon_list = [p.strip().lower() for p in value.split(",")]

        return [b for b in builds if b.pokemon.lower() in pokemon_list]


class RoleFilterStrategy(FilterStrategy):
    def apply(self, builds: List[BuildResponse], value: Optional[str]):
        LOG.info("Applying Role Filter Strategy")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Value: %s", value)

        if not value:
            return builds

        role_list = [r.strip().lower() for r in value.split(",")]

        return [b for b in builds if b.role.lower() in role_list]


class ItemFilterStrategy(FilterStrategy):
    def apply(self, builds: List[BuildResponse], value: Optional[str]):
        LOG.info("Applying Item Filter Strategy")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Value: %s", value)

        if not value:
            return builds

        item_list = [i.strip().lower() for i in value.split(",")]

        return [b for b in builds if b.item.lower() in item_list]


class IgnorePokemonFilterStrategy(FilterStrategy):
    def apply(self, builds: List[BuildResponse], value: Optional[str]):
        LOG.info("Applying Ignore Pokemon Filter Strategy")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Value: %s", value)

        if not value:
            return builds

        ignore_pokemon_list = [p.strip().lower() for p in value.split(",")]

        return [
            b for b in builds if b.pokemon.lower() not in ignore_pokemon_list
        ]


class IgnoreRoleFilterStrategy(FilterStrategy):
    def apply(self, builds: List[BuildResponse], value: Optional[str]):
        LOG.info("Applying Ignore Role Filter Strategy")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Value: %s", value)

        if not value:
            return builds

        ignore_role_list = [r.strip().lower() for r in value.split(",")]

        return [b for b in builds if b.role.lower() not in ignore_role_list]


class IgnoreItemFilterStrategy(FilterStrategy):
    def apply(self, builds: List[BuildResponse], value: Optional[str]):
        LOG.info("Applying Ignore Item Filter Strategy")
        LOG.debug("Builds:\n%s", builds)
        LOG.debug("Value: %s", value)

        if not value:
            return builds

        ignore_item_list = [i.strip().lower() for i in value.split(",")]

        return [b for b in builds if b.item.lower() not in ignore_item_list]


FILTER_STRATEGIES = {
    "pokemon": PokemonFilterStrategy(),
    "role": RoleFilterStrategy(),
    "item": ItemFilterStrategy(),
    "ignore_pokemon": IgnorePokemonFilterStrategy(),
    "ignore_role": IgnoreRoleFilterStrategy(),
    "ignore_item": IgnoreItemFilterStrategy(),
}
