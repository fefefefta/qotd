<template>
  <transition name="fade">
    <div v-if="isVisible" class="fixed top-4 right-0 m-4 sm:right-4 z-50 p-4 bg-primary text-white rounded-lg shadow-lg flex items-center">
      <div class="mr-2">👋 Привет!</div>
      <div>Тебе было присвоено имя <strong>{{ name }}</strong></div>
      <button @click="$emit('hide')" class="ml-4 bg-secondary hover:bg-secondary-focus text-white rounded px-2 py-1">Закрыть</button>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'NewUserNotification',
  props: {
    name: {
      type: String,
      required: true
    },
    isVisible: {
      type: Boolean,
      required: true
    }
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
