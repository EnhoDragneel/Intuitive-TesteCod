<template>
  <component
    :is="`i-heroicons-${props.name}`"
    :class="[
      'inline-block',
      sizeClass,
      props.color
    ]"
  />
</template>

<script setup>
import { computed } from 'vue' 

const props = defineProps({
  name: String, 
  size: {
    type: Number,
    default: 20,
  },
  color: {
    type: String,
    default: 'text-gray-700',
  },
})

const sizeClass = computed(() => `w-${props.size} h-${props.size}`)
</script>
