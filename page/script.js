// --- DYNAMIC CACHE BUSTER ---
(function() {
    const v = Date.now(); // The "datenow thing" to fix the favicon
    
    // 1. Force Favicon update
    const favicon = document.getElementById('favicon-link');
    if (favicon) favicon.href = `/assets/favicon.ico?v=${v}`;
    
    // 2. Force CSS update
    const theme = document.getElementById('theme-link');
    if (theme) theme.href = `/page/style.css?v=${v}`;
    
    // 3. Force this script to update on next reload
    const script = document.getElementById('main-script');
    if (script) script.src = `/page/script.js?v=${v}`;

    console.log("Cache busted with version: " + v);
})();

// --- APP LOGIC ---
const API_BASE = ""; // Leaving this empty makes it work on any server (not just localhost)
const outputBox = document.getElementById("output-box");
const formattedBox = document.getElementById("formatted-output");

async function fetchData(endpoint) {
    outputBox.innerText = "Processing request...";
    formattedBox.innerHTML = "<em>Loading...</em>";
    formattedBox.className = ""; 

    try {
        // Add ?v= to API calls too so the JSON data is always fresh
        const response = await fetch(`${API_BASE}${endpoint}?v=${Date.now()}`);
        const data = await response.json();
        
        outputBox.innerText = JSON.stringify(data, null, 2);

        if (data.status === "success") {
            formattedBox.classList.add("status-success");
            if (data.total_GB) {
                formattedBox.innerHTML = `<strong>💾 Storage Status</strong><br>Total: ${data.total_GB}GB | Free: ${data.free_GB}GB`;
            } else {
                formattedBox.innerHTML = `<strong>✅ Success!</strong><br>${data.message}`;
            }
        } else {
            formattedBox.classList.add("status-error");
            formattedBox.innerHTML = `<strong>❌ Error!</strong><br>${data.message}`;
        }
    } catch (error) {
        formattedBox.className = "status-error";
        formattedBox.innerHTML = `<strong>🔌 Connection Failed!</strong>`;
    }
}

function installGame() {
    const id = document.getElementById("gameId").value;
    if (id) fetchData('/si/' + id);
}

function uninstallGame() {
    const id = document.getElementById("gameId").value;
    if (id) fetchData('/uninstall/' + id);
}

async function takeScreenshot() {
    const imgElement = document.getElementById("screenshot-display");
    imgElement.style.display = "none"; 
    try {
        // Add ?v= to the screenshot so you don't keep seeing the old image
        const response = await fetch(`${API_BASE}/screenshot?v=${Date.now()}`);
        const imageBlob = await response.blob();
        imgElement.src = URL.createObjectURL(imageBlob);
        imgElement.style.display = "block";
        formattedBox.className = "status-success";
        formattedBox.innerHTML = `<strong>📸 Screenshot Captured!</strong>`;
    } catch (e) {
        formattedBox.className = "status-error";
        formattedBox.innerHTML = `<strong>❌ Screenshot Failed!</strong>`;
    }
}