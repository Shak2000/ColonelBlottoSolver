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
        Finds the most robust pure strategy for the player.
        It identifies the player's combination that maximizes the minimum
        (win_prob - lose_prob) difference across all opponent strategies.
        This ensures a solution is always returned if combinations exist.
        """
        best_solution = None
        # Initialize with a very low value to ensure any valid solution is better
        # This will track the best 'min_win_minus_lose_diff' found across all player combos
        overall_max_min_win_minus_lose_diff = -float('inf')

        # To store the probabilities of the best solution found (average across all opponent strategies)
        overall_best_win_prob = 0.0
        overall_best_draw_prob = 0.0
        overall_best_lose_prob = 0.0

        # Iterate through all possible combinations for the current player
        for player_combo_base in self.combos:
            # Generate all unique permutations of the player's base combination
            player_permutations = list(set(itertools.permutations(player_combo_base)))

            # Initialize minimum win_prob - lose_prob difference for this player_combo_base
            # This tracks the worst-case scenario for the current player_combo_base
            current_player_min_win_minus_lose_diff = float('inf')

            # Accumulate probabilities for averaging across all opponent strategies for *this* player_combo_base
            current_player_avg_win_prob_sum = 0.0
            current_player_avg_draw_prob_sum = 0.0
            current_player_avg_lose_prob_sum = 0.0
            current_player_opponent_strategies_count = 0

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

                # Calculate the difference (win_prob - lose_prob) for this specific opponent strategy
                win_minus_lose_diff_vs_opponent = win_prob_vs_opponent - lose_prob_vs_opponent

                # Update the minimum (win_prob - lose_prob) for the current player's base combo
                # This finds the worst-case outcome for the current player_combo_base
                current_player_min_win_minus_lose_diff = min(
                    current_player_min_win_minus_lose_diff,
                    win_minus_lose_diff_vs_opponent
                )

                # Accumulate probabilities for averaging across all opponent strategies
                current_player_avg_win_prob_sum += win_prob_vs_opponent
                current_player_avg_draw_prob_sum += draw_prob_vs_opponent
                current_player_avg_lose_prob_sum += lose_prob_vs_opponent
                current_player_opponent_strategies_count += 1

            # After checking against all opponent strategies for the current player_combo_base:
            # We want to find the player_combo_base that maximizes its 'current_player_min_win_minus_lose_diff'.
            # This is the most robust strategy against the worst-case opponent.
            if current_player_min_win_minus_lose_diff > overall_max_min_win_minus_lose_diff:
                overall_max_min_win_minus_lose_diff = current_player_min_win_minus_lose_diff
                best_solution = player_combo_base

                # Calculate the average probabilities for this new best solution
                if current_player_opponent_strategies_count > 0:
                    overall_best_win_prob = current_player_avg_win_prob_sum / current_player_opponent_strategies_count
                    overall_best_draw_prob = current_player_avg_draw_prob_sum / current_player_opponent_strategies_count
                    overall_best_lose_prob = current_player_avg_lose_prob_sum / current_player_opponent_strategies_count
                else:
                    overall_best_win_prob = 0.0
                    overall_best_draw_prob = 0.0
                    overall_best_lose_prob = 0.0

        # Return the best solution found and its average probabilities.
        # Also return the overall_max_min_win_minus_lose_diff to check the strict condition in main().
        return best_solution, overall_best_win_prob, overall_best_draw_prob, overall_best_lose_prob, overall_max_min_win_minus_lose_diff


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
                # Unpack the new return value from solve_blotto
                solution_combo, win_prob, draw_prob, lose_prob, min_win_minus_lose_diff_for_solution = game.solve_blotto()

                if solution_combo:
                    print(f"\nSolution to the puzzle: {solution_combo}")
                    print(f"For this combination, considering all opponent strategies and permutations (average probabilities):")
                    print(f"  Probability of Winning: {win_prob:.4f}")
                    print(f"  Probability of Drawing: {draw_prob:.4f}")
                    print(f"  Probability of Losing:  {lose_prob:.4f}")

                    # Check if the strict condition (win_prob >= lose_prob against all opponent combos) is met
                    if min_win_minus_lose_diff_for_solution >= 0:
                        print(f"\nThis combination ensures the probability of winning is greater than or equal to the "
                              f"probability of losing against ANY opponent strategy (minimum win-lose difference: "
                              f"{min_win_minus_lose_diff_for_solution:.4f}).")
                    else:
                        print(f"\nNote: No pure strategy was found where the probability of winning is always greater "
                              f"than or equal to the probability of losing against every opponent strategy.")
                        print(f"This is the best available pure strategy found, maximizing the minimum (win_prob - "
                              f"lose_prob) difference (which is {min_win_minus_lose_diff_for_solution:.4f}).")
                else:
                    # This case should ideally not be hit if troops and fields are positive,
                    # as there will always be combinations.
                    print("No combinations generated. Please check input parameters.")

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
