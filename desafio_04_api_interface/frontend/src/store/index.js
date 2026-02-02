import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export const useAnsStore = defineStore('ans', {
    state: () => ({
        operadoras: [],
        total: 0,
        page: 1,
        limit: 10,
        loading: false,
        error: null,
        estatisticas: null
    }),
    actions: {
        async fetchOperadoras(page = 1, search = '') {
            this.loading = true
            this.error = null
            try {
                const response = await axios.get(`${API_BASE}/operadoras`, {
                    params: { page, limit: this.limit, search }
                })
                this.operadoras = response.data.data
                this.total = response.data.total
                this.page = response.data.page
            } catch (err) {
                this.error = 'Erro ao carregar operadoras'
                console.error(err)
            } finally {
                this.loading = false
            }
        },
        async fetchEstatisticas() {
            try {
                const response = await axios.get(`${API_BASE}/estatisticas`)
                this.estatisticas = response.data
            } catch (err) {
                console.error(err)
            }
        }
    }
})
