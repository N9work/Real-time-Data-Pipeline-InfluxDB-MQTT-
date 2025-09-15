<script setup>
import ModelViewer3D from './ModelViewer3D.vue'
</script>

<template>
  <div style="padding:16px">
    <h1>Smart Cozy Room ...</h1>
    <!-- ใช้ไฟล์โมเดลจาก public/models/robot.glb -->
    <ModelViewer3D model-url="models/room_update2.glb" :distance="4" />
  </div>
</template>
