// // Main JavaScript for AgriDetect Application

document.addEventListener("DOMContentLoaded", function () {
  // DOM Elements
  const fileInput = document.getElementById("file-input");
  const dropZone = document.getElementById("drop-zone");
  const imagePreview = document.getElementById("image-preview");
  const previewContainer = document.getElementById("preview-container");
  const analyzeBtn = document.getElementById("analyze-btn");
  const resultsContainer = document.getElementById("results-container");
  const loadingModal = document.getElementById("loading-modal");
  const uploadTab = document.getElementById("upload-tab");
  const cameraTab = document.getElementById("camera-tab");
  const datasetTab = document.getElementById("dataset-tab");
  const uploadArea = document.getElementById("upload-area");
  const cameraContainer = document.getElementById("camera-container");
  const datasetContainer = document.getElementById("dataset-container");
  const newAnalysisBtn = document.getElementById("new-analysis");

  // Current state
  let currentImage = null;
  let currentImageFile = null;

  // Tab Switching
  uploadTab.addEventListener("click", () => switchTab("upload"));
  cameraTab.addEventListener("click", () => switchTab("camera"));
  datasetTab.addEventListener("click", () => switchTab("dataset"));

  // File input change handler
  fileInput.addEventListener("change", handleFileSelect);

  // Drag and drop functionality
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "#2e7d32";
    dropZone.style.background = "#f0f7f0";
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.style.borderColor = "#ddd";
    dropZone.style.background = "#f8f9fa";
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.style.borderColor = "#ddd";
    dropZone.style.background = "#f8f9fa";

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  });

  // Click to upload
  dropZone.addEventListener("click", () => {
    fileInput.click();
  });

  // Analyze button click
  analyzeBtn.addEventListener("click", analyzeImage);

  // New analysis button
  if (newAnalysisBtn) {
    newAnalysisBtn.addEventListener("click", resetAnalysis);
  }

  // Remove button
  document
    .getElementById("remove-btn")
    ?.addEventListener("click", resetAnalysis);

  // Load dataset items
  loadDatasetItems();

  // Search dataset
  const datasetSearch = document.getElementById("dataset-search");
  if (datasetSearch) {
    datasetSearch.addEventListener("input", filterDatasetItems);
  }

  // Functions
  function switchTab(tabName) {
    // Update active tab
    document.querySelectorAll(".upload-option").forEach((opt) => {
      opt.classList.remove("active");
    });

    if (tabName === "upload") {
      uploadTab.classList.add("active");
      uploadArea.style.display = "block";
      cameraContainer.style.display = "none";
      datasetContainer.style.display = "none";
    } else if (tabName === "camera") {
      cameraTab.classList.add("active");
      uploadArea.style.display = "none";
      cameraContainer.style.display = "block";
      datasetContainer.style.display = "none";
      initializeCamera();
    } else if (tabName === "dataset") {
      datasetTab.classList.add("active");
      uploadArea.style.display = "none";
      cameraContainer.style.display = "none";
      datasetContainer.style.display = "block";
    }
  }

  function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
      handleFile(file);
    }
  }

  function handleFile(file) {
    // Validate file type
    const validTypes = ["image/jpeg", "image/png", "image/jpg", "image/webp"];
    if (!validTypes.includes(file.type)) {
      showNotification(
        "Please upload a valid image file (JPEG, PNG, WEBP)",
        "error"
      );
      return;
    }

    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
      showNotification("File size must be less than 16MB", "error");
      return;
    }

    currentImageFile = file;

    // Create object URL for preview
    const objectUrl = URL.createObjectURL(file);
    imagePreview.src = objectUrl;

    // Update preview info
    document.getElementById("preview-filename").textContent = file.name;
    document.getElementById(
      "preview-size"
    ).textContent = `Size: ${formatFileSize(file.size)}`;

    // Show preview container
    previewContainer.style.display = "block";

    // Hide results if any
    resultsContainer.style.display = "none";
  }

  async function analyzeImage() {
    if (!currentImageFile) {
      showNotification("Please select an image first", "warning");
      return;
    }

    // Show loading modal
    loadingModal.style.display = "flex";

    try {
      // Create FormData
      const formData = new FormData();
      formData.append("file", currentImageFile);

      // Send to server
      const response = await fetch("/predict", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        displayResults(data);
      } else {
        throw new Error(data.error || "Analysis failed");
      }
    } catch (error) {
      console.error("Error:", error);
      showNotification(`Analysis failed: ${error.message}`, "error");
    } finally {
      // Hide loading modal
      loadingModal.style.display = "none";
    }
  }

  function displayResults(data) {
    // Update results
    document.getElementById("disease-name").textContent = formatDiseaseName(
      data.disease
    );
    document.getElementById("confidence-badge").textContent = `${(
      data.confidence * 100
    ).toFixed(2)}% Confidence`;

    // Update disease information
    if (data.info) {
      document.getElementById("symptoms-text").textContent = data.info.symptoms;
      document.getElementById("treatment-text").textContent =
        data.info.treatment;
      document.getElementById("prevention-text").textContent =
        data.info.prevention;
      document.getElementById("chemical-control").textContent =
        data.info.chemical_control;
      document.getElementById("organic-control").textContent =
        data.info.organic_control;
    }

    // Show results container
    resultsContainer.style.display = "block";

    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: "smooth" });
  }

  function resetAnalysis() {
    // Reset file input
    fileInput.value = "";

    // Clear preview
    imagePreview.src = "";
    previewContainer.style.display = "none";

    // Hide results
    resultsContainer.style.display = "none";

    // Reset current image
    currentImage = null;
    currentImageFile = null;

    // Switch to upload tab
    switchTab("upload");
  }

  async function loadDatasetItems() {
    try {
      const response = await fetch("/get_diseases");
      const data = await response.json();

      if (response.ok) {
        displayDatasetItems(data.diseases);
      }
    } catch (error) {
      console.error("Error loading dataset:", error);
    }
  }

  function displayDatasetItems(diseases) {
    const datasetGrid = document.getElementById("dataset-grid");
    if (!datasetGrid) return;

    datasetGrid.innerHTML = "";

    diseases.forEach((disease) => {
      const item = document.createElement("div");
      item.className = "dataset-item";
      item.innerHTML = `
                <i class="fas fa-leaf"></i>
                <h5>${formatDiseaseName(disease)}</h5>
                <p>Click to select sample</p>
            `;

      item.addEventListener("click", () => {
        // In a real application, you would load a sample image from the dataset
        showNotification(
          "Sample image selection from dataset would be implemented here",
          "info"
        );
      });

      datasetGrid.appendChild(item);
    });
  }

  function filterDatasetItems() {
    const searchTerm = datasetSearch.value.toLowerCase();
    const items = document.querySelectorAll(".dataset-item");

    items.forEach((item) => {
      const diseaseName = item.querySelector("h5").textContent.toLowerCase();
      if (diseaseName.includes(searchTerm)) {
        item.style.display = "block";
      } else {
        item.style.display = "none";
      }
    });
  }

  function formatDiseaseName(disease) {
    return disease
      .replace(/_/g, " ")
      .replace(/([A-Z])/g, " $1")
      .trim();
  }

  function formatFileSize(bytes) {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  }

  function showNotification(message, type = "info") {
    // Create notification element
    const notification = document.createElement("div");
    notification.className = `notification ${type}`;
    notification.innerHTML = `
            <i class="fas fa-${getIconForType(type)}"></i>
            <span>${message}</span>
            <button class="close-notification">&times;</button>
        `;

    // Add to document
    document.body.appendChild(notification);

    // Add close functionality
    notification
      .querySelector(".close-notification")
      .addEventListener("click", () => {
        notification.remove();
      });

    // Auto-remove after 5 seconds
    setTimeout(() => {
      if (notification.parentNode) {
        notification.remove();
      }
    }, 5000);
  }

  function getIconForType(type) {
    switch (type) {
      case "success":
        return "check-circle";
      case "error":
        return "exclamation-circle";
      case "warning":
        return "exclamation-triangle";
      default:
        return "info-circle";
    }
  }

  // Add notification styles
  const style = document.createElement("style");
  style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            color: white;
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 1002;
            animation: slideIn 0.3s ease;
            max-width: 400px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .notification.success { background: var(--success-color); }
        .notification.error { background: var(--danger-color); }
        .notification.warning { background: var(--warning-color); }
        .notification.info { background: var(--info-color); }

        .close-notification {
            background: none;
            border: none;
            color: white;
            font-size: 1.2rem;
            cursor: pointer;
            margin-left: auto;
            padding: 0;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
  document.head.appendChild(style);
});
