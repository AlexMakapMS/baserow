<template>
  <component
    :is="elementType.formComponent"
    :key="element.id"
    ref="elementForm"
    :builder="builder"
    class="element-form"
    :default-values="defaultValues"
    @values-changed="onChange($event)"
  />
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import { notifyIf } from '@baserow/modules/core/utils/error'
import { clone } from '@baserow/modules/core/utils/object'
import _ from 'lodash'

export default {
  name: 'GeneralSidePanel',
  inject: ['builder'],
  props: {},
  data() {
    return {}
  },
  computed: {
    ...mapGetters({
      element: 'element/getSelected',
    }),

    elementType() {
      if (this.element) {
        return this.$registry.get('element', this.element.type)
      }
      return null
    },

    defaultValues() {
      return this.elementType.getComponentProps(this.element)
    },
  },
  methods: {
    ...mapActions({
      actionDebouncedUpdateSelectedElement: 'element/debouncedUpdateSelected',
    }),
    async onChange(newValues) {
      const oldValues = this.elementType.getComponentProps(this.element)
      if (!_.isEqual(newValues, oldValues)) {
        try {
          await this.actionDebouncedUpdateSelectedElement({
            // Here we clone the values to prevent "modification oustide
            // of the store" error
            values: clone(newValues),
          })
        } catch (error) {
          // Restore the previous saved values from the store
          this.$refs.elementForm.reset()
          notifyIf(error)
        }
      }
    },
  },
}
</script>
