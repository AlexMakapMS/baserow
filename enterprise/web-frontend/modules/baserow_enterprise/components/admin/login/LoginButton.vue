<template>
  <div>
    <a
      class="auth-provider-buttons__button"
      :class="{ 'auth-provider-buttons__button--small': small }"
      :href="`${loginUrl}`"
      target="_self"
    >
      <AuthProviderIcon :icon="icon" />
      <div v-if="!small">{{ $t('loginButton.continueWith') }} {{ name }}</div>
    </a>
  </div>
</template>

<script>
import AuthProviderIcon from '@baserow_enterprise/components/AuthProviderIcon.vue'

export default {
  name: 'OAuth2LoginButton',
  components: { AuthProviderIcon },
  props: {
    redirectUrl: {
      type: String,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      required: true,
    },
    small: {
      type: Boolean,
      default: false,
      required: false,
    },
    invitation: {
      required: false,
      validator: (prop) => typeof prop === 'object' || prop === null,
      default: null,
    },
  },
  computed: {
    loginUrl() {
      // GroupDeprecation
      const { groupInvitationToken, workspaceInvitationToken } =
        this.$route.query
      const invitationToken = workspaceInvitationToken || groupInvitationToken
      const parsedUrl = new URL(this.redirectUrl)
      if (invitationToken) {
        parsedUrl.searchParams.append(
          'workspace_invitation_token',
          invitationToken
        )
      }
      return parsedUrl.toString()
    },
  },
}
</script>
