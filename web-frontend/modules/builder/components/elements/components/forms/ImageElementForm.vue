<template>
  <form @submit.prevent>
    <FormElement class="control">
      <label class="control__label">
        {{ $t('imageElementForm.urlTitle') }}
      </label>
      <div class="control__elements">
        <input v-model="values.image_url" class="input" type="url" />
      </div>
    </FormElement>
  </form>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'

export default {
  name: 'ImageElementForm',
  mixins: [form],
  data() {
    return {
      values: {
        image_url: null,
      },
    }
  },
}
</script>
