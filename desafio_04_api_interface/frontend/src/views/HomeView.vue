<script setup>
import { onMounted, ref, watch } from 'vue'
import { useAnsStore } from '../store'
import { Search, ChevronLeft, ChevronRight, BarChart3, TrendingUp } from 'lucide-vue-next'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const store = useAnsStore()
const search = ref('')

onMounted(() => {
  store.fetchOperadoras(1)
  store.fetchEstatisticas()
})

const handleSearch = () => {
  store.fetchOperadoras(1, search.value)
}

const changePage = (step) => {
  const newPage = store.page + step
  if (newPage > 0 && newPage <= Math.ceil(store.total / store.limit)) {
    store.fetchOperadoras(newPage, search.value)
  }
}

// Chart Data
const chartData = ref({
  labels: [],
  datasets: []
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#1e293b',
      titleColor: '#f8fafc',
      bodyColor: '#f8fafc',
      borderColor: '#334155',
      borderWidth: 1
    }
  },
  scales: {
    y: {
      grid: { color: '#334155' },
      ticks: { color: '#94a3b8' }
    },
    x: {
      grid: { display: false },
      ticks: { color: '#94a3b8' }
    }
  }
}

watch(() => store.estatisticas, (stats) => {
  if (stats && stats.distribuicao_uf) {
    chartData.value = {
      labels: stats.distribuicao_uf.slice(0, 10).map(i => i.uf),
      datasets: [{
        label: 'Gasto Total (R$)',
        backgroundColor: '#6366f1',
        borderRadius: 4,
        data: stats.distribuicao_uf.slice(0, 10).map(i => i.total)
      }]
    }
  }
}, { deep: true })
</script>

<template>
  <div class="home-view">
    <!-- Header Stats -->
    <div class="stats-grid" v-if="store.estatisticas">
      <div class="card stat-card fade-in">
        <div class="stat-icon"><TrendingUp size="20" /></div>
        <div class="stat-info">
          <p class="stat-label">Total Despesas Acumuladas</p>
          <h2 class="stat-value">R$ {{ (store.estatisticas.total_geral / 1e9).toFixed(2) }}B</h2>
        </div>
      </div>
      <div class="card stat-card fade-in" style="animation-delay: 0.1s">
        <div class="stat-icon" style="background: rgba(34, 211, 238, 0.2); color: var(--accent)"><BarChart3 size="20" /></div>
        <div class="stat-info">
          <p class="stat-label">Média por Registro</p>
          <h2 class="stat-value">R$ {{ (store.estatisticas.media_geral / 1e6).toFixed(2) }}M</h2>
        </div>
      </div>
    </div>

    <!-- Chart -->
    <div class="chart-section card fade-in" style="animation-delay: 0.2s">
      <h3 class="section-title">Distribuição de Gasto por UF (Top 10)</h3>
      <div class="chart-container">
        <Bar :data="chartData" :options="chartOptions" v-if="chartData.labels.length" />
      </div>
    </div>

    <!-- Table Section -->
    <div id="operadoras-table" class="table-section card fade-in" style="animation-delay: 0.3s">
      <div class="table-header">
        <h3 class="section-title">Diretório de Operadoras</h3>
        <div class="search-box">
          <Search class="search-icon" size="18" />
          <input 
            v-model="search" 
            @input="handleSearch" 
            placeholder="Buscar por nome ou CNPJ..." 
          />
        </div>
      </div>

      <div class="table-container">
        <div v-if="store.loading" class="loading-overlay">
          <div class="spinner"></div>
        </div>

        <table v-else>
          <thead>
            <tr>
              <th>Razão Social</th>
              <th>CNPJ</th>
              <th>Modalidade</th>
              <th>UF</th>
              <th style="text-align: right">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="op in store.operadoras" :key="op.cnpj">
              <td>
                <div class="op-name">{{ op.razao_social }}</div>
                <div class="op-reg">Registro: {{ op.registro_ans }}</div>
              </td>
              <td>{{ op.cnpj }}</td>
              <td><span class="badge">{{ op.modalidade }}</span></td>
              <td>{{ op.uf }}</td>
              <td style="text-align: right">
                <router-link :to="{ name: 'detail', params: { cnpj: op.cnpj }}" class="view-link">
                  Ver Detalhes
                </router-link>
              </td>
            </tr>
            <tr v-if="!store.loading && store.operadoras.length === 0">
              <td colspan="5" style="text-align: center; padding: 3rem; color: var(--text-muted)">
                Nenhuma operadora encontrada.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="pagination">
        <p class="page-info">
          Mostrando <b>{{ (store.page - 1) * store.limit + 1 }}</b> - 
          <b>{{ Math.min(store.page * store.limit, store.total) }}</b> de 
          <b>{{ store.total }}</b> operadoras
        </p>
        <div class="page-controls">
          <button @click="changePage(-1)" :disabled="store.page === 1" class="page-btn">
            <ChevronLeft size="18" />
          </button>
          <span class="page-current">{{ store.page }}</span>
          <button @click="changePage(1)" :disabled="store.page >= Math.ceil(store.total / store.limit)" class="page-btn">
            <ChevronRight size="18" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.stat-icon {
  background: rgba(99, 102, 241, 0.2);
  color: var(--primary);
  padding: 1rem;
  border-radius: 1rem;
}

.stat-label {
  color: var(--text-muted);
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.chart-section {
  margin-bottom: 2rem;
}

.chart-container {
  height: 300px;
  position: relative;
}

.section-title {
  margin-bottom: 1.5rem;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.search-box {
  position: relative;
  width: 300px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
}

.search-box input {
  width: 100%;
  padding-left: 2.5rem;
}

.op-name {
  font-weight: 500;
  color: white;
}

.op-reg {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.view-link {
  color: var(--accent);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
}

.view-link:hover {
  text-decoration: underline;
}

.pagination {
  margin-top: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-info {
  font-size: 0.875rem;
  color: var(--text-muted);
}

.page-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-btn {
  background: #1a2233;
  color: var(--text-muted);
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  border: 1px solid var(--border);
}

.page-btn:hover:not(:disabled) {
  background: var(--border);
  color: white;
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.loading-overlay {
  padding: 5rem;
  display: flex;
  justify-content: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
