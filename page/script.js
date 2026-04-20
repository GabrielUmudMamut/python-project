const API_BASE = "http://127.0.0.1:8000";
const outputBox = document.getElementById("output-box");
const formattedBox = document.getElementById("formatted-output"); // Get the new box

async function fetchData(endpoint) {
    // 1. Set loading states
    outputBox.innerText = "Processing request...";
    formattedBox.innerHTML = "<em>Loading...</em>";
    formattedBox.className = ""; // Clear any success/error colors

    try {
        const response = await fetch(API_BASE + endpoint);
        const data = await response.json();
        
        // 2. Put raw JSON in the old box
        outputBox.innerText = JSON.stringify(data, null, 2);

        // 3. Format the new "Good Looking" box based on success/error
        if (data.status === "success") {
            formattedBox.classList.add("status-success"); // Makes it green
            
            // Check if this is the storage endpoint (which has different data)
            if (data.total_GB) {
                formattedBox.innerHTML = `
                    <strong>💾 Storage Status</strong>
                    <div class="storage-stats">
                        Total Space: ${data.total_GB} GB<br>
                        Used Space: ${data.used_GB} GB<br>
                        <strong>Free Space: ${data.free_GB} GB</strong>
                    </div>
                `;
            } else {
                // Normal success message for open/close/install
                formattedBox.innerHTML = `<strong>✅ Success!</strong><br><br>${data.message}`;
            }

        } else if (data.status === "error") {
            formattedBox.classList.add("status-error"); // Makes it red
            formattedBox.innerHTML = `<strong>❌ Error!</strong><br><br>${data.message}`;
        }

    } catch (error) {
        // Handle server crash or connection issues
        outputBox.innerText = "Error: " + error.message;
        formattedBox.className = "status-error";
        formattedBox.innerHTML = `<strong>🔌 Connection Failed!</strong><br><br>Make sure your Python server is running and the EULA is accepted.`;
    }
}

function installGame() {
    const gameId = document.getElementById("gameId").value;
    if (!gameId) return alert("Please enter a Game ID");
    fetchData('/si/' + gameId);
}

function uninstallGame() {
    const gameId = document.getElementById("gameId").value;
    if (!gameId) return alert("Please enter a Game ID");
    fetchData('/uninstall/' + gameId);
}

async function takeScreenshot() {
    outputBox.innerText = "Capturing screenshot...";
    formattedBox.innerHTML = "<em>Taking picture...</em>";
    formattedBox.className = "";
    
    const imgElement = document.getElementById("screenshot-display");
    imgElement.style.display = "none"; 

    try {
        const response = await fetch(API_BASE + '/screenshot');
        if (!response.ok) throw new Error("Failed to load image");
        
        const imageBlob = await response.blob();
        const imageObjectURL = URL.createObjectURL(imageBlob);
        
        imgElement.src = imageObjectURL;
        imgElement.style.display = "block";
        
        outputBox.innerText = "Screenshot captured successfully!";
        formattedBox.classList.add("status-success");
        formattedBox.innerHTML = `<strong>📸 Screenshot Captured!</strong><br><br>Image is displayed up there ^.`;
        
    } catch (error) {
        outputBox.innerText = "Screenshot Error: " + error.message;
        formattedBox.classList.add("status-error");
        formattedBox.innerHTML = `<strong>❌ Screenshot Failed!</strong><br><br>${error.message}`;
    }
}