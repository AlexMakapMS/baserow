<template>
  <div
    class="element"
    :class="{ 'element--active': active }"
    @click="$emit('selected')"
  >
    <InsertElementButton
      v-if="active"
      class="element__insert--top"
      @click="$emit('insert', PLACEMENTS.BEFORE)"
    />
    <ElementMenu
      v-if="active"
      :move-up-disabled="isFirstElement"
      :move-down-disabled="isLastElement"
      :is-copying="isCopying"
      @delete="$emit('delete')"
      @move="$emit('move', $event)"
      @duplicate="$emit('duplicate')"
    />
    <component
      :is="elementType.component"
      v-bind="elementType.getComponentProps(element)"
      class="element__component"
    ></component>
    <InsertElementButton
      v-if="active"
      class="element__insert--bottom"
      @click="$emit('insert', PLACEMENTS.AFTER)"
    />
  </div>
</template>

<script>
import ElementMenu from '@baserow/modules/builder/components/elements/ElementMenu'
import InsertElementButton from '@baserow/modules/builder/components/elements/InsertElementButton'
import { PLACEMENTS } from '@baserow/modules/builder/enums'
export default {
  name: 'ElementPreview',
  components: { ElementMenu, InsertElementButton },
  props: {
    element: {
      type: Object,
      required: true,
    },
    active: {
      type: Boolean,
      required: false,
      default: false,
    },
    isLastElement: {
      type: Boolean,
      required: false,
      default: false,
    },
    isFirstElement: {
      type: Boolean,
      required: false,
      default: false,
    },
    isCopying: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    PLACEMENTS: () => PLACEMENTS,
    elementType() {
      return this.$registry.get('element', this.element.type)
    },
  },
}
</script>
