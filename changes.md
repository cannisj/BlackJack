## Version 1.1.0  (2023-05-22)

**Changes**

* **Buy-in Feature:**
    *   Implemented `player_wants_buyback()` function to offer the player a buy-in option when their chips run out.
    *   Modified `reset_game_state()` to reset the player's chips to 100 when they choose to buy back in.
    *   Integrated the buy-in logic within the main `game()` function, allowing seamless continuation of the game.

* **Robustness Improvements:**
    *   Added null pointer checks to `reset_game_state()` to prevent crashes if any game objects (deck, hands, chips) are not properly initialized.
    *   Enclosed deck reshuffling within a `try-except` block for more robust error handling. If an unexpected issue arises during reshuffling, an error message is displayed.

**Future Considerations** 

* **Implement a variable buy-in amount, allowing the player more choice.**
* **Add minimum and maximum betting limits to the game.**
* **Add chip tracker to maintain chip count after each hand.**