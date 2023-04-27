<template>
  <form @submit.prevent>
    <FormElement class="control" :error="fieldHasErrors('image_url')">
      <label class="control__label">
        {{ $t('imageElementForm.urlTitle') }}
      </label>
      <div class="control__elements">
        <input
          v-model="values.image_url"
          :class="{ 'input--error': fieldHasErrors('image_url') }"
          class="input"
          type="url"
          @blur="$v.values.image_url.$touch()"
        />
        <div
          v-if="
            fieldHasErrors('image_url') &&
            !$v.values.image_url.isValidAbsoluteURL
          "
          class="error"
        >
          {{ $t('imageElementForm.invalidUrlError') }}
        </div>
      </div>
    </FormElement>
  </form>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'
import { isValidAbsoluteURL } from '@baserow/modules/core/utils/string'

export default {
  name: 'ImageElementForm',
  mixins: [form],
  data() {
    return {
      values: {
        image_url: '',
      },
    }
  },
  methods: {
    emitChange(newValues) {
      if (this.isFormValid()) {
        form.methods.emitChange.bind(this)(newValues)
      }
    },
  },
  validations: {
    values: {
      image_url: {
        isValidAbsoluteURL: (value) =>
          isValidAbsoluteURL(value) || value === '',
      },
    },
  },
}
</script>
