<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { useAlignerStore } from '@/stores/aligner'
import { useAuthStore } from '@/stores/auth'
import { getProgress, uploadProxy, AlignmentState } from '@/api/alignments'
import AlignmentSettings from './AlignmentSettings.vue'
import AlignmentControls from './AlignmentControls.vue'
import ProxyUploadPanel from './ProxyUploadPanel.vue'
import VisualizationCarousel from './VisualizationCarousel.vue'
import AlignmentEditor from './AlignmentEditor.vue'

const { t } = useI18n()
const route = useRoute()
const aligner = useAlignerStore()
const auth = useAuthStore()

const guid = computed(() => route.params.guid as string)

const batchSize = ref(200)
const batchCount = ref(1)
const window_ = ref(40)
const batchShift = ref(0)
const useProxyFrom = ref(false)
const useProxyTo = ref(false)

const stateLabels: Record<number, string> = {
  [AlignmentState.INIT]: 'aligner.stateInit',
  [AlignmentState.IN_PROGRESS]: 'aligner.stateInProgress',
  [AlignmentState.IN_PROGRESS_DONE]: 'aligner.stateInProgressDone',
  [AlignmentState.DONE]: 'aligner.stateDone',
  [AlignmentState.ERROR]: 'aligner.stateError',
}

onMounted(async () => {
  const data = await getProgress(guid.value)
  aligner.selectedAlignment = data
})

onUnmounted(() => {
  aligner.stopPolling()
})

async function handleAlignAll() {
  await aligner.startAlignment(guid.value, {
    align_all: true,
    batch_shift: batchShift.value,
    window: window_.value,
    use_proxy_from: useProxyFrom.value,
    use_proxy_to: useProxyTo.value,
  })
}

async function handleAlignNext() {
  await aligner.alignNext(guid.value, {
    amount: batchCount.value,
    batch_shift: batchShift.value,
    window: window_.value,
    use_proxy_from: useProxyFrom.value,
    use_proxy_to: useProxyTo.value,
  })
}

async function handleStop() {
  await aligner.stopAlignment(guid.value)
}

async function handleResolve() {
  await aligner.resolveConflicts(guid.value, {
    use_proxy_from: useProxyFrom.value,
    use_proxy_to: useProxyTo.value,
  })
  const data = await getProgress(guid.value)
  aligner.selectedAlignment = data
}

async function handleProxyUpload(direction: 'from' | 'to', file: File) {
  const data = await uploadProxy(guid.value, direction, file)
  aligner.selectedAlignment = data
}
</script>

