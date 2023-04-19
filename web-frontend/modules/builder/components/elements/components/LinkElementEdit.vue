<template>
  <div class="link-element" :class="classes">
    <Button
      v-if="element.variant === 'button'"
      type="link"
      v-bind="extraAttr"
      :target="element.target"
      :full-width="element.width === 'full'"
      @click.prevent=""
    >
      {{ element.value || $t('linkElement.noValue') }}
    </Button>
    <a
      v-else
      class="link-element__link"
      v-bind="extraAttr"
      :target="`_${element.target}`"
      @click.prevent=""
    >
      {{ element.value || $t('linkElement.noValue') }}
    </a>
  </div>
</template>

<script>
import textElement from '@baserow/modules/builder/mixins/elements/textElement'
import { LinkElementType } from '@baserow/modules/builder/elementTypes'

export default {
  name: 'LinkElement',
  mixins: [textElement],
  props: {
    element: {
      type: Object,
      required: true,
    },
    builder: { type: Object, required: true },
  },
  data() {
    return { inError: false, url: '' }
  },
  computed: {
    classes() {
      return {
        [`link-element--alignment-${this.element.alignment}`]: true,
        'element--no-value': !this.element.value,
        'element--in-error': this.inError,
      }
    },
    extraAttr() {
      const attr = {}
      if (this.url) {
        attr.href = this.url
      }
      return attr
    },
  },
  watch: {
    navigation_type() {
      this.updateUrl()
    },
    navigate_to_page_id() {
      this.updateUrl()
    },
    navigate_to_url() {
      this.updateUrl()
    },
    page_parameters: {
      handler() {
        this.updateUrl()
      },
      deep: true,
    },
  },
  mounted() {
    this.updateUrl()
  },
  methods: {
    updateUrl() {
      this.inError = false
      try {
        return LinkElementType.getUrlFromElement(this.element, this.builder)
      } catch (e) {
        this.inError = true
        return ''
      }
    },
  },
}
</script>
