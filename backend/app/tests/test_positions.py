from app.commands.trades import get_positions_by_user
from app.commands.trades import build_grouped_positions


def test_positions_one_open(test_app, test_database,add_user, add_position):
    exchange = "ex"
    user = add_user("test", "test")

    add_position(user.id, "BASE", 1, 1, 1, 2, True)
    add_position(user.id, "BASE", 1, 1, 1, None, False)

    positions_df = get_positions_by_user(user.id)
    positions_df["current_price"] = 1
    positions_df = build_grouped_positions(positions_df, "BTC")
    
    assert positions_df["total_pl"][0] == 1
    assert positions_df["total_pl_perc"][0] == .5
    
    assert positions_df["realized_pl_perc"][0] == 1
    assert positions_df["realized_pl"][0] == 1
    assert positions_df["unrealized_pl_perc"][0] == 0
    assert positions_df["unrealized_pl"][0] == 0
    
    assert len(positions_df) == 1

