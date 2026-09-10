async function studyTopic() {

    // Get the topic from the input field
    const topic = document.getElementById("topic").value.trim();

    // Get UI elements
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");

    // Validate input
    if (!topic) {
        alert("Please enter a topic!");
        return;
    }

    // Show loading message
    loading.style.display = "block";

    // Hide previous result
    result.style.display = "none";

    try {

        // Call FastAPI API
        const response = await fetch(
            `/study?topic=${encodeURIComponent(topic)}`
        );

        // Check for API errors
        if (!response.ok) {
            throw new Error("Failed to generate study material");
        }

        // Convert API response to JSON
        const data = await response.json();

        // Display topic
        document.getElementById("topic-title").innerText =
            "📖 Topic: " + data.topic;

        // Display explanation
        document.getElementById("explanation").innerText =
            data.explanation;

        // Display quiz
        document.getElementById("quiz").innerText =
            data.quiz;

        // Show result
        result.style.display = "block";

    } catch (error) {

        alert("Error: " + error.message);

    } finally {

        // Hide loading message
        loading.style.display = "none";

    }
}