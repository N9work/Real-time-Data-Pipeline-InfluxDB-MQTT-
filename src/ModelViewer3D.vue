<template>
  <div ref="container" class="viewer">
    <div v-if="loading" class="overlay">Loading 3D model…</div>
    <canvas ref="canvas"></canvas>
    <div class="hud">
      <button @click="toggleAutoRotate">{{ autoRotate ? '⏸ Stop' : '▶️ Auto-rotate' }}</button>
      <button @click="resetView">🔄 Reset view</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'

const props = defineProps({
  modelUrl: { type: String, required: true },
  distance: { type: Number, default: 3 },
})

const container = ref(null)
const canvas = ref(null)

let renderer, scene, camera, controls, animationId
let modelRoot

const raycaster = new THREE.Raycaster()
const mouse = new THREE.Vector2()

const loading = ref(true)
const autoRotate = ref(false)

function fitCameraToObject(object, offset = 1.25) {
  const box = new THREE.Box3().setFromObject(object)
  const size = new THREE.Vector3()
  const center = new THREE.Vector3()
  box.getSize(size)
  box.getCenter(center)

  const maxDim = Math.max(size.x, size.y, size.z)
  const fov = THREE.MathUtils.degToRad(camera.fov)
  let camZ = Math.abs(maxDim / (2 * Math.tan(fov / 2))) * offset

  camZ = Math.max(camZ, props.distance)
  camera.position.set(center.x + camZ, center.y + camZ * 0.2, center.z + camZ)
  camera.near = camZ / 100
  camera.far = camZ * 100
  camera.updateProjectionMatrix()
  controls.target.copy(center)
  controls.update()
}

function addLights(scene) {
  const hemi = new THREE.HemisphereLight(0xffffff, 0x444444, 1.1)
  hemi.position.set(0, 1, 0)
  scene.add(hemi)

  const dir = new THREE.DirectionalLight(0xffffff, 1.0)
  dir.position.set(5, 10, 7)
  dir.castShadow = true
  scene.add(dir)
}

function animate() {
  animationId = requestAnimationFrame(animate)
  if (controls) {
    controls.autoRotate = autoRotate.value
    controls.update()
  }
  renderer.render(scene, camera)
}

function onResize() {
  if (!container.value) return
  const { clientWidth: w, clientHeight: h } = container.value
  camera.aspect = w / h
  camera.updateProjectionMatrix()
  renderer.setSize(w, h, true)
  renderer.setPixelRatio(window.devicePixelRatio)
}

function toggleAutoRotate() {
  autoRotate.value = !autoRotate.value
}

function resetView() {
  if (modelRoot) fitCameraToObject(modelRoot, 1.4)
}

async function loadModel(url) {
  const loader = new GLTFLoader()
  return new Promise((resolve, reject) => {
    loader.load(url, (gltf) => resolve(gltf.scene), undefined, (err) => reject(err))
  })
}

// ✅ คลิกตรวจจับ object
function onClick(event) {
  if (!container.value) return

  const rect = renderer.domElement.getBoundingClientRect()
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1

  raycaster.setFromCamera(mouse, camera)
  const intersects = raycaster.intersectObjects(scene.children, true)

  if (intersects.length > 0) {
    const object = intersects[0].object
    if (object.userData.url) {
      window.open(object.userData.url, "_blank")
    } else {
      console.log("คลิก object แต่ไม่มี URL:", object.name)
    }
  }
}

onMounted(async () => {
  // Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true, canvas: canvas.value })
  renderer.outputColorSpace = THREE.SRGBColorSpace
  renderer.physicallyCorrectLights = true
  renderer.shadowMap.enabled = true

  // Scene & Camera
  scene = new THREE.Scene()
  scene.background = new THREE.Color('#CCF1FF')

  const { clientWidth: w, clientHeight: h } = container.value
  camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 1000)
  camera.position.set(0, 1, props.distance)

  // Controls
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.06
  controls.enablePan = true
  controls.enableZoom = true
  controls.minDistance = 0.3
  controls.maxDistance = 100
  controls.autoRotateSpeed = 1.5

  addLights(scene)

  try {
    modelRoot = await loadModel(props.modelUrl)
    // 🟢 กำหนด URL ให้ Mesh ที่ต้องการ
    modelRoot.traverse((obj) => {
      if (obj.isMesh) {
        // ตัวอย่าง: คลิกแล้วไป Google
        if (obj.name === "LCD-material") obj.userData.url = "http://localhost:3000/d/d4bf7ca1-57f9-46b7-9aa8-3c25daadc4b7/sensor-monitoring?orgId=1&from=now-15m&to=now&timezone=browser&refresh=auto"
      }
    })
    scene.add(modelRoot)
    fitCameraToObject(modelRoot, 1.6)
  } catch (e) {
    console.error('Failed to load model:', e)
    const geom = new THREE.TorusKnotGeometry(0.6, 0.22, 150, 20)
    const mat = new THREE.MeshStandardMaterial({ metalness: 0.4, roughness: 0.3 })
    modelRoot = new THREE.Mesh(geom, mat)
    scene.add(modelRoot)
    fitCameraToObject(modelRoot, 2.0)
  } finally {
    loading.value = false
  }

  onResize()
  window.addEventListener('resize', onResize)
  renderer.domElement.addEventListener('click', onClick) 
  animate()
})

onBeforeUnmount(() => {
  cancelAnimationFrame(animationId)
  window.removeEventListener('resize', onResize)
  renderer.domElement.removeEventListener('click', onClick)
  if (renderer) renderer.dispose()
  if (controls) controls.dispose()
})
</script>

<style scoped>
.viewer {
  position: relative;
  width: 100%;
  height: 70vh;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}
canvas {
  display: block;
  width: 100%;
  height: 100%;
}
.overlay {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  font-weight: 600;
  letter-spacing: 0.2px;
  background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(0,0,0,0.1));
  z-index: 2;
  backdrop-filter: blur(2px);
}
.hud {
  position: absolute;
  bottom: 12px;
  left: 12px;
  display: flex;
  gap: 8px;
  z-index: 3;
}
.hud button {
  background: rgba(0, 0, 0, 0.85);
  border: 0;
  padding: 8px 12px;
  border-radius: 999px;
  font-weight: 600;
  cursor: pointer;
}
.hud button:hover {
  background: rgb(74, 74, 74);
}
</style>
