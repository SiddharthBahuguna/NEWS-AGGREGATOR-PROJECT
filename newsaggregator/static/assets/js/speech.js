let synth = window.speechSynthesis;
let currentUtterance = null;

function startReadAloud(url) {
    if (synth.speaking) {
        synth.cancel();
    }

    console.log("Fetching article from URllL:", url);

    fetch(`/fetch_article_content/?url=${encodeURIComponent(url)}`)
        .then(response => {
            console.log("Response status:", response.status);
            if (!response.ok) {
                throw new Error("Network response was not ok " + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            console.log("Fetched data successfully");
            const parser = new DOMParser();
            const doc = parser.parseFromString(data.content, 'text/html');
            const articleElement = doc.querySelector('.sc-77igqf-0.fnnahv'); // Updated selector to match your article content
            if (!articleElement) {
                throw new Error("Article content not found");
            }
            const articleContent = articleElement.innerText;

            console.log("Article content extracted:", articleContent);
            currentUtterance = new SpeechSynthesisUtterance(articleContent);
            synth.speak(currentUtterance);
        })
        .catch(error => {
            console.error('Error fetching article content:', error);
        });
}

function pauseReadAloud(button) {
    console.log("eeee")
    if (synth.speaking && !synth.paused) {
        synth.pause();
        button.innerText = "Resume";
    } else if (synth.paused) {
        synth.resume();
        button.innerText = "Pause";
    }
}

function stopReadAloud() {
    if (synth.speaking) {
        synth.cancel();
        const pauseButton = document.getElementById('pause-resume-btn');
        if (pauseButton) {
            pauseButton.innerText = "Pause";
        }
    }
}