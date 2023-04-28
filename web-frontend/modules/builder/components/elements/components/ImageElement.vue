<template>
  <img
    :alt="element.alt_text || $t('imageElement.emptyState')"
    :src="element.image_url"
  />
</template>

<script>
export default {
  name: 'ImageElement',
  props: {
    /**
     * @type {Object}
     * @property {string} image_url - The url of the image source
     * @property {string} alt_text - The text that's displayed when the image can't load
     */
    element: {
      type: Object,
      required: true,
    },
  },
}
</script>
