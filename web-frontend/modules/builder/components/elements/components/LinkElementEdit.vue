<template>
  <div class="link-element" :class="classes">
    <Button
      v-if="variant === 'button'"
      type="link"
      v-bind="extraAttr"
      :target="target"
      :full-width="width === 'full'"
      @click.prevent=""
    >
      {{ value || $t('linkElement.noValue') }}
    </Button>
    <a
      v-else
      class="link-element__link"
      v-bind="extraAttr"
      :target="`_${target}`"
      @click.prevent=""
    >
      {{ value || $t('linkElement.noValue') }}
    </a>
  </div>
</template>

<script>
import textElement from '@baserow/modules/builder/mixins/elements/textElement'
import { compile } from 'path-to-regexp'

export default {
  name: 'LinkElement',
  mixins: [textElement],
  props: {
    // eslint-disable-next-line vue/prop-name-casing
    navigation_type: { type: String, default: 'page' },
    // eslint-disable-next-line vue/prop-name-casing
    navigate_to_page_id: { type: Number, default: null },
    // eslint-disable-next-line vue/prop-name-casing
    page_parameters: { type: Array, default: () => [] },
    // eslint-disable-next-line vue/prop-name-casing
    navigate_to_url: { type: String, default: '' },
    alignment: { type: String, default: 'left' },
    variant: { type: String, default: 'link' },
    target: { type: String, default: 'self' },
    width: { type: String, default: 'auto' },
    builder: { type: Object, required: true },
  },
  data() {
    return { inError: false, url: '' }
  },
  computed: {
    classes() {
      return {
        [`link-element--alignment-${this.alignment}`]: true,
        'element--no-value': !this.value,
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
      if (this.navigation_type === 'page') {
        if (!isNaN(this.navigate_to_page_id)) {
          const page = this.builder.pages.find(
            ({ id }) => id === this.navigate_to_page_id
          )

          // The builder page list might be empty or the page has been deleted
          if (!page) {
            this.url = ''
            return
          }

          const toPath = compile(page.path, { encode: encodeURIComponent })
          const pageParams = Object.fromEntries(
            this.page_parameters.map(({ name, value }) => [name, value])
          )
          try {
            this.url = toPath(pageParams)
          } catch (e) {
            this.inError = true
            this.url = ''
          }
        }
      } else {
        this.url = this.navigate_to_url
      }
    },
  },
}
</script>
