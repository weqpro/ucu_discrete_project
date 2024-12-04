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

dropArea.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropArea.classList.add('dragover');
});

dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('dragover');
});

dropArea.addEventListener('drop', (event) => {
    event.preventDefault();
    dropArea.classList.remove('dragover');
    draggedFile = event.dataTransfer.files[0]; // Get the first file
    if (draggedFile) {
        alert(`File ready to upload: ${draggedFile.name}`);
    }
});

// Send coordinates and step to the server
function sendCoordinatesToServer(startX, startY, endX, endY, step) {
    const url = "http://127.0.0.1:1234/init-info"; // Make sure this matches your server URL
    const data = { startX, startY, endX, endY, step };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Coordinates successfully sent:", data);
    })
    .catch(error => {
        console.error("Error during coordinate upload:", error);
    });
}

// Add event listeners for input fields to capture coordinate and step changes
const startXInput = document.getElementById('start-x');
const startYInput = document.getElementById('start-y');
const endXInput = document.getElementById('end-x');
const endYInput = document.getElementById('end-y');
const stepInput = document.getElementById('step');

let startX = 0, startY = 0, endX = 0, endY = 0, step = 0;

startXInput.addEventListener('input', (e) => { startX = e.target.value; });
startYInput.addEventListener('input', (e) => { startY = e.target.value; });
endXInput.addEventListener('input', (e) => { endX = e.target.value; });
endYInput.addEventListener('input', (e) => { endY = e.target.value; });
stepInput.addEventListener('input', (e) => { step = e.target.value; });

// Button to send the data to the server
const sendDataButton = document.getElementById('send-coordinates-btn');
sendDataButton.addEventListener('click', () => {
    sendCoordinatesToServer(startX, startY, endX, endY, step);
});
