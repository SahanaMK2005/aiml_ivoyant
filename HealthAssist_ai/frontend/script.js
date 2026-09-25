// =====================================================
// CHAT ELEMENTS
// =====================================================

const chatBox =
    document.getElementById("chat-box");

const userInput =
    document.getElementById("user-input");

const sendButton =
    document.getElementById("send-button");


// =====================================================
// DAY 16 EVALUATION ELEMENTS
// =====================================================

const testSelect =
    document.getElementById("test-select");

const runEvaluationButton =
    document.getElementById("run-evaluation-button");

const evaluationDetails =
    document.getElementById("evaluation-details");

const evaluationTestId =
    document.getElementById("evaluation-test-id");

const evaluationCategory =
    document.getElementById("evaluation-category");

const evaluationPrompt =
    document.getElementById("evaluation-prompt");

const evaluationExpected =
    document.getElementById("evaluation-expected");

const evaluationResponseContainer =
    document.getElementById("evaluation-response-container");

const evaluationResponse =
    document.getElementById("evaluation-response");


// =====================================================
// SUMMARY ELEMENTS
// =====================================================

const totalTests =
    document.getElementById("total-tests");

const testedCount =
    document.getElementById("tested-count");

const failureCount =
    document.getElementById("failure-count");

const hallucinationCount =
    document.getElementById("hallucination-count");


// =====================================================
// EVALUATION COUNTERS
// =====================================================

let testsRun = 0;

let failures = 0;

let hallucinations = 0;


// =====================================================
// ADD MESSAGE TO CHAT
// =====================================================

function addMessage(message, type) {

    const messageDiv =
        document.createElement("div");

    messageDiv.classList.add(
        "message",
        type
    );


    const contentDiv =
        document.createElement("div");

    contentDiv.classList.add(
        "message-content"
    );


    contentDiv.innerText =
        message;


    messageDiv.appendChild(
        contentDiv
    );


    chatBox.appendChild(
        messageDiv
    );


    chatBox.scrollTop =
        chatBox.scrollHeight;
}


// =====================================================
// USE SUGGESTION
// =====================================================

function useSuggestion(question) {

    userInput.value =
        question;

    userInput.focus();

    sendMessage();
}


// =====================================================
// SEND CHAT MESSAGE
// =====================================================

async function sendMessage() {

    const message =
        userInput.value.trim();


    // Don't send empty messages

    if (!message) {

        return;

    }


    // Remove welcome screen

    const welcome =
        document.getElementById("welcome");


    if (welcome) {

        welcome.remove();

    }


    // Display user message

    addMessage(
        message,
        "user"
    );


    // Clear input

    userInput.value = "";


    // Disable send button

    sendButton.disabled = true;


    // Create loading message

    const loadingDiv =
        document.createElement("div");


    loadingDiv.classList.add(
        "message",
        "ai"
    );


    loadingDiv.innerHTML = `
        <div class="message-content loading">
            HealthAssist AI is thinking...
        </div>
    `;


    chatBox.appendChild(
        loadingDiv
    );


    chatBox.scrollTop =
        chatBox.scrollHeight;


    try {

        // Send request to FastAPI

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        if (!response.ok) {

            throw new Error(
                "Server returned an error."
            );

        }


        // Convert response to JSON

        const data =
            await response.json();


        // Remove loading message

        loadingDiv.remove();


        // Display AI response

        addMessage(
            data.response,
            "ai"
        );

    }


    catch (error) {

        console.error(
            "HealthAssist error:",
            error
        );


        loadingDiv.remove();


        addMessage(
            "Sorry, I could not connect to HealthAssist AI. Please make sure the FastAPI server is running.",
            "ai"
        );

    }


    // Enable send button

    sendButton.disabled = false;


    // Focus input

    userInput.focus();
}


// =====================================================
// SEND BUTTON
// =====================================================

sendButton.addEventListener(
    "click",
    sendMessage
);


