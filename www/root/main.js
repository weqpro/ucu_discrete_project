import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Renderer setup
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0x000000);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

// Scene setup
const scene = new THREE.Scene();

// Camera setup
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
camera.position.set(4, 4, 11);

// OrbitControls setup
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.enablePan = false;
controls.minDistance = 5;
controls.maxDistance = 20;
controls.minPolarAngle = 0.2;
controls.maxPolarAngle = 1.5;
controls.autoRotate = true;
controls.target = new THREE.Vector3(0, 1, 0);
controls.update();

// Ground setup
const groundGeometry = new THREE.PlaneGeometry(20, 20, 32, 32);
groundGeometry.rotateX(-Math.PI / 2);
const groundMaterial = new THREE.MeshStandardMaterial({
  color: 0x555555,
  side: THREE.DoubleSide
});
const groundMesh = new THREE.Mesh(groundGeometry, groundMaterial);
groundMesh.castShadow = false;
groundMesh.receiveShadow = true;
scene.add(groundMesh);

// SpotLight setup
const spotLight = new THREE.SpotLight(0xffffff, 6000, 100, 0.22, 1);
spotLight.position.set(0, 25, 0);
spotLight.castShadow = false;
spotLight.shadow.bias = -0.0001;
scene.add(spotLight);

// Model loading
const loader = new GLTFLoader().setPath('./terrain/');
loader.load('sample_terrain2.glb', (gltf) => {
    console.log('Model loaded');
    const mesh = gltf.scene;
    mesh.rotation.set(-Math.PI / 2, 0, 0);
    mesh.scale.set(0.2, 0.2, 0.2);
    mesh.position.set(-2.5, 0, 2.5);
    mesh.traverse((child) => {
        if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
        }
    });
    scene.add(mesh);

    // Hide the progress container (ensure this exists in your HTML)
    const progressContainer = document.getElementById('progress-container');
    if (progressContainer) {
        progressContainer.style.display = 'none';
    }
});

// Window resize event listener
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();

// Drag-and-drop file upload logic
const dropArea = document.getElementById('drop-area');
let draggedFile = null;

// Variables to store text field values
let startX = null, startY = null, endX = null, endY = null, step = null;

// Attach event listeners to the text fields
document.getElementById('start-x').addEventListener('input', (e) => startX = parseFloat(e.target.value));
document.getElementById('start-y').addEventListener('input', (e) => startY = parseFloat(e.target.value));
document.getElementById('end-x').addEventListener('input', (e) => endX = parseFloat(e.target.value));
document.getElementById('end-y').addEventListener('input', (e) => endY = parseFloat(e.target.value));
document.getElementById('step').addEventListener('input', (e) => step = parseFloat(e.target.value));

dropArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropArea.classList.add('dragover');
});

dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('dragover');
});

// Server endpoint
const serverURL = "https://your-server-url.com/upload"; // Replace with your actual server endpoint

// Function to send the file to the server
function sendFileToServer(fileContent, fileName) {
    const dataToSend = {
        fileContent: fileContent,
        fileName: fileName,
    };

    fetch(serverURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dataToSend)
    })
        .then((response) => {
            if (response.ok) {
                console.log("File successfully uploaded!");
                return response.json();
            } else {
                console.error("Failed to upload file:", response.status, response.statusText);
            }
        })
        .catch((error) => {
            console.error("Error during file upload:", error);
        });
}

// Function to send coordinates and step to the server
function sendCoordinatesToServer(coordinates) {
    fetch(`${serverURL}/coordinates`, { // Use a different endpoint if needed
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(coordinates)
    })
        .then((response) => {
            if (response.ok) {
                console.log("Coordinates and step successfully uploaded!");
                return response.json();
            } else {
                console.error("Failed to upload coordinates:", response.status, response.statusText);
            }
        })
        .catch((error) => {
            console.error("Error during coordinates upload:", error);
        });
}

// Handle file drop
dropArea.addEventListener('drop', (event) => {
    event.preventDefault();
    dropArea.classList.remove('dragover');
    draggedFile = event.dataTransfer.files[0]; // Get the first file

    if (draggedFile) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const fileContent = e.target.result; // File content as text
            console.log("File content ready to send:", fileContent);

            // Send the file content to the server
            sendFileToServer(fileContent, draggedFile.name);
        };
        reader.readAsText(draggedFile); // Read the file as text
    }
});

// Handle coordinate submission
document.getElementById('send-coordinates-btn').addEventListener('click', () => {
    const coordinates = { startX, startY, endX, endY, step };

    if (Object.values(coordinates).some((val) => val === null || isNaN(val))) {
        alert("Please fill in all coordinates (startX, startY, endX, endY, step) before submitting.");
        return;
    }

    // Send the coordinates and step to the server
    sendCoordinatesToServer(coordinates);
});