const apiBase = 'http://localhost:8000';

document.getElementById('go').addEventListener('click', analyzePassword);
document.getElementById('pw').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        analyzePassword();
    }
});

function getRatingClass(rating) {
    const ratingMap = {
        'very weak': 'very-weak',
        'weak': 'weak',
        'moderate': 'moderate',
        'strong': 'strong',
        'very strong': 'very-strong'
    };
    return ratingMap[rating.toLowerCase()] || '';
}

function formatJSON(data) {
    // Format the JSON output to be more readable
    const formatted = {};
    
    // Basic info
    formatted.Password = '*'.repeat(data.length);
    formatted.Length = data.length;
    formatted.Rating = data.rating;
    formatted.Score = `${data.final_score.toFixed(1)}/100`;
    
    // Scores
    formatted['Score Breakdown'] = {
        'Character Variety': (data.variety_score * 100).toFixed(1) + '%',
        'Length Score': (data.length_score * 100).toFixed(1) + '%',
        'Adjacency Ratio': (data.adjacency_ratio * 100).toFixed(1) + '% (lower is better)',
        'Longest Path Segment': `${data.longest_simple_path_length} chars (${data.longest_path_segment})`,
        'Vertex Cover Ratio': (data.vc_ratio * 100).toFixed(1) + '% (lower is better)'
    };
    
    // Graph info
    formatted['Graph Analysis'] = {
        'Unique Nodes': data.induced_nodes.length,
        'Edges in Induced Graph': data.induced_edges.length,
        'Average Log Degree': data.avg_log_degree.toFixed(3)
    };
    
    return JSON.stringify(formatted, null, 2);
}

async function analyzePassword() {
    const pwInput = document.getElementById('pw');
    const outElement = document.getElementById('out');
    const scoreDisplay = document.getElementById('score-display');
    const ratingText = document.getElementById('rating-text');
    const scoreValue = document.getElementById('score-value');
    
    const pw = pwInput.value.trim();
    
    if (!pw) {
        outElement.textContent = 'Please enter a password to analyze';
        scoreDisplay.style.display = 'none';
        return;
    }
    
    try {
        outElement.textContent = 'Analyzing...';
        
        const response = await fetch(apiBase + '/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: pw })
        });
        
        if (!response.ok) {
            const error = await response.text();
            throw new Error(error || 'Failed to analyze password');
        }
        
        const result = await response.json();
        
        // Update the score display
        const rating = result.rating;
        const score = result.final_score.toFixed(1);
        
        // Set the rating text and class
        ratingText.textContent = `${rating.charAt(0).toUpperCase() + rating.slice(1)}: `;
        scoreValue.textContent = `${score}/100`;
        
        // Update the display
        scoreDisplay.className = `score ${getRatingClass(rating)}`;
        scoreDisplay.style.display = 'block';
        
        // Format and display the full results
        outElement.textContent = formatJSON(result);
        
    } catch (error) {
        console.error('Error:', error);
        outElement.textContent = `Error: ${error.message}. Make sure the backend server is running.`;
        scoreDisplay.style.display = 'none';
    }
}
