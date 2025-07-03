import itertools


class Game:
    def __init__(self, troops, fields):
        self.troops = troops
        self.fields = fields
        self.combos = []
        # Generate all possible combinations of troops for the given fields
        self.get_combos(0, troops, [0 for _ in range(fields)])
        self.map = dict()
        self.choice = []

    def get_combos(self, index, troops, combo):
        """
        Recursively generates all combinations of distributing 'troops' across 'fields'.
        Each combination is a list where each element represents troops on a field.
        """
        if troops == 0:
            # If all troops are distributed, add the current combination to the list
            self.combos.append(list(combo)) # Use list(combo) to append a copy
            return
        elif index == len(combo) - 1:
            # If it's the last field, assign all remaining troops to it
            combo[-1] += troops
            self.combos.append(list(combo)) # Use list(combo) to append a copy
            combo[-1] -= troops # Backtrack for other combinations
            return

        # Iterate through possible troop counts for the current field
        for i in range(0, troops + 1):
            combo[index] += i
            # Recurse for the next field with remaining troops
            self.get_combos(index + 1, troops - i, combo)
            combo[index] -= i # Backtrack for other combinations

    def calculate_outcome(self, player_combo, opponent_combo):
        """
        Calculates the outcome of a battle between two combinations.
        Returns 1 if player_combo wins, -1 if opponent_combo wins, 0 for a draw.
        """
        player_score = 0
        opponent_score = 0
        for i in range(self.fields):
            if player_combo[i] > opponent_combo[i]:
                player_score += 1
            elif opponent_combo[i] > player_combo[i]:
                opponent_score += 1
        if player_score > opponent_score:
            return 1  # Player wins
        elif opponent_score > player_score:
            return -1 # Opponent wins
        else:
            return 0  # Draw

    def solve_blotto(self):
        """
        Finds a combination of troops that guarantees a win or draw against
        any opponent's combination, considering permutations.
        It now prioritizes combinations where win probability >= lose probability,
        and among those, maximizes (win_prob - lose_prob).
        """
        best_solution = None
        # Initialize with a very low value to ensure any valid solution is better
        max_min_win_minus_lose_diff = -float('inf')
        # To store the probabilities of the best solution found
        best_win_prob = 0.0
        best_draw_prob = 0.0
        best_lose_prob = 0.0

        # Iterate through all possible combinations for the current player
        for player_combo_base in self.combos:
            # Generate all unique permutations of the player's base combination
            player_permutations = list(set(itertools.permutations(player_combo_base)))

            # Initialize minimum win_prob - lose_prob difference for this player_combo_base
            min_win_minus_lose_diff_for_player_combo = float('inf')

            # Store average probabilities against all opponent strategies for this player_combo_base
            avg_win_prob_sum = 0.0
            avg_draw_prob_sum = 0.0
            avg_lose_prob_sum = 0.0
            opponent_strategies_count = 0

            # For each opponent's base combination
            for opponent_combo_base in self.combos:
                # Generate all unique permutations of the opponent's base combination
                opponent_permutations = list(set(itertools.permutations(opponent_combo_base)))

                total_outcomes = 0
                player_wins = 0
                draws = 0
                player_losses = 0

                # Simulate battles between all permutations of player and opponent
                for p_perm in player_permutations:
                    for o_perm in opponent_permutations:
                        outcome = self.calculate_outcome(list(p_perm), list(o_perm))
                        total_outcomes += 1
                        if outcome == 1:
                            player_wins += 1
                        elif outcome == 0:
                            draws += 1
                        else: # outcome == -1
                            player_losses += 1

                # Calculate probabilities against this specific opponent's base combination
                if total_outcomes > 0:
                    win_prob_vs_opponent = player_wins / total_outcomes
                    draw_prob_vs_opponent = draws / total_outcomes
                    lose_prob_vs_opponent = player_losses / total_outcomes
                else:
                    win_prob_vs_opponent = 0.0
                    draw_prob_vs_opponent = 0.0
                    lose_prob_vs_opponent = 0.0

                # Calculate the difference (win_prob - lose_prob) for this opponent
                win_minus_lose_diff_vs_opponent = win_prob_vs_opponent - lose_prob_vs_opponent

                # Update the minimum (win_prob - lose_prob) for the current player's base combo
                min_win_minus_lose_diff_for_player_combo = min(
                    min_win_minus_lose_diff_for_player_combo,
                    win_minus_lose_diff_vs_opponent
                )

                # Accumulate probabilities for averaging across all opponent strategies
                avg_win_prob_sum += win_prob_vs_opponent
                avg_draw_prob_sum += draw_prob_vs_opponent
                avg_lose_prob_sum += lose_prob_vs_opponent
                opponent_strategies_count += 1

            # After checking against all opponent strategies, evaluate this player_combo_base
            # Condition: win_prob >= lose_prob (i.e., min_win_minus_lose_diff_for_player_combo >= 0)
            # And it must be better than previous best solutions
            if min_win_minus_lose_diff_for_player_combo >= 0 and \
               min_win_minus_lose_diff_for_player_combo >= max_min_win_minus_lose_diff:

                max_min_win_minus_lose_diff = min_win_minus_lose_diff_for_player_combo
                best_solution = player_combo_base

                # Calculate the average probabilities for the best solution found
                if opponent_strategies_count > 0:
                    best_win_prob = avg_win_prob_sum / opponent_strategies_count
                    best_draw_prob = avg_draw_prob_sum / opponent_strategies_count
                    best_lose_prob = avg_lose_prob_sum / opponent_strategies_count
                else:
                    best_win_prob = 0.0
                    best_draw_prob = 0.0
                    best_lose_prob = 0.0

        return best_solution, best_win_prob, best_draw_prob, best_lose_prob


def main():
    """
    Main function to run the Colonel Blotto game solver.
    Provides a menu for the user to solve puzzles or quit.
    """
    while True:
        print("\n--- Colonel Blotto Game Solver ---")
        print("1. Solve a puzzle")
        print("2. Quit")

        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            try:
                troops = int(input("Enter the number of troops: "))
                fields = int(input("Enter the number of fields: "))

                if troops <= 0 or fields <= 0:
                    print("Number of troops and fields must be positive integers.")
                    continue

                print(f"\nCalculating solution for {troops} troops and {fields} fields...")
                game = Game(troops, fields)
                solution_combo, win_prob, draw_prob, lose_prob = game.solve_blotto()

                if solution_combo:
                    print(f"\nSolution to the puzzle: {solution_combo}")
                    print(f"For this combination, considering all opponent strategies and permutations:")
                    print(f"  Probability of Winning: {win_prob:.4f}")
                    print(f"  Probability of Drawing: {draw_prob:.4f}")
                    print(f"  Probability of Losing:  {lose_prob:.4f}")
                    if win_prob >= lose_prob:
                        print("\nThis combination ensures the probability of winning is "
                              "greater than or equal to the probability of losing.")
                    else:
                        print("\nNote: This combination was chosen as the best available, but "
                              "the win probability might still be less than the lose probability in some scenarios.")
                else:
                    print("No optimal solution found for the given parameters that satisfies win_prob >= lose_prob.")

            except ValueError:
                print("Invalid input. Please enter integer values for troops and fields.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '2':
            print("Exiting Colonel Blotto Game Solver. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
