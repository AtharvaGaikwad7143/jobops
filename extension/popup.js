const button = document.getElementById("detect-job");
const status = document.getElementById("status");

button.addEventListener("click", async () => {
    status.textContent = "Detecting...";

    const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    chrome.tabs.sendMessage(
        tab.id,
        { type: "GET_JOB" },
        (response) => {
            if (chrome.runtime.lastError) {
                status.textContent =
                    "Could not communicate with page.";

                console.error(
                    chrome.runtime.lastError.message
                );

                return;
            }

            if (!response?.success) {
                status.textContent =
                    response?.error || "Job not detected.";

                return;
            }

            console.log("JOB:", response.job);

            status.textContent =
                `Detected: ${response.job.title}`;
        }
    );
});