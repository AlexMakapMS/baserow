<template>
  <img alt="TODO" :src="element.image_url" />
</template>

<script>
export default {
  name: 'ImageElement',
  props: {
    /**
     * @type {Object}
     * @property {string} image_url
     */
    element: {
      type: Object,
      required: true,
    },
  },
}
</script>
