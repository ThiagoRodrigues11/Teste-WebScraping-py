<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { ArrowLeft, Building2, MapPin, Hash, Package } from 'lucide-vue-next'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const props = defineProps({
  cnpj: String
})

const operadora = ref(null)
const despesas = ref([])
const loading = ref(true)

// Chart Data
const chartData = ref({ labels: [], datasets: [] })
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false }
  },
  scales: {
    y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
  }
}

onMounted(async () => {
  try {
    const [opRes, despRes] = await Promise.all([
      axios.get(`http://localhost:8000/api/operadoras/${props.cnpj}`),
      axios.get(`http://localhost:8000/api/operadoras/${props.cnpj}/despesas`)
    ])
    operadora.value = opRes.data
    despesas.value = despRes.data
    
    // Preparar gráfico (Inverter para ordem cronológica)
    const sortedDepesas = [...despRes.data].reverse()
    chartData.value = {
      labels: sortedDepesas.map(d => `${d.trimestre}/${d.ano}`),
      datasets: [{
        label: 'Despesa (R$)',
        borderColor: '#22d3ee',
        backgroundColor: 'rgba(34, 211, 238, 0.1)',
        data: sortedDepesas.map(d => d.ValorDespesas),
        fill: true,
        tension: 0.4
      }]
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="detail-view">
    <router-link to="/" class="back-link">
      <ArrowLeft size="18" /> Voltar para a lista
    </router-link>

    <div v-if="loading" class="loading-state">Carregando detalhes...</div>

    <div v-else-if="operadora" class="detail-container fade-in">
      <div class="header-card card">
        <div class="header-info">
          <div class="header-title">
            <Building2 size="32" class="header-icon" />
            <div>
              <h1>{{ operadora.razao_social }}</h1>
              <p class="subtitle">Detalhes cadastrais e financeiro</p>
            </div>
          </div>
        </div>

        <div class="info-grid">
          <div class="info-item">
            <Hash size="16" />
            <div class="label">CNPJ</div>
            <div class="value">{{ operadora.cnpj }}</div>
          </div>
          <div class="info-item">
            <Package size="16" />
            <div class="label">Modalidade</div>
            <div class="value">{{ operadora.modalidade }}</div>
          </div>
          <div class="info-item">
             <MapPin size="16" />
            <div class="label">UF</div>
            <div class="value">{{ operadora.uf }}</div>
          </div>
          <div class="info-item">
            <div class="label">Registro ANS</div>
            <div class="value">{{ operadora.registro_ans }}</div>
          </div>
        </div>
      </div>

      <div class="content-grid">
        <div class="chart-col card shadow">
           <h3 class="section-title">Histórico de Despesas Assistenciais</h3>
           <div class="chart-wrapper">
             <Line :data="chartData" :options="chartOptions" />
           </div>
        </div>

        <div class="list-col card shadow">
          <h3 class="section-title">Últimos Lançamentos</h3>
          <div class="expense-list">
            <div v-for="d in despesas" :key="d.id" class="expense-item">
              <div class="expense-date">{{ d.trimestre }} / {{ d.ano }}</div>
              <div class="expense-value">R$ {{ d.ValorDespesas.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) }}</div>
            </div>
            <div v-if="despesas.length === 0" class="empty-state">
              Nenhuma despesa registrada.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-muted);
  text-decoration: none;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

.back-link:hover {
  color: white;
}

.header-card {
  margin-bottom: 2rem;
  background: linear-gradient(135deg, var(--bg-card), #1a2233);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.header-icon {
  color: var(--primary);
}

.subtitle {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border);
}

.info-item .label {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--text-muted);
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.info-item .value {
  font-weight: 600;
  font-size: 1.1rem;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.chart-wrapper {
  height: 400px;
}

.expense-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.expense-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  border-bottom: 1px solid var(--border);
}

.expense-item:last-child {
  border-bottom: none;
}

.expense-date {
  color: var(--text-muted);
  font-weight: 500;
}

.expense-value {
  font-weight: 600;
  color: var(--accent);
}

@media (max-width: 900px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
