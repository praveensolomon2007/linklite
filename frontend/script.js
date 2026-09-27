const urlInput = document.getElementById("urlInput");
const shortenButton = document.getElementById("shortenButton");
const result = document.getElementById("result");

shortenButton.addEventListener("click", shortenUrl);

async function shortenUrl() {
    const url = urlInput.value.trim();

    if (!url) {
        result.textContent = "Please enter a URL.";
        return;
    }

    result.textContent = "Creating short URL...";

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/shorten",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    url: url
                })
            }
        );

        const data = await response.json();

        result.innerHTML = `
            <p>Your shortened URL:</p>
            <a href="${data.short_url}" target="_blank">
                ${data.short_url}
            </a>
        `;

    } catch (error) {
        result.textContent = "Could not connect to the API.";
        console.error(error);
    }
}