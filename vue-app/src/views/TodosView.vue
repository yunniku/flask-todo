<template>
  <div id="todo-app">

    <!-- 구글 캘린더 연동 상태 -->
    <div class="d-flex justify-content-end mb-3">
      <a v-if="googleConnected" href="/google/logout" class="btn btn-sm btn-outline-danger me-2">
        <i class="bi bi-google"></i> 구글 캘린더 연동 해제
      </a>
      <a v-else href="/google/login" class="btn btn-sm btn-outline-dark">
        <i class="bi bi-google"></i> 구글 캘린더 연동하기
      </a>
    </div>

    <div class="row g-4">

      <!-- 왼쪽: 할 일 추가 폼 -->
      <div class="col-md-4">
        <div class="card shadow-sm mb-4">
          <div class="card-body p-4">
            <h5 class="card-title mb-3">
              <i class="bi bi-plus-circle"></i> 할 일 추가
            </h5>
            <div class="mb-3">
              <input type="text" class="form-control" placeholder="할 일 제목 *" v-model="form.title">
            </div>
            <div class="mb-3">
              <textarea class="form-control" placeholder="상세 내용 (선택)" rows="2" v-model="form.content"></textarea>
            </div>
            <div class="mb-3">
              <input type="text" class="form-control" placeholder="카테고리 (예: 공부, 운동)" v-model="form.category">
            </div>
            <div class="mb-3">
              <label class="form-label text-muted small">마감일</label>
              <input type="date" class="form-control" v-model="form.due_date">
            </div>
            <button class="btn btn-dark w-100" @click="addTodo" :disabled="loading">
              <i class="bi bi-plus"></i> 추가하기
            </button>
          </div>
        </div>

        <!-- 카테고리 필터 -->
        <div class="card shadow-sm" v-if="categories.length > 0">
          <div class="card-body p-3">
            <h6 class="card-title"><i class="bi bi-tag"></i> 카테고리</h6>
            <button class="btn btn-sm me-1 mb-1"
              :class="selectedCategory === '' ? 'btn-dark' : 'btn-outline-dark'"
              @click="selectedCategory = ''">전체</button>
            <button v-for="cat in categories" :key="cat"
              class="btn btn-sm me-1 mb-1"
              :class="selectedCategory === cat ? 'btn-dark' : 'btn-outline-dark'"
              @click="selectedCategory = cat">{{ cat }}</button>
          </div>
        </div>
      </div>

      <!-- 오른쪽: 할 일 목록 -->
      <div class="col-md-8">
        <h5 class="mb-4 mt-2">
          <i class="bi bi-list-check"></i>
          {{ selectedCategory ? selectedCategory + ' 할 일' : '전체 할 일' }}
          <span class="badge bg-secondary">{{ filteredTodos.length }}</span>
        </h5>

        <div v-if="loading" class="text-center py-5 text-muted">
          <div class="spinner-border spinner-border-sm"></div> 불러오는 중...
        </div>

        <template v-else-if="filteredTodos.length > 0">
          <div v-for="todo in filteredTodos" :key="todo.id"
            class="card todo-card shadow-sm mb-2"
            :class="{ 'done-card': todo.done }">
            <div class="card-body p-3">
              <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                  <h6 class="mb-1" :class="{ 'done-text': todo.done }">{{ todo.title }}</h6>
                  <p v-if="todo.content" class="text-muted small mb-1" :class="{ 'done-text': todo.done }">{{ todo.content }}</p>
                  <div class="d-flex gap-2 flex-wrap">
                    <span v-if="todo.category" class="badge bg-secondary">{{ todo.category }}</span>
                    <span v-if="todo.due_date" class="badge bg-warning text-dark">
                      <i class="bi bi-calendar"></i> {{ todo.due_date }}
                    </span>
                    <span v-if="todo.done" class="badge bg-success">완료 ✅</span>
                  </div>
                </div>
                <div class="d-flex gap-1 ms-2">
                  <button class="btn btn-sm" :class="todo.done ? 'btn-success' : 'btn-outline-success'" @click="toggleTodo(todo)">
                    <i class="bi bi-check"></i>
                  </button>
                  <a v-if="googleConnected" :href="'/calendar/add/' + todo.id" class="btn btn-sm btn-outline-dark" title="구글 캘린더에 추가">
                    <i class="bi bi-calendar-plus"></i>
                  </a>
                  <a :href="'/edit/' + todo.id" class="btn btn-sm btn-outline-primary">
                    <i class="bi bi-pencil"></i>
                  </a>
                  <button class="btn btn-sm btn-outline-danger" @click="openModal(todo.id, todo.title)">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </template>

        <div v-else class="text-center py-5 text-muted">
          <i class="bi bi-inbox" style="font-size: 3rem;"></i>
          <p class="mt-2">할 일이 없어요! 추가해보세요 😊</p>
        </div>
      </div>
    </div>

    <!-- 삭제 확인 모달 -->
    <div v-if="showModal" class="modal fade show d-block" style="background:rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title"><i class="bi bi-exclamation-triangle text-danger"></i> 삭제 확인</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <p><strong>{{ deleteTodoTitle }}</strong> 을(를) 정말 삭제할까요?</p>
            <p class="text-muted small">삭제된 항목은 복구할 수 없어요.</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">취소</button>
            <button class="btn btn-danger" @click="deleteTodo"><i class="bi bi-trash"></i> 삭제</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const todos = ref([])
const loading = ref(false)
const selectedCategory = ref('')
const googleConnected = ref(false)
const form = ref({ title: '', content: '', category: '', due_date: '' })
const showModal = ref(false)
const deleteTodoId = ref(null)
const deleteTodoTitle = ref('')

const categories = computed(() => [...new Set(todos.value.map(t => t.category).filter(c => c))])
const filteredTodos = computed(() => {
  if (!selectedCategory.value) return todos.value
  return todos.value.filter(t => t.category === selectedCategory.value)
})

async function fetchTodos() {
  loading.value = true
  try {
    const res = await axios.get('/api/todos')
    if (res.data.success) todos.value = res.data.todos
  } finally {
    loading.value = false
  }
}

async function fetchGoogleStatus() {
  try {
    const res = await axios.get('/api/google/status')
    googleConnected.value = res.data.connected
  } catch {}
}

async function addTodo() {
  if (!form.value.title.trim()) return alert('제목을 입력해주세요!')
  try {
    const res = await axios.post('/api/todos', form.value)
    if (res.data.success) {
      await fetchTodos()
      form.value = { title: '', content: '', category: '', due_date: '' }
    }
  } catch (err) {
    console.error('추가 실패:', err)
  }
}

async function toggleTodo(todo) {
  try {
    const res = await axios.put(`/api/todos/${todo.id}`, { done: !todo.done })
    if (res.data.success) todo.done = !todo.done
  } catch (err) {
    console.error('토글 실패:', err)
  }
}

function openModal(id, title) {
  deleteTodoId.value = id
  deleteTodoTitle.value = title
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  deleteTodoId.value = null
  deleteTodoTitle.value = ''
}

async function deleteTodo() {
  try {
    const res = await axios.delete(`/api/todos/${deleteTodoId.value}`)
    if (res.data.success) {
      todos.value = todos.value.filter(t => t.id !== deleteTodoId.value)
      closeModal()
    }
  } catch (err) {
    console.error('삭제 실패:', err)
  }
}

onMounted(() => {
  fetchTodos()
  fetchGoogleStatus()
})
</script>
