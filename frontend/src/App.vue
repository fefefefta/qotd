<template>
  <div class="xl:w-6/12 lg:w-7/12 md:w-9/12 sm:w-5/6 flex flex-col">
    <div class="self-start ml-2 mb-4">
      <h1 class=" text-5xl font-serif ">QotD</h1>
      <small class="">question of the day</small>
    </div>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>
