<script setup>
defineProps({
  msg: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="page-title">
    {{ msg }}
  </div>
</template>

<style scoped>
.page-title {
  font-size: 32px;
  color: rgba(255, 255, 255, 0.87);
  text-align: center;
  margin-bottom: 20px;
}
</style>
