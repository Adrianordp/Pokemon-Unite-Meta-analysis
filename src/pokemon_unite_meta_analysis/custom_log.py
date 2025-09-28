"""
Module for logging setup.
Provides functionality to retrieve, process, and print sorted Pokémon build
data from the latest table in the BuildRepository. The data is sorted by
'moveset item true pick rate' and 'moveset item win rate', with columns renamed
for readability. Builds are colorized based on their role (Support, Attacker, etc.)
when printed.
"""

from util.log import setup_custom_logger

LOG = setup_custom_logger("log_manipulate_builds")
