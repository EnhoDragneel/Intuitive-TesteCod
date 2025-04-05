<template>
  <div class="relative w-full">
    <input
      v-bind="$attrs"
      class="w-full pl-4 pr-12 py-2 rounded-xl border border-gray-300 focus:ring-2 focus:ring-primary focus:outline-none text-gray-800 placeholder-gray-400"
    />
    <div class="absolute right-2 top-1/2 -translate-y-1/2 flex items-center space-x-1">
      <slot name="append" />
    </div>
  </div>
</template>
