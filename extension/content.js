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


/* =========================================
   APPLICATION DETECTION
========================================= */


function findApplyButtons() {
    const elements = document.querySelectorAll(
        "button, a"
    );

    return Array.from(elements).filter((element) => {
        const text = element.innerText
            ?.trim()
            .toLowerCase();

        if (!text) {
            return false;
        }

        return (
            text === "apply" ||
            text.includes("apply now") ||
            text.includes("easy apply")
        );
    });
}


function createApplicationSignal(button) {
    return {
        type: "APPLICATION_SIGNAL",
        signal: "APPLY_CLICK",
        source: detectSite(),
        job_url: window.location.href,
        timestamp: new Date().toISOString(),
        button_text: button.innerText?.trim() || ""
    };
}


function handleApplyClick(button) {
    const signal = createApplicationSignal(button);

    console.log(
        "Possible application started"
    );

    console.log(
        "APPLICATION_SIGNAL:",
        signal
    );
}


function attachApplyListeners() {
    const buttons = findApplyButtons();

    console.log(
        "Apply buttons found:",
        buttons.length
    );

    buttons.forEach((button) => {

        if (button.dataset.jobopsObserved === "true") {
            return;
        }

        button.dataset.jobopsObserved = "true";

        button.addEventListener(
            "click",
            () => {
                handleApplyClick(button);
            }
        );

        console.log(
            "Apply listener attached:",
            button.innerText?.trim()
        );
    });
}


/* =========================================
   DOM OBSERVER
========================================= */


const observer = new MutationObserver(() => {
    attachApplyListeners();
});


observer.observe(document.body, {
    childList: true,
    subtree: true
});


/* =========================================
   INITIALIZATION
========================================= */


console.log("JobOps loaded");
console.log("Site:", detectSite());


if (detectJobPage()) {
    console.log("Job detected!");

    const job = extractBasicJobData();

    console.log(
        "Detected job:",
        job
    );

    attachApplyListeners();
} else {
    console.log(
        "Not a supported job page"
    );
}


/* =========================================
   POPUP COMMUNICATION
========================================= */


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