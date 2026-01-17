
const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const browseBtn = document.getElementById("browseBtn");
const uploadedFile = document.getElementById("uploadedFile");
const analyzeBtn = document.getElementById("analyzeBtn");
const featureColumn = document.getElementById("featureColumn");
const table = document.getElementById('table');
const colsElement = document.getElementById('columns');
const tbody = document.getElementById('tbody');

let file = null;
let filename = "";
let featureCol = "";

const ALLOWED_TYPES = [
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
];

function isValidFile(file) {
    const MAX_SIZE = 50 * 1024 * 1024; // 50MB in bytes
    return ALLOWED_TYPES.includes(file.type) && file.size <= MAX_SIZE;
}

function displayFileName(file) {
    if (!file || !uploadedFile) return;

    uploadedFile.classList.remove("hidden");
    uploadedFile.innerHTML = `
                <div class="flex items-center justify-between bg-gray-100 px-4 py-2 rounded">
                    <span class="text-sm text-gray-700 truncate">
                        📄 ${file.name}
                    </span>
                    <button
                        class="text-red-500 text-sm hover:underline"
                        onclick="removeFile()">
                        Remove
                    </button>
                </div>
            `;
}

function removeFile() {
    file = null;
    uploadedFile.classList.add("hidden");
    uploadedFile.innerHTML = "";
}

async function predictSentiment(file) {
    if (!file || !isValidFile(file)) {
        alert("Only CSV or Excel files are allowed!");
        return;
    }

    if (!featureColumn.value.trim()) {
        alert("Please enter the feature column name");
        return;
    }

    const formData = new FormData();
    formData.append("fileInput", file);
    formData.append("featureColumn", featureColumn.value);

    try {
        const res = await fetch("/analyze/file", {
            method: "POST",
            body: formData
        });

        // if (!res.ok) throw new Error("Upload failed");

        const data = await res.json();

        console.log(data);

        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = 'Analyze';

        generateTable(data.sentiment);

    } catch (err) {
        console.error(err);
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = 'Analyze';
    }
}

function generateTable(table) {
    if (table) {
        console.log(table);
        // table.classList.add('border');
    }

    for (const col of Object.keys(table[0])) {
        const heading = document.createElement('th');
        heading.innerText = col;

        colsElement.appendChild(heading);
    }

    for (const row of table) {
        const rowElement = document.createElement('tr');
        rowElement.classList.add(row.sentiment);

        for (const col of Object.values(row)) {
            const cell = document.createElement('td');
            cell.innerText = col;

            rowElement.appendChild(cell);
        }
        tbody.appendChild(rowElement);
    }
}

featureColumn.addEventListener('input', (e) => {
    featureCol = e.target.value;
})

browseBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", (e) => {
    const f = e.target.files[0];
    if (!f) return;

    if (!isValidFile(f)) {
        alert("Invalid file type");
        return;
    }

    file = f;
    displayFileName(file);
    fileInput.value = "";
});

analyzeBtn.onclick = () => {
    if (!file) {
        alert("No file uploaded");
        return;
    }

    colsElement.innerHTML = "";
    tbody.innerHTML = "";

    predictSentiment(file);
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = 'Analyzing...'
};

/* Drag and Drop Functionality */

uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("border-blue-500", "bg-blue-50");
});

uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("border-blue-500", "bg-blue-50");
});

uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("border-blue-500", "bg-blue-50");

    const f = e.dataTransfer.files[0];
    if (!f || !isValidFile(f)) {
        alert("Invalid file type or the file exceeds size of 50MB");
        return;
    }

    file = f;
    displayFileName(file);
});

/* Paste Functionality */

document.addEventListener("paste", (e) => {
    const items = e.clipboardData.items;

    for (let i = 0; i < items.length; i++) {
        if (items[i].kind === "file") {
            const f = items[i].getAsFile();
            if (!isValidFile(f)) {
                alert("Invalid file type");
                return;
            }
            file = f;
            displayFileName(file);
            break;
        }
    }
});