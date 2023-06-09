<template>
  <div>
    <ul class="dashboard__sidebar-group">
      <li class="dashboard__sidebar-title">
        {{ $t('dashboardSidebar.workspaces') }}
      </li>
      <li v-for="workspace in workspaces" :key="workspace.id">
        <a
          class="dashboard__sidebar-link"
          @click="$emit('workspace-selected', workspace)"
        >
          <i class="fas fa-fw fa-layer-group"></i>
          {{ workspace.name }}
        </a>
      </li>
      <li>
        <a
          v-if="$hasPermission('create_workspace')"
          class="dashboard__sidebar-link dashboard__sidebar-link--light"
          @click="$emit('create-workspace-clicked')"
        >
          <i class="fas fa-fw fa-plus"></i>
          {{ $t('dashboard.createWorkspace') }}
        </a>
      </li>
    </ul>
    <ul class="dashboard__sidebar-group">
      <li class="dashboard__sidebar-title">
        {{ $t('dashboardSidebar.links') }}
      </li>
      <component
        :is="component"
        v-for="(component, index) in sidebarLinksComponents"
        :key="index"
      ></component>
      <li>
        <a
          class="dashboard__sidebar-link"
          href="https://baserow.io/user-docs"
          target="_blank"
        >
          <i class="fas fa-fw fa-question-circle"></i>
          {{ $t('dashboardSidebar.knowledgeBase') }}
        </a>
      </li>
      <li>
        <a
          class="dashboard__sidebar-link"
          href="https://baserow.io/blog/category/tutorials"
          target="_blank"
        >
          <i class="fas fa-fw fa-graduation-cap"></i>
          {{ $t('dashboardSidebar.tutorials') }}
        </a>
      </li>
      <li>
        <a class="dashboard__sidebar-link" @click="$refs.settingsModal.show()">
          <i class="fas fa-fw fa-cogs"></i>
          {{ $t('dashboardSidebar.userSettings') }}
        </a>
      </li>
      <li>
        <a class="dashboard__sidebar-link" @click="$refs.trashModal.show()">
          <i class="fas fa-fw fa-trash"></i>
          {{ $t('dashboardSidebar.trash') }}
        </a>
      </li>
      <li>
        <a class="dashboard__sidebar-link" @click="logoff()">
          <i class="fas fa-fw fa-sign-out-alt"></i>
          {{ $t('dashboardSidebar.logoff') }}
        </a>
      </li>
    </ul>
    <SettingsModal ref="settingsModal"></SettingsModal>
    <TrashModal ref="trashModal"></TrashModal>
  </div>
</template>

<script>
import TrashModal from '@baserow/modules/core/components/trash/TrashModal'
import SettingsModal from '@baserow/modules/core/components/settings/SettingsModal'
import { logoutAndRedirectToLogin } from '@baserow/modules/core/utils/auth'

export default {
  name: 'DashboardSidebar',
  components: { SettingsModal, TrashModal },
  props: {
    workspaces: {
      type: Array,
      required: true,
    },
  },
  computed: {
    sidebarLinksComponents() {
      return Object.values(this.$registry.getAll('plugin'))
        .map((plugin) => plugin.getDashboardSidebarLinksComponent())
        .filter((component) => component !== null)
    },
  },
  methods: {
    logoff() {
      logoutAndRedirectToLogin(this.$nuxt.$router, this.$store)
    },
  },
}
</script>
