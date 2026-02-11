<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { apiGetUsers, type UserOut } from '@/api/auth'
import { useToast } from '@/composables/useToast'

const { t } = useI18n()
const toast = useToast()

const users = ref<UserOut[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    users.value = await apiGetUsers()
  } catch {
    toast.error(t('admin.loadError'))
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="admin-page">
    <h1 class="admin-title">{{ t('admin.title') }}</h1>

    <h2 class="table-title">{{ t('admin.usersTable') }}</h2>

    <p v-if="loading" class="loading-text">{{ t('admin.loading') }}</p>

    <div v-else class="table-wrap">
      <table class="users-table">
        <thead>
          <tr>
            <th>{{ t('admin.colId') }}</th>
            <th>{{ t('admin.colUsername') }}</th>
            <th>{{ t('admin.colEmail') }}</th>
            <th>{{ t('admin.colRole') }}</th>
            <th>{{ t('admin.colVerified') }}</th>
            <th>{{ t('admin.colActive') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>{{ user.is_email_verified ? t('admin.yes') : t('admin.no') }}</td>
            <td>{{ user.is_active ? t('admin.yes') : t('admin.no') }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.admin-page {
  max-width: 900px;
  margin: 0 auto;
  padding: var(--spacing-xl);
}

.admin-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-strong);
  margin-bottom: var(--spacing-xl);
}

.table-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: var(--spacing-md);
}

.loading-text {
  color: var(--color-text-muted);
  font-size: 14px;
}

.table-wrap {
  overflow-x: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.users-table th,
.users-table td {
  padding: var(--spacing-sm) var(--spacing-md);
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.users-table th {
  background: var(--color-bg-hover);
  font-weight: 600;
  color: var(--color-text-subtle);
  font-size: 13px;
}

.users-table tbody tr:last-child td {
  border-bottom: none;
}

.users-table tbody tr:hover {
  background: var(--color-bg-hover);
}
</style>
