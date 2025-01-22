async function RunSentimentAnalysis() {
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const responseDiv = document.getElementById("system_response");

    if (!textToAnalyze) {
        responseDiv.innerHTML = "Please enter some text to analyze.";
        return;
    }

    console.log("Running sentiment analysis...")
    console.log("Text: ", textToAnalyze)

    
    try {
        const response = await fetch(`http://127.0.0.1:8000/predict?text=${encodeURIComponent(textToAnalyze)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        console.log(response)
        const data = await response.text(); // Change to text() to handle unexpected end of response

        console.log(data)
        if (response.ok) {
            const result = JSON.parse(data);
            responseDiv.innerHTML = `
                <h3>Emotion Detection Result:</h3>
                <p>Top Emotion: ${result.top_emotion}</p>
                <p>Probabilities:</p>
                <ul>
                    ${Object.entries(result.probabilities).map(([emotion, probability]) => `
                        <li>${emotion}: ${probability.toFixed(2)}</li>
                    `).join('')}
                </ul>
            `;
        } else {
            responseDiv.innerHTML = "Error: " + data.detail;
        }
    } catch (error) {
        console.error("Error fetching data:", error);
        responseDiv.innerHTML = "An error occurred while fetching the data.";
    }
}
