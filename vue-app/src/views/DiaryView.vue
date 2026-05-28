<template>
  <div class="page-wrap">
    <div class="row g-4">

      <!-- 왼쪽: 다이어리 작성 -->
      <div class="col-12 col-md-5">
        <div class="card">
          <div class="card-body">
            <div class="dash-card-title mb-3">
              <i class="bi bi-journal-richtext"></i>
              {{ currentYear }}년 {{ currentMonth }}월 오늘 기록
            </div>

            <!-- 날짜 -->
            <div class="mb-3">
              <label class="form-label">날짜</label>
              <input type="date" class="form-control" v-model="form.date">
            </div>

            <!-- 기분 -->
            <div class="mb-3">
              <label class="form-label">오늘 기분</label>
              <div class="mood-row">
                <label v-for="mood in moods" :key="mood" class="mood-label" @click="form.mood = mood">
                  <span class="mood-btn" :class="{ active: form.mood === mood }">{{ mood }}</span>
                </label>
              </div>
            </div>

            <!-- 테마 색상 -->
            <div class="mb-3">
              <label class="form-label">테마 색상</label>
              <div class="theme-row">
                <label v-for="theme in themes" :key="theme.color" class="theme-label" :title="theme.label" @click="form.theme_color = theme.color">
                  <span class="theme-dot-btn" :class="{ active: form.theme_color === theme.color }" :style="{ background: theme.hex }"></span>
                </label>
              </div>
            </div>

            <!-- 내용 -->
            <div class="mb-3">
              <label class="form-label">오늘 하루</label>
              <textarea class="form-control diary-textarea-lg" placeholder="오늘 하루를 자유롭게 기록해보세요..." v-model="form.content"></textarea>
            </div>

            <!-- 스티커 -->
            <div class="mb-3">
              <label class="form-label">스티커</label>
              <div class="sticker-row">
                <label v-for="s in stickerList" :key="s" class="sticker-label" @click="toggleSticker(s)">
                  <span class="sticker" :class="{ active: form.stickers.includes(s) }">{{ s }}</span>
                </label>
              </div>
            </div>

            <button class="btn btn-dark w-100" @click="saveDiary">
              <i class="bi bi-save"></i> 저장하기
            </button>
          </div>
        </div>
      </div>

      <!-- 오른쪽: 다이어리 목록 -->
      <div class="col-12 col-md-7">
        <div class="d-flex align-items-center justify-content-between mb-3">
          <h5 class="mb-0">{{ currentYear }}년 {{ currentMonth }}월 기록</h5>
          <div class="cal-nav">
            <button class="cal-nav-btn" @click="prevMonth"><i class="bi bi-chevron-left"></i></button>
            <button class="cal-nav-btn" @click="nextMonth"><i class="bi bi-chevron-right"></i></button>
          </div>
        </div>

        <template v-if="diaries.length > 0">
          <div v-for="diary in diaries" :key="diary.id" class="diary-card" :style="{ borderLeftColor: themeColor(diary.theme_color) }">
            <div class="diary-card-header">
              <div class="diary-date">
                {{ formatDate(diary.date) }}
                <span v-if="diary.mood" class="diary-mood">{{ diary.mood }}</span>
              </div>
              <div class="d-flex gap-2">
                <button class="diary-btn" @click="deleteDiary(diary.id)">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
            <div v-if="diary.content" class="diary-preview">
              {{ diary.content.slice(0, 80) }}{{ diary.content.length > 80 ? '...' : '' }}
            </div>
            <div v-if="diary.stickers?.length > 0" class="diary-stickers">
              {{ diary.stickers.join('') }}
            </div>
          </div>
        </template>
        <div v-else class="text-center py-5 text-muted">
          <i class="bi bi-journal" style="font-size:3rem;color:#ddd;display:block;margin-bottom:12px"></i>
          <p>이번 달 기록이 없어요.<br>오늘 하루를 기록해보세요! 📔</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const today = new Date()
const currentYear = ref(today.getFullYear())
const currentMonth = ref(today.getMonth() + 1)

const diaries = ref([])
const form = ref({
  date: today.toISOString().slice(0, 10),
  mood: '',
  theme_color: 'purple',
  content: '',
  stickers: []
})

const moods = ['😊','😢','😴','😤','🥰','😎','🤔','😅']
const stickerList = ['⭐','🌸','🎵','💫','🌈','🍀','🎨','🌙','🔥','💪','📚','🎯']
const themes = [
  { color: 'purple', hex: '#7F77DD', label: '보라' },
  { color: 'pink', hex: '#D4537E', label: '핑크' },
  { color: 'teal', hex: '#1D9E75', label: '초록' },
  { color: 'blue', hex: '#378ADD', label: '파랑' },
  { color: 'amber', hex: '#EF9F27', label: '노랑' }
]

const themeColorMap = { purple: '#7F77DD', pink: '#D4537E', teal: '#1D9E75', blue: '#378ADD', amber: '#EF9F27' }
function themeColor(color) { return themeColorMap[color] || '#7F77DD' }
function formatDate(dateStr) {
  const d = new Date(dateStr)
  return `${d.getMonth() + 1}월 ${d.getDate()}일`
}

function toggleSticker(s) {
  const idx = form.value.stickers.indexOf(s)
  if (idx === -1) form.value.stickers.push(s)
  else form.value.stickers.splice(idx, 1)
}

async function fetchDiaries() {
  try {
    const res = await axios.get('/api/diary', { params: { year: currentYear.value, month: currentMonth.value } })
    diaries.value = res.data.diaries
    if (res.data.today_diary) {
      const d = res.data.today_diary
      form.value = { date: d.date, mood: d.mood || '', theme_color: d.theme_color || 'purple', content: d.content || '', stickers: d.stickers || [] }
    }
  } catch (err) {
    console.error('다이어리 로딩 실패:', err)
  }
}

async function saveDiary() {
  try {
    const res = await axios.post('/api/diary', form.value)
    if (res.data.success) {
      alert(res.data.message)
      await fetchDiaries()
    }
  } catch (err) {
    console.error('저장 실패:', err)
  }
}

async function deleteDiary(id) {
  if (!confirm('삭제할까요?')) return
  try {
    const res = await axios.delete(`/api/diary/${id}`)
    if (res.data.success) await fetchDiaries()
  } catch (err) {
    console.error('삭제 실패:', err)
  }
}

function prevMonth() {
  if (currentMonth.value === 1) { currentMonth.value = 12; currentYear.value-- }
  else currentMonth.value--
  fetchDiaries()
}

function nextMonth() {
  if (currentMonth.value === 12) { currentMonth.value = 1; currentYear.value++ }
  else currentMonth.value++
  fetchDiaries()
}

onMounted(fetchDiaries)
</script>
