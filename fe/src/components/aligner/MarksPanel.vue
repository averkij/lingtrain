<script setup lang="ts">
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { getDocumentMarks, type Mark } from '@/api/documents'

const { t } = useI18n()

const props = defineProps<{
  guidFrom: string | null
  guidTo: string | null
}>()

const marksFrom = ref<Mark[]>([])
const marksTo = ref<Mark[]>([])
const loading = ref(false)

const markColors: Record<string, string> = {
  author: 'marks-panel__badge--green',
  title: 'marks-panel__badge--green',
  translator: 'marks-panel__badge--green',
  h1: 'marks-panel__badge--teal',
  h2: 'marks-panel__badge--cyan',
  h3: 'marks-panel__badge--lime',
  h4: 'marks-panel__badge--lime',
  h5: 'marks-panel__badge--lime',
  qtext: 'marks-panel__badge--purple',
  qname: 'marks-panel__badge--purple',
  image: 'marks-panel__badge--orange',
  divider: 'marks-panel__badge--orange',
}

async function fetchMarks() {
  loading.value = true
  try {
    const [fromRes, toRes] = await Promise.all([
      props.guidFrom ? getDocumentMarks(props.guidFrom) : Promise.resolve({ marks: [] }),
      props.guidTo ? getDocumentMarks(props.guidTo) : Promise.resolve({ marks: [] }),
    ])
    marksFrom.value = fromRes.marks
    marksTo.value = toRes.marks
  } finally {
    loading.value = false
  }
}

watch(
  () => [props.guidFrom, props.guidTo],
  () => {
    if (props.guidFrom || props.guidTo) {
      fetchMarks()
    } else {
      marksFrom.value = []
      marksTo.value = []
    }
  },
  { immediate: true },
)
</script>

<template>
  <div class="marks-panel">
    <div v-if="!guidFrom && !guidTo" class="marks-panel__empty">
      {{ t('aligner.selectDocument') }}
    </div>

    <template v-else>
      <div v-if="loading" class="marks-panel__loading">
        <span class="marks-panel__spinner" />
        {{ t('aligner.loading') }}
      </div>

      <div v-else-if="marksFrom.length === 0 && marksTo.length === 0" class="marks-panel__empty">
        {{ t('aligner.noMarks') }}
      </div>

      <div v-else class="marks-panel__row">
        <div class="marks-panel__side">
          <div v-for="(mark, i) in marksFrom" :key="i" class="marks-panel__item">
            <span class="marks-panel__num">{{ i + 1 }}</span>
            <span class="marks-panel__badge" :class="markColors[mark.type]">{{ mark.type }}</span>
            <span class="marks-panel__text">{{ mark.text }}</span>
          </div>
          <div v-if="marksFrom.length === 0" class="marks-panel__side-empty">--</div>
        </div>
        <div class="marks-panel__side">
          <div v-for="(mark, i) in marksTo" :key="i" class="marks-panel__item">
            <span class="marks-panel__num">{{ i + 1 }}</span>
            <span class="marks-panel__badge" :class="markColors[mark.type]">{{ mark.type }}</span>
            <span class="marks-panel__text">{{ mark.text }}</span>
          </div>
          <div v-if="marksTo.length === 0" class="marks-panel__side-empty">--</div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.marks-panel__empty {
  font-size: var(--font-size-body);
  color: var(--color-text-muted);
  text-align: center;
  padding: var(--spacing-lg);
}

.marks-panel__loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-body);
  color: var(--color-text-muted);
  padding: var(--spacing-xl);
}

.marks-panel__spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.marks-panel__row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
}

.marks-panel__side {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.marks-panel__side-empty {
  font-size: var(--font-size-body);
  color: var(--color-text-muted);
  text-align: center;
  padding: var(--spacing-lg);
}

.marks-panel__item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 5px var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
  font-size: var(--font-size-body);
}

.marks-panel__item:last-child {
  border-bottom: none;
}

.marks-panel__num {
  flex-shrink: 0;
  min-width: 24px;
  text-align: right;
  font-size: var(--font-size-sm);
  font-weight: 500;
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
}

.marks-panel__badge {
  flex-shrink: 0;
  padding: 0 6px;
  font-size: var(--font-size-2xs);
  font-weight: 600;
  border-radius: 3px;
  color: #fff;
  line-height: 18px;
  white-space: nowrap;
  background: var(--color-text-muted);
}

.marks-panel__badge--green { background: #4caf50; }
.marks-panel__badge--teal { background: #009688; }
.marks-panel__badge--cyan { background: #00bcd4; }
.marks-panel__badge--lime { background: #8bc34a; }
.marks-panel__badge--purple { background: #9c27b0; }
.marks-panel__badge--orange { background: #ff9800; }

.marks-panel__text {
  flex: 1;
  color: var(--color-text);
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
