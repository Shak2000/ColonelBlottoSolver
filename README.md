# Colonel Blotto Solver

A strategic game theory solver for the classic Colonel Blotto problem, featuring both a web interface and command-line interface.

## What is Colonel Blotto?

Colonel Blotto is a classic game theory problem where two players simultaneously distribute their troops across multiple battlefields. Each player wins a battlefield if they allocate more troops to it than their opponent. The player who wins the most battlefields wins the overall game.

## Features

- **Web Interface**: Modern, responsive web application with real-time solving
- **Command Line Interface**: Terminal-based solver for quick calculations
- **Robust Strategy Finding**: Finds the most robust pure strategy using minimax principles
- **Comprehensive Analysis**: Calculates win/draw/lose probabilities against all possible opponent strategies
- **Permutation Handling**: Considers all possible arrangements of troop distributions

## Project Structure

```
colonel-blotto-solver/
├── app.py          # FastAPI web server
├── main.py         # Core game logic and CLI interface
├── index.html      # Web interface
├── styles.css      # Custom styling
├── script.js       # Frontend JavaScript
└── README.md       # This file
```

## Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Setup

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn
   ```

3. **Run the application**:
   ```bash
   uvicorn app:app --reload
   ```

4. **Access the web interface** at `http://localhost:8000`

## Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:8000`
2. Enter the number of troops and fields
3. Click "Solve Puzzle" to find the optimal strategy
4. View the recommended troop distribution

### Command Line Interface

Run the standalone solver:
```bash
python main.py
```

Follow the prompts to:
- Enter number of troops
- Enter number of fields
- View the optimal strategy and probability analysis

## How It Works

### Algorithm

The solver uses a minimax approach to find the most robust pure strategy:

1. **Generate Combinations**: Creates all possible ways to distribute troops across fields
2. **Permutation Analysis**: Considers all arrangements of each combination
3. **Battle Simulation**: Simulates battles between all player and opponent permutations
4. **Robustness Evaluation**: Finds the strategy that maximizes the minimum (win_prob - lose_prob) difference
5. **Strategy Selection**: Returns the most robust strategy against worst-case opponents

### Strategy Evaluation

For each potential strategy, the solver:
- Tests it against every possible opponent strategy
- Calculates win/draw/lose probabilities
- Finds the worst-case scenario (minimum win-lose difference)
- Selects the strategy with the best worst-case performance

## Example

**Input**: 5 troops, 3 fields

**Output**: `[2, 2, 1]` - Deploy 2 troops to first field, 2 to second field, 1 to third field

This means the optimal strategy is to distribute your 5 troops as 2-2-1 across the three battlefields.

## API Endpoints

### Web Server Endpoints

- `GET /` - Serves the web interface
- `POST /new_game?troops={n}&fields={m}` - Initialize a new game
- `GET /solve_blotto` - Solve the current game and return optimal strategy

### Response Format

The solver returns:
```json
[
  [2, 2, 1],        // Optimal troop distribution
  0.6667,           // Win probability
  0.1667,           // Draw probability  
  0.1667,           // Lose probability
  0.5000            // Minimum win-lose difference
]
```

## Technical Details

### Core Classes

- **Game**: Main class handling troop combinations and battle simulation
- **get_combos()**: Recursively generates all valid troop distributions
- **calculate_outcome()**: Determines winner of individual battles
- **solve_blotto()**: Implements the minimax strategy selection

### Web Framework

- **FastAPI**: Modern Python web framework for the API
- **Vanilla JavaScript**: Frontend interaction and API calls
- **Tailwind CSS**: Utility-first CSS framework for styling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Game Theory Background

Colonel Blotto is a fundamental problem in game theory that demonstrates:
- **Zero-sum games**: One player's gain equals another's loss
- **Resource allocation**: Optimal distribution of limited resources
- **Strategic thinking**: Anticipating opponent moves
- **Minimax principle**: Maximizing minimum expected payoff

The solver finds pure strategies rather than mixed strategies, making it practical for real-world applications where you need a single, concrete plan of action.

## Limitations

- Focuses on pure strategies only (not mixed strategies)
- Assumes symmetric games (both players have same number of troops)
- Computational complexity grows exponentially with troops and fields
- Best suited for small to medium-sized games (≤20 troops, ≤10 fields)

## Future Enhancements

- Support for asymmetric games (different troop counts)
- Mixed strategy Nash equilibrium solver
- Performance optimizations for larger games
- Historical game analysis and learning
- Multi-player variant support
