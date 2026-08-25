<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { httpsCallable } from 'firebase/functions'
import { functions, firebaseEnabled, logAnalyticsEvent } from '@/services/firebase'
import { i18n } from '@/i18n'

const { t } = useI18n()

const email = ref('')
const busy = ref(false)
const done = ref(false)
const error = ref('')

function isValid(v: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)
}

async function submit(): Promise<void> {
  error.value = ''
  const value = email.value.trim()
  if (!isValid(value)) {
    error.value = t('newsletter.errInvalid')
    return
  }
  if (!firebaseEnabled || !functions) {
    error.value = t('newsletter.errGeneric')
    return
  }
  busy.value = true
  try {
    const call = httpsCallable<{ email: string; locale: string }, { ok: boolean }>(
      functions,
      'subscribeNewsletter',
    )
    await call({ email: value, locale: i18n.global.locale.value })
    // GA4 lead-gen tracking (best-effort).
    await logAnalyticsEvent('generate_lead', { method: 'newsletter' })
    done.value = true
    email.value = ''
  } catch {
    error.value = t('newsletter.errGeneric')
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="newsletter">
    <template v-if="!done">
      <label class="newsletter-label" for="nl-email">{{ t('newsletter.heading') }}</label>
      <div class="newsletter-row">
        <input
          id="nl-email"
          v-model="email"
          type="email"
          autocomplete="email"
          :placeholder="t('newsletter.placeholder')"
          class="newsletter-input"
          :disabled="busy"
          @keyup.enter="submit"
        />
        <button type="button" class="newsletter-btn" :disabled="busy" @click="submit">
          {{ busy ? t('newsletter.sending') : t('newsletter.button') }}
        </button>
      </div>
      <p v-if="error" class="newsletter-error">{{ error }}</p>
      <p class="newsletter-privacy">{{ t('newsletter.privacy') }}</p>
    </template>
    <p v-else class="newsletter-done">{{ t('newsletter.success') }}</p>
  </div>
</template>

<style scoped lang="scss">
.newsletter { display: flex; flex-direction: column; gap: .5rem; min-width: 240px; max-width: 340px; }
.newsletter-label { font-size: .82rem; color: #CFE0F2; }
.newsletter-row { display: flex; gap: .4rem; }
.newsletter-input {
  flex: 1; padding: .45rem .6rem; border-radius: 6px; border: 1px solid #2C496E;
  background: #16314F; color: #fff; font-size: .85rem;
  &::placeholder { color: #7E97B6; }
  &:focus { outline: none; border-color: #5BC2B5; }
  &:disabled { opacity: .6; }
}
.newsletter-btn {
  padding: .45rem .85rem; border-radius: 6px; border: none; cursor: pointer;
  background: #5BC2B5; color: #08263F; font-size: .82rem; font-weight: 600; white-space: nowrap;
  &:hover { background: #6FD0C3; }
  &:disabled { opacity: .6; cursor: default; }
}
.newsletter-error { font-size: .74rem; color: #FF9B9B; margin: 0; }
.newsletter-privacy { font-size: .72rem; line-height: 1.5; color: #8FA9C6; margin: .15rem 0 0; }
.newsletter-done { font-size: .82rem; color: #5BC2B5; margin: 0; }
</style>
