// Camera functionality for AgriDetect

class CameraHandler {
  constructor() {
    this.videoElement = document.getElementById("camera-preview");
    this.canvasElement = document.getElementById("capture-canvas");
    this.captureButton = document.getElementById("capture-btn");
    this.switchCameraButton = document.getElementById("switch-camera");
    this.stream = null;
    this.facingMode = "environment"; // Start with back camera
    this.initialized = false;

    this.init();
  }

  async init() {
    if (this.initialized) return;

    // Event listeners
    if (this.captureButton) {
      this.captureButton.addEventListener("click", () => this.captureImage());
    }

    if (this.switchCameraButton) {
      this.switchCameraButton.addEventListener("click", () =>
        this.switchCamera()
      );
    }

    this.initialized = true;
  }

  async startCamera() {
    try {
      // Stop existing stream if any
      if (this.stream) {
        this.stopCamera();
      }

      // Get camera stream
      this.stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: this.facingMode,
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
        audio: false,
      });

      // Set video source
      this.videoElement.srcObject = this.stream;

      // Play video
      await this.videoElement.play();
    } catch (error) {
      console.error("Error accessing camera:", error);
      this.showCameraError(error);
    }
  }

  stopCamera() {
    if (this.stream) {
      this.stream.getTracks().forEach((track) => track.stop());
      this.stream = null;
    }
    if (this.videoElement) {
      this.videoElement.srcObject = null;
    }
  }

  async switchCamera() {
    this.facingMode =
      this.facingMode === "environment" ? "user" : "environment";
    await this.startCamera();
  }

  captureImage() {
    if (!this.stream) return;

    // Set canvas dimensions to match video
    this.canvasElement.width = this.videoElement.videoWidth;
    this.canvasElement.height = this.videoElement.videoHeight;

    // Draw current video frame to canvas
    const context = this.canvasElement.getContext("2d");
    context.drawImage(this.videoElement, 0, 0);

    // Convert canvas to blob
    this.canvasElement.toBlob(
      (blob) => {
        if (blob) {
          // Create file from blob
          const file = new File([blob], "camera-capture.jpg", {
            type: "image/jpeg",
            lastModified: Date.now(),
          });

          // Handle the captured image
          this.handleCapturedImage(file);
        }
      },
      "image/jpeg",
      0.9
    );
  }

  handleCapturedImage(file) {
    // This would integrate with the main file handling system
    console.log("Image captured:", file);

    // Show preview (integrate with main.js)
    if (window.handleFile) {
      window.handleFile(file);
    }

    // Stop camera after capture
    this.stopCamera();

    // Switch to upload tab
    if (window.switchTab) {
      window.switchTab("upload");
    }
  }

  showCameraError(error) {
    let message = "Camera access error: ";

    switch (error.name) {
      case "NotAllowedError":
        message +=
          "Camera access was denied. Please allow camera access in your browser settings.";
        break;
      case "NotFoundError":
        message += "No camera found on this device.";
        break;
      case "NotReadableError":
        message += "Camera is already in use by another application.";
        break;
      default:
        message += error.message;
    }

    alert(message);
  }
}

// Initialize camera when camera tab is active
let cameraHandler = null;

function initializeCamera() {
  if (!cameraHandler) {
    cameraHandler = new CameraHandler();
  }

  // Check if camera is supported
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert(
      "Camera API is not supported in your browser. Please use Chrome, Firefox, or Safari."
    );
    return;
  }

  // Start camera
  cameraHandler.startCamera();
}

// Stop camera when leaving camera tab
function stopCamera() {
  if (cameraHandler) {
    cameraHandler.stopCamera();
  }
}

// Make functions available globally
window.initializeCamera = initializeCamera;
window.stopCamera = stopCamera;
