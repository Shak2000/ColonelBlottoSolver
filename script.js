document.addEventListener('DOMContentLoaded', () => {
    const troopsInput = document.getElementById('troops');
    const fieldsInput = document.getElementById('fields');
    const solveButton = document.getElementById('solveButton');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsDiv = document.getElementById('results');
    const solutionComboSpan = document.getElementById('solutionCombo');
    const winProbSpan = document.getElementById('winProb');
    const drawProbSpan = document.getElementById('drawProb');
    const loseProbSpan = document.getElementById('loseProb');
    const conditionMetParagraph = document.getElementById('conditionMet');
    const errorMessageDiv = document.getElementById('errorMessage');
    const errorTextParagraph = document.getElementById('errorText');

    solveButton.addEventListener('click', async () => {
        const troops = troopsInput.value;
        const fields = fieldsInput.value;

        // Reset previous results and errors
        resultsDiv.classList.add('hidden');
        errorMessageDiv.classList.add('hidden');
        loadingIndicator.classList.remove('hidden');

        try {
            // Call the /new_game endpoint to initialize the game on the server
            const newGameResponse = await fetch(`/new_game?troops=${troops}&fields=${fields}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!newGameResponse.ok) {
                const errorData = await newGameResponse.json();
                throw new Error(errorData.detail || `HTTP error! status: ${newGameResponse.status}`);
            }

            // After initializing, call the /solve_blotto endpoint
            const solveResponse = await fetch('/solve_blotto');

            if (!solveResponse.ok) {
                const errorData = await solveResponse.json();
                throw new Error(errorData.detail || `HTTP error! status: ${solveResponse.status}`);
            }

            const data = await solveResponse.json();

            // The data returned from solve_blotto is a list:
            // [solution_combo, win_prob, draw_prob, lose_prob, min_win_minus_lose_diff_for_solution]
            const [solution_combo, win_prob, draw_prob, lose_prob, min_win_minus_lose_diff_for_solution] = data;

            solutionComboSpan.textContent = solution_combo ? solution_combo.join(', ') : 'N/A';
            winProbSpan.textContent = win_prob !== undefined ? win_prob.toFixed(4) : 'N/A';
            drawProbSpan.textContent = draw_prob !== undefined ? draw_prob.toFixed(4) : 'N/A';
            loseProbSpan.textContent = lose_prob !== undefined ? lose_prob.toFixed(4) : 'N/A';

            if (min_win_minus_lose_diff_for_solution >= 0) {
                conditionMetParagraph.textContent = `This combination ensures the probability of winning is greater than or equal to the probability of losing against ANY opponent strategy (minimum win-lose difference: ${min_win_minus_lose_diff_for_solution.toFixed(4)}).`;
                conditionMetParagraph.classList.remove('text-red-300');
                conditionMetParagraph.classList.add('text-green-300');
            } else {
                conditionMetParagraph.textContent = `Note: No pure strategy was found where the probability of winning is always greater than or equal to the probability of losing against every opponent strategy. This is the best available pure strategy found, maximizing the minimum (win_prob - lose_prob) difference (which is ${min_win_minus_lose_diff_for_solution.toFixed(4)}).`;
                conditionMetParagraph.classList.remove('text-green-300');
                conditionMetParagraph.classList.add('text-red-300');
            }

            resultsDiv.classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            errorTextParagraph.textContent = `An error occurred: ${error.message}. Please check your inputs.`;
            errorMessageDiv.classList.remove('hidden');
        } finally {
            loadingIndicator.classList.add('hidden');
        }
    });
});