// =====================================================
// ENTER KEY
// =====================================================

userInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    }
);


// =====================================================
// DAY 16 - LOAD TEST CASES
// =====================================================

async function loadEvaluationTests() {

    try {

        const response =
            await fetch(
                "/evaluation/tests"
            );


        if (!response.ok) {

            throw new Error(
                "Could not load evaluation tests."
            );

        }


        const data =
            await response.json();


        // Clear dropdown

        testSelect.innerHTML = `
            <option value="">
                Select a test...
            </option>
        `;


        // Add test cases

        data.tests.forEach(
            function (test) {

                const option =
                    document.createElement("option");


                option.value =
                    test.id;


                option.textContent =
                    `${test.id} - ${test.category}`;


                testSelect.appendChild(
                    option
                );

            }
        );


        // Update total test count

        totalTests.textContent =
            data.tests.length;

    }


    catch (error) {

        console.error(
            "Evaluation loading error:",
            error
        );

    }
}


// =====================================================
// DAY 16 - SHOW SELECTED TEST
// =====================================================

testSelect.addEventListener(
    "change",
    async function () {

        const testId =
            testSelect.value;


        // Nothing selected

        if (!testId) {

            evaluationDetails.style.display =
                "none";


            evaluationResponseContainer.style.display =
                "none";


            return;

        }


        try {

            const response =
                await fetch(
                    `/evaluation/test/${testId}`
                );


            if (!response.ok) {

                throw new Error(
                    "Could not load test details."
                );

            }


            const test =
                await response.json();


            // Show test details

            evaluationDetails.style.display =
                "grid";


            evaluationTestId.textContent =
                test.id;


            evaluationCategory.textContent =
                test.category;


            evaluationPrompt.textContent =
                test.prompt;


            evaluationExpected.textContent =
                test.expected_behavior;


            // Hide previous AI response

            evaluationResponseContainer.style.display =
                "none";

        }


        catch (error) {

            console.error(
                "Test selection error:",
                error
            );

        }

    }
);


// =====================================================
// DAY 16 - RUN EVALUATION
// =====================================================

runEvaluationButton.addEventListener(
    "click",
    async function () {

        const testId =
            testSelect.value;


        // Make sure a test is selected

        if (!testId) {

            alert(
                "Please select a test case first."
            );

            return;

        }


        // Disable button

        runEvaluationButton.disabled =
            true;


        runEvaluationButton.textContent =
            "Running...";


        // Hide previous response

        evaluationResponseContainer.style.display =
            "none";


        try {

            // Send selected test to FastAPI

            const response =
                await fetch(
                    "/evaluation/run",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            test_id: testId
                        })
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "Evaluation request failed."
                );

            }


            const data =
                await response.json();


            // =================================================
            // SHOW ACTUAL GEMINI RESPONSE
            // =================================================

            evaluationResponseContainer.style.display =
                "block";


            evaluationResponse.textContent =
                data.actual_response;


            // =================================================
            // UPDATE TEST COUNT
            // =================================================

            testsRun++;


            testedCount.textContent =
                testsRun;


            // =================================================
            // IMPORTANT:
            // Do not automatically call the response
            // a hallucination.
            //
            // Day 16 requires actual response evaluation.
            // =================================================

            failureCount.textContent =
                failures;


            hallucinationCount.textContent =
                hallucinations;


            // =================================================
            // Scroll to response
            // =================================================

            evaluationResponseContainer.scrollIntoView({
                behavior: "smooth",
                block: "nearest"
            });

        }


        catch (error) {

            console.error(
                "Evaluation error:",
                error
            );


            alert(
                "Could not run the evaluation. Please make sure the FastAPI server is running."
            );

        }


        // Enable button

        runEvaluationButton.disabled =
            false;


        runEvaluationButton.textContent =
            "Run Evaluation";

    }
);


// =====================================================
// INITIALIZE EVALUATION
// =====================================================

loadEvaluationTests();