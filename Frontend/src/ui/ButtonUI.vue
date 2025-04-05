<template>
  <button
    :class="[
      'inline-flex items-center justify-center px-4 py-2 rounded-xl font-medium transition duration-150 ease-in-out',
      variant === 'primary' && 'bg-primary text-white hover:bg-primary-dark',
      variant === 'outline' && 'border border-gray-300 text-gray-700 hover:bg-gray-100',
      variant === 'ghost' && 'text-gray-700 hover:bg-gray-100',
      disabled && 'opacity-50 cursor-not-allowed'
    ]"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary', // 'primary', 'outline', 'ghost'
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})
</script>
