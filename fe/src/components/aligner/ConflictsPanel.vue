<script setup lang="ts">
import { onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useEditorStore } from '@/stores/editor'

const { t } = useI18n()
const editor = useEditorStore()

const props = defineProps<{
  guid: string
}>()

onMounted(() => {
  editor.fetchConflicts(props.guid)
})

async function showDetail(id: number) {
  await editor.fetchConflictDetail(props.guid, id)
}
</script>

<template>
  <div class="conflicts-panel">
    <h3 class="conflicts-panel__title">{{ t('aligner.conflicts') }}</h3>

    <div v-if="editor.conflicts.length === 0" class="conflicts-panel__empty">
      {{ t('aligner.noConflicts') }}
    </div>

    <ul v-else class="conflicts-panel__list">
      <li
        v-for="c in editor.conflicts"
        :key="c.id"
        class="conflicts-panel__item"
        @click="showDetail(c.id)"
      >
        <span class="conflicts-panel__type">{{ c.type }}</span>
        <span class="conflicts-panel__batch">Batch {{ c.batch_id }}</span>
      </li>
    </ul>

    <div v-if="editor.conflictDetails" class="conflicts-panel__detail">
      <div class="conflicts-panel__detail-header">
        {{ editor.conflictDetails.type }} (Batch {{ editor.conflictDetails.batch_id }})
      </div>
      <div class="conflicts-panel__detail-sides">
        <div class="conflicts-panel__detail-side">
          <strong>{{ t('aligner.from') }}</strong>
          <p v-for="(line, i) in editor.conflictDetails.left" :key="i">{{ line }}</p>
        </div>
        <div class="conflicts-panel__detail-side">
          <strong>{{ t('aligner.to') }}</strong>
          <p v-for="(line, i) in editor.conflictDetails.right" :key="i">{{ line }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.conflicts-panel {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-xs);
}

.conflicts-panel__title {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-strong);
  margin-bottom: var(--spacing-md);
}

.conflicts-panel__empty {
  font-size: 13px;
  color: var(--color-text-muted);
  text-align: center;
  padding: var(--spacing-lg);
}

.conflicts-panel__list {
  list-style: none;
  padding: 0;
  margin: 0 0 var(--spacing-md);
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.conflicts-panel__item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.conflicts-panel__item:hover {
  background: var(--color-bg-hover);
}

.conflicts-panel__type {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text);
}

.conflicts-panel__batch {
  font-size: 12px;
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
}

.conflicts-panel__detail {
  border-top: 1px solid var(--color-border);
  padding-top: var(--spacing-md);
}

.conflicts-panel__detail-header {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-strong);
  margin-bottom: var(--spacing-sm);
}

.conflicts-panel__detail-sides {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

.conflicts-panel__detail-side {
  font-size: 12px;
  color: var(--color-text);
  line-height: 1.5;
}

.conflicts-panel__detail-side strong {
  display: block;
  font-size: 10px;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: var(--spacing-xs);
}

.conflicts-panel__detail-side p {
  margin: 2px 0;
}
</style>