<template>
  <div class="alignment-detail">
    <template v-if="aligner.selectedAlignment">
      <div class="alignment-detail__header">
        <h2 class="alignment-detail__name">{{ aligner.selectedAlignment.name }}</h2>
        <span
          class="alignment-detail__state"
          :class="`alignment-detail__state--${aligner.selectedAlignment.state}`"
        >
          {{ t(stateLabels[aligner.selectedAlignment.state] ?? 'aligner.stateInit') }}
        </span>
      </div>

      <div class="alignment-detail__langs">
        {{ aligner.selectedAlignment.lang_from }} &rarr; {{ aligner.selectedAlignment.lang_to }}
      </div>

      <div v-if="aligner.selectedAlignment.total_batches > 0" class="alignment-detail__progress">
        <div class="alignment-detail__progress-top">
          <span class="alignment-detail__progress-label">{{ t('aligner.progress') }}</span>
          <span class="alignment-detail__progress-text">
            {{ aligner.selectedAlignment.curr_batches }} / {{ aligner.selectedAlignment.total_batches }}
          </span>
        </div>
        <div class="alignment-detail__progress-bar">
          <div
            class="alignment-detail__progress-fill"
            :style="{
              width: `${(aligner.selectedAlignment.curr_batches / aligner.selectedAlignment.total_batches) * 100}%`,
            }"
          />
        </div>
      </div>

      <div class="alignment-detail__panels">
        <AlignmentSettings
          v-model:batch-size="batchSize"
          v-model:batch-count="batchCount"
          v-model:window="window_"
          v-model:batch-shift="batchShift"
          v-model:use-proxy-from="useProxyFrom"
          v-model:use-proxy-to="useProxyTo"
        />

        <AlignmentControls
          :state="aligner.selectedAlignment.state"
          @align-all="handleAlignAll"
          @align-next="handleAlignNext"
          @stop="handleStop"
          @resolve="handleResolve"
        />
      </div>

      <div class="alignment-detail__section-title">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M2 3h5l1.5 2H14v8H2V3Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round" />
          <path d="M5.5 8h5M5.5 10.5h3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" />
        </svg>
        {{ t('aligner.proxyDocuments') }}
      </div>
      <p class="alignment-detail__info">{{ t('aligner.proxyInfo') }}</p>
      <div class="alignment-detail__row">
        <ProxyUploadPanel
          :label="t('aligner.proxyFrom')"
          :lang="aligner.selectedAlignment.lang_from"
          :loaded="aligner.selectedAlignment.proxy_from_loaded"
          @upload="(file) => handleProxyUpload('from', file)"
        />
        <ProxyUploadPanel
          :label="t('aligner.proxyTo')"
          :lang="aligner.selectedAlignment.lang_to"
          :loaded="aligner.selectedAlignment.proxy_to_loaded"
          @upload="(file) => handleProxyUpload('to', file)"
        />
      </div>

      <VisualizationCarousel
        :guid="guid"
        :total-batches="aligner.selectedAlignment.curr_batches"
        :user-id="auth.user?.id ?? 0"
      />

      <template v-if="aligner.selectedAlignment.curr_batches > 0">
        <div class="alignment-detail__section-title">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M3 3h10M3 8h7M3 13h9" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" />
          </svg>
          {{ t('aligner.editor') }}
        </div>
        <p class="alignment-detail__info">{{ t('aligner.editorInfo') }}</p>
        <AlignmentEditor :guid="guid" />
      </template>
    </template>

    <div v-else class="alignment-detail__loading">
      <span class="alignment-detail__spinner" />
      {{ t('aligner.loading') }}
    </div>
  </div>
</template>

<style scoped>
.alignment-detail {
  padding: var(--spacing-xl) var(--spacing-2xl);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  max-width: 1200px;
}

.alignment-detail__header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.alignment-detail__name {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text-strong);
  margin: 0;
  letter-spacing: -0.3px;
}

.alignment-detail__state {
  padding: 3px 10px;
  font-size: 11px;
  font-weight: 600;
  border-radius: 20px;
  white-space: nowrap;
  letter-spacing: 0.2px;
}

.alignment-detail__state--0 {
  background: var(--color-bg-hover);
  color: var(--color-text-muted);
}
.alignment-detail__state--1 {
  background: var(--color-info-subtle);
  color: #1d4ed8;
}
.alignment-detail__state--2 {
  background: var(--color-warning-subtle);
  color: var(--color-warning);
}
.alignment-detail__state--3 {
  background: var(--color-success-subtle);
  color: var(--color-success);
}
.alignment-detail__state--4 {
  background: var(--color-error-subtle);
  color: var(--color-error);
}

.alignment-detail__langs {
  font-size: 13px;
  color: var(--color-text-muted);
  font-weight: 500;
}

.alignment-detail__progress {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.alignment-detail__progress-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.alignment-detail__progress-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
}

.alignment-detail__progress-bar {
  height: 6px;
  background: var(--color-bg-hover);
  border-radius: 3px;
  overflow: hidden;
}

.alignment-detail__progress-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: 3px;
  transition: width var(--transition-normal);
}

.alignment-detail__progress-text {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
}

.alignment-detail__panels {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
}

.alignment-detail__section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text-strong);
  margin-top: var(--spacing-md);
}

.alignment-detail__section-title svg {
  color: var(--color-primary);
}

.alignment-detail__info {
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-info-subtle);
  border-radius: var(--radius);
  border-left: 3px solid var(--color-primary);
}

.alignment-detail__row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
  align-items: start;
}

.alignment-detail__loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-size: 13px;
  color: var(--color-text-muted);
  padding: var(--spacing-2xl);
}

.alignment-detail__spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
