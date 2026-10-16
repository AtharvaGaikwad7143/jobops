let currentJob = null;

const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");

const loginButton = document.getElementById("login");
const detectButton = document.getElementById("detect-job");
const saveButton = document.getElementById("save-job");

const status = document.getElementById("status");


async function login() {
    const username = usernameInput.value.trim();
    const password = passwordInput.value;

    if (!username || !password) {
        status.textContent = "Enter username and password.";
        return;
    }

    status.textContent = "Logging in...";

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/auth/login/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            console.error("LOGIN ERROR:", data);

            status.textContent =
                data.detail || "Login failed.";

            return;
        }

        await chrome.storage.local.set({
            accessToken: data.access,
            refreshToken: data.refresh
        });

        status.textContent = "Logged in.";

        console.log("Login successful");

    } catch (error) {
        console.error("LOGIN ERROR:", error);

        status.textContent =
            "Could not connect to backend.";
    }
}


async function getAccessToken() {
    const data = await chrome.storage.local.get(
        ["accessToken"]
    );

    return data.accessToken;
}


async function saveJob(job) {
    const accessToken = await getAccessToken();

    if (!accessToken) {
        throw new Error("NOT_LOGGED_IN");
    }

    const response = await fetch(
        "http://127.0.0.1:8000/api/jobs/",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${accessToken}`
            },

            body: JSON.stringify(job)
        }
    );

    const data = await response.json();

    if (!response.ok) {
        console.error("SAVE JOB ERROR:", data);

        throw new Error(
            data.detail || `Backend returned ${response.status}`
        );
    }

    return data;
}


loginButton.addEventListener("click", async () => {
    await login();
});


detectButton.addEventListener("click", async () => {
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

            currentJob = response.job;

            console.log("JOB:", currentJob);

            status.textContent =
                `Detected: ${currentJob.title || "Job"}`;
        }
    );
});


saveButton.addEventListener("click", async () => {

    if (!currentJob) {
        status.textContent =
            "Detect a job first.";

        return;
    }

    status.textContent = "Saving...";

    try {

        const savedJob = await saveJob(currentJob);

        console.log("SAVED JOB:", savedJob);

        status.textContent =
            `Saved: ${savedJob.title}`;

    } catch (error) {

        console.error("SAVE ERROR:", error);

        if (error.message === "NOT_LOGGED_IN") {
            status.textContent =
                "Login first.";
        } else {
            status.textContent =
                `Failed: ${error.message}`;
        }
    }
});