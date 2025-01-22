async function runSentimentAnalysis() {
  const textToAnalyze = document.getElementById("textToAnalyze").value;
  const responseDiv = document.getElementById("system_response");
  const loadingIndicator = document.getElementById("loadingIndicator");
  const loadingExcuse = document.getElementById("loadingExcuse");
  const analyzeButton = document.getElementById("analyzeButton");

  if (!textToAnalyze) {
    responseDiv.innerHTML =
      "<p class='error'>Please enter some text to analyze.</p>";
    return;
  }

  // Show loading indicator and disable button
  loadingIndicator.classList.remove("hidden");
  loadingExcuse.classList.remove("hidden");
  analyzeButton.disabled = true;
  responseDiv.innerHTML = "";

  try {
    const url = "https://emotion-detection-text.onrender.com";
    const response = await fetch(
      `${url}/predict?text=${encodeURIComponent(textToAnalyze)}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    const data = await response.text();

    if (response.ok) {
      const result = JSON.parse(data);
      responseDiv.innerHTML = `
                  <h3>Top Emotion: <span class="emotion">${
                    result.top_emotion
                  }</span></h3>
                  <h4>Probabilities:</h4>
                  <ul>
                      ${Object.entries(result.probabilities)
                        .map(
                          ([emotion, probability]) => `
                          <li><strong>${emotion}:</strong> ${(
                            probability * 100
                          ).toFixed(2)}%</li>
                      `
                        )
                        .join("")}
                  </ul>
              `;
    } else {
      responseDiv.innerHTML = `<p class='error'>Error: ${
        data.detail || "An unexpected error occurred."
      }</p>`;
    }
  } catch (error) {
    console.error("Error fetching data:", error);
    responseDiv.innerHTML =
      "<p class='error'>An error occurred while fetching the data. Please try again later.</p>";
  } finally {
    // Hide loading indicator and enable button
    loadingIndicator.classList.add("hidden");
    loadingExcuse.classList.add("hidden");
    analyzeButton.disabled = false;
  }
}
