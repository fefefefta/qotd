<template>
  <div class="sticky top-4 z-40">
    <div class="card bg-white shadow-lg p-4 md:p-6">
      <h1 class="card-title text-left">🤔 {{ question.title }}</h1>
      <p class="text-gray-700 text-left">{{ question.text }}</p>
      <span class="text-left">
        <div class="badge badge-secondary">{{ question.date }}</div>
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Question',
  props: {
    question: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.card {
  width: 100%; /* Ширина занимает всю доступную ширину */
}
</style>
