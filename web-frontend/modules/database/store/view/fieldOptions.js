import _ from 'lodash'
import ViewService from '@baserow/modules/database/services/view'
import { clone } from '@baserow/modules/core/utils/object'

export default () => {
  const state = () => ({
    fieldOptions: {},
  })

  const mutations = {
    REPLACE_ALL_FIELD_OPTIONS(state, fieldOptions) {
      state.fieldOptions = fieldOptions
    },
    UPDATE_ALL_FIELD_OPTIONS(state, fieldOptions) {
      state.fieldOptions = _.merge({}, state.fieldOptions, fieldOptions)
    },
    UPDATE_FIELD_OPTIONS_OF_FIELD(state, { fieldId, values }) {
      if (Object.prototype.hasOwnProperty.call(state.fieldOptions, fieldId)) {
        Object.assign(state.fieldOptions[fieldId], values)
      } else {
        state.fieldOptions = Object.assign({}, state.fieldOptions, {
          [fieldId]: values,
        })
      }
    },
    DELETE_FIELD_OPTIONS(state, fieldId) {
      if (Object.prototype.hasOwnProperty.call(state.fieldOptions, fieldId)) {
        delete state.fieldOptions[fieldId]
      }
    },
  }

  const actions = {
    /**
     * Updates the field options of a given field and also makes an API request to the
     * backend with the changed values. If the request fails the action is reverted.
     */
    async updateFieldOptionsOfField(
      { commit, getters },
      { field, values, oldValues }
    ) {
      const viewId = getters.getViewId
      commit('UPDATE_FIELD_OPTIONS_OF_FIELD', {
        fieldId: field.id,
        values,
      })
      const updateValues = { field_options: {} }
      updateValues.field_options[field.id] = values

      try {
        await ViewService(this.$client).updateFieldOptions({
          viewId,
          values: updateValues,
        })
      } catch (error) {
        commit('UPDATE_FIELD_OPTIONS_OF_FIELD', {
          fieldId: field.id,
          values: oldValues,
        })
        throw error
      }
    },
    /**
     * Updates the field options of a given field in the store. So no API request to
     * the backend is made.
     */
    setFieldOptionsOfField({ commit }, { field, values }) {
      commit('UPDATE_FIELD_OPTIONS_OF_FIELD', {
        fieldId: field.id,
        values,
      })
    },
    /**
     * Replaces all field options with new values and also makes an API request to the
     * backend with the changed values. If the request fails the action is reverted.
     */
    async updateAllFieldOptions(
      { dispatch, getters },
      { newFieldOptions, oldFieldOptions }
    ) {
      const viewId = getters.getViewId
      dispatch('forceUpdateAllFieldOptions', newFieldOptions)
      const updateValues = { field_options: newFieldOptions }

      try {
        await ViewService(this.$client).updateFieldOptions({
          viewId,
          values: updateValues,
        })
      } catch (error) {
        dispatch('forceUpdateAllFieldOptions', oldFieldOptions)
        throw error
      }
    },
    /**
     * Forcefully updates all field options without making a call to the backend.
     */
    forceUpdateAllFieldOptions({ commit }, fieldOptions) {
      commit('UPDATE_ALL_FIELD_OPTIONS', fieldOptions)
    },
    /**
     * Updates the order of all the available field options. The provided order parameter
     * should be an array containing the field ids in the correct order.
     */
    async updateFieldOptionsOrder({ commit, getters, dispatch }, { order }) {
      const oldFieldOptions = clone(getters.getAllFieldOptions)
      const newFieldOptions = clone(getters.getAllFieldOptions)

      // Update the order of the field options that have not been provided in the order.
      // They will get a position that places them after the provided field ids.
      let i = 0
      Object.keys(newFieldOptions).forEach((fieldId) => {
        if (!order.includes(parseInt(fieldId))) {
          newFieldOptions[fieldId].order = order.length + i
          i++
        }
      })

      // Update create the field options and set the correct order value.
      order.forEach((fieldId, index) => {
        const id = fieldId.toString()
        if (Object.prototype.hasOwnProperty.call(newFieldOptions, id)) {
          newFieldOptions[fieldId.toString()].order = index
        }
      })

      return await dispatch('updateAllFieldOptions', {
        oldFieldOptions,
        newFieldOptions,
      })
    },
    /**
     * Deletes the field options of the provided field id if they exist.
     */
    forceDeleteFieldOptions({ commit }, fieldId) {
      commit('DELETE_FIELD_OPTIONS', fieldId)
    },
  }

  const getters = {
    getAllFieldOptions(state) {
      return state.fieldOptions
    },
  }

  return {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
  }
}
