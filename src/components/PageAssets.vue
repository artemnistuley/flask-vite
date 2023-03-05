<script setup>
import viteLogo from '@/assets/icons/vite.svg';
</script>

<template>
  <div class="page-assets">
    <img :src="viteLogo" class="logo" alt="Vite logo" />
    <img src="/src/assets/icons/vue.svg" class="logo vue" alt="Vue logo" />
  </div>
</template>

<style scoped>
.page-assets {
  display: flex;
  justify-content: center;
  gap: 10px;
}
</style>
