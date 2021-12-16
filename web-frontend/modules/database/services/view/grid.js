export default (client) => {
  return {
    fetchRows({
      gridId,
      limit = 100,
      offset = null,
      cancelToken = null,
      includeFieldOptions = false,
      includeRowMetadata = true,
      search = false,
      publicUrl = false,
    }) {
      const config = {
        params: {
          limit,
        },
      }
      const include = []

      if (offset !== null) {
        config.params.offset = offset
      }

      if (cancelToken !== null) {
        config.cancelToken = cancelToken
      }

      if (includeFieldOptions) {
        include.push('field_options')
      }

      if (includeRowMetadata) {
        include.push('row_metadata')
      }

      if (include.length > 0) {
        config.params.include = include.join(',')
      }

      if (search) {
        config.params.search = search
      }

      const url = publicUrl ? 'public/' : ''

      return client.get(`/database/views/grid/${gridId}/${url}`, config)
    },
    fetchCount({ gridId, search, cancelToken = null, publicUrl = false }) {
      const config = {
        params: {
          count: true,
        },
      }
      if (cancelToken !== null) {
        config.cancelToken = cancelToken
      }

      if (search) {
        config.params.search = search
      }

      const url = publicUrl ? 'public/' : ''

      return client.get(`/database/views/grid/${gridId}/${url}`, config)
    },
    filterRows({ gridId, rowIds, fieldIds = null }) {
      const data = { row_ids: rowIds }

      if (fieldIds !== null) {
        data.field_ids = fieldIds
      }

      return client.post(`/database/views/grid/${gridId}/`, data)
    },
  }
}
