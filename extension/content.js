function detectSite() {
    const hostname = window.location.hostname;

    if (hostname.includes("linkedin.com")) {
        return "linkedin";
    }

    if (hostname.includes("naukri.com")) {
        return "naukri";
    }

    return "unknown";
}


function detectJobPage() {
    const site = detectSite();
    const url = window.location.href;

    if (
        site === "linkedin" &&
        url.includes("/jobs/view/")
    ) {
        return true;
    }

    if (
        site === "naukri" &&
        url.includes("/job-listings-")
    ) {
        return true;
    }

    return false;
}


function extractBasicJobData() {
    return {
        title: document.title,
        location: "",
        description: document.body.innerText,
        source: detectSite(),
        source_url: window.location.href,
        company: 3
    };
}


console.log("JobOps loaded");
console.log("Site:", detectSite());


if (detectJobPage()) {
    console.log("Job detected!");

    const job = extractBasicJobData();

    console.log("Detected job:", job);
} else {
    console.log("Not a supported job page");
}


chrome.runtime.onMessage.addListener(
    (message, sender, sendResponse) => {

        if (message.type === "GET_JOB") {

            if (!detectJobPage()) {
                sendResponse({
                    success: false,
                    error: "Not a supported job page"
                });

                return;
            }

            sendResponse({
                success: true,
                job: extractBasicJobData()
            });
        }
    }
);