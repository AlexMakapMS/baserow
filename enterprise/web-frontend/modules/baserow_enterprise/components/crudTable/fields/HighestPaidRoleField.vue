<template>
  <div v-if="roleUID" class="highest-role-field">
    {{ roleName }}
    <a
      href="https://baserow.io/user-docs/subscriptions-overview#who-is-considered-a-user-for-billing-purposes"
      target="_blank"
    >
      <Badge v-if="role.isBillable" class="margin-left-1" primary
        >{{ $t('highestPaidRoleField.billable') }}
      </Badge>
    </a>
  </div>
</template>

<script>
export default {
  name: 'HighestPaidRoleField',
  props: {
    row: {
      required: true,
      type: Object,
    },
    column: {
      required: true,
      type: Object,
    },
  },
  computed: {
    roleUID() {
      return this.row[this.column.key]
    },
    roleName() {
      return this.role ? this.role.name : ''
    },
    role() {
      return this.roles.find((r) => r.uid === this.roleUID)
    },
    roleIsBillable() {
      return this?.role.isBillable
    },
    workspace() {
      return this.$store.getters['workspace/get'](
        this.column.additionalProps.workspaceId
      )
    },
    roles() {
      // filters out role not for Team subject and not for workspace level
      return this.workspace ? this.workspace._.roles : []
    },
  },
  methods: {
    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1)
    },
  },
}
</script>
