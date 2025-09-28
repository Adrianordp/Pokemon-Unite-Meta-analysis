from entity.build_response import BuildResponse


def test_build_instantiation():
    # Arrange
    pokemon = "Pikachu"
    role = "Attacker"
    pokemon_win_rate = 0.55
    pokemon_pick_rate = 0.20
    move_1 = "Thunderbolt"
    move_2 = "Electro Ball"
    moveset_win_rate = 0.60
    moveset_pick_rate = 0.15
    moveset_true_pick_rate = 0.10
    item = "Wise Glasses"
    moveset_item_win_rate = 0.62
    moveset_item_pick_rate = 0.12
    moveset_item_true_pick_rate = 0.08

    # Act
    build = BuildResponse(
        pokemon=pokemon,
        role=role,
        pokemon_win_rate=pokemon_win_rate,
        pokemon_pick_rate=pokemon_pick_rate,
        move_1=move_1,
        move_2=move_2,
        moveset_win_rate=moveset_win_rate,
        moveset_pick_rate=moveset_pick_rate,
        moveset_true_pick_rate=moveset_true_pick_rate,
        item=item,
        moveset_item_win_rate=moveset_item_win_rate,
        moveset_item_pick_rate=moveset_item_pick_rate,
        moveset_item_true_pick_rate=moveset_item_true_pick_rate,
    )

    # Assert
    assert build.pokemon == pokemon
    assert build.role == role
    assert build.pokemon_win_rate == pokemon_win_rate
    assert build.move_1 == move_1
    assert build.item == item
