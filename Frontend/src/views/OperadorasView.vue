<template>
  <div class="container">
    <h2 class="titulo">Lista de Operadoras</h2>

    <div class="busca-container">
      <div class="input-wrapper">
        <input
          v-model="busca"
          placeholder="Buscar por razão social, nome fantasia ou CNPJ"
          @keyup.enter="carregarOperadoras(1)"
          class="input-busca"
        />
        <button @click="carregarOperadoras(1)" class="botao-busca">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search">
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.3-4.3"/>
          </svg>
        </button>
      </div>
    </div>

    <div v-if="carregando" class="carregando">
      <div class="spinner"></div>
    </div>

    <div v-else-if="operadoras.length === 0" class="nenhum-resultado">
      <p>Nenhuma operadora encontrada.</p>
    </div>

    <div v-else class="grid-operadoras">
      <div v-for="op in operadoras" :key="op.registro_ans" class="card-operadora">
        <h3 class="card-titulo">{{ op.razao_social }}</h3>
        <div class="card-info">
          <p><span class="label">Fantasia:</span> {{ op.nome_fantasia || 'N/A' }}</p>
          <p><span class="label">CNPJ:</span> {{ op.cnpj }}</p>
          <p><span class="label">Registro ANS:</span> {{ op.registro_ans }}</p>
        </div>
      </div>
    </div>

    <div v-if="operadoras.length > 0" class="paginacao">
      <button 
        @click="carregarOperadoras(paginaAtual - 1)" 
        :disabled="paginaAtual === 1"
        class="botao-paginacao"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round" class="icon-esquerda">
          <path d="m15 18-6-6 6-6"/>
        </svg>
        Anterior
      </button>
      <span class="info-pagina">Página {{ paginaAtual }} de {{ totalPaginas }}</span>
      <button 
        @click="carregarOperadoras(paginaAtual + 1)" 
        :disabled="paginaAtual >= totalPaginas"
        class="botao-paginacao"
      >
        Próxima
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round" class="icon-direita">
          <path d="m9 18 6-6-6-6"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const operadoras = ref([])
const busca = ref('')
const paginaAtual = ref(1)
const totalPaginas = ref(1)
const pageSize = 10
const carregando = ref(false)

async function carregarOperadoras(pagina = 1) {
  if (pagina < 1) return

  carregando.value = true
  paginaAtual.value = pagina

  const params = new URLSearchParams()
  if (busca.value) {
    params.append('q', busca.value)
  }
  params.append('page', pagina)
  params.append('page_size', pageSize)

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/buscar/?${params}`)
    const data = await response.json()

    operadoras.value = data.results
    totalPaginas.value = data.total_pages
  } catch (error) {
    console.error('Erro ao buscar operadoras:', error)
  } finally {
    carregando.value = false
  }
}

onMounted(() => {
  carregarOperadoras()
})
</script>

<style>
:root {
  --color-primary: #4f46e5;
  --color-primary-dark: #4338ca;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.titulo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.busca-container {
  margin-bottom: 1.5rem;
}

.input-wrapper {
  position: relative;
}

.input-busca {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.input-busca:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-primary);
}

.botao-busca {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background-color: var(--color-primary);
  color: white;
  padding: 0.5rem;
  border-radius: 0.375rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.botao-busca:hover {
  background-color: var(--color-primary-dark);
}

.carregando {
  display: flex;
  justify-content: center;
  margin: 2rem 0;
}

.spinner {
  border: 4px solid transparent;
  border-top-color: var(--color-primary);
  border-bottom-color: var(--color-primary);
  border-radius: 50%;
  width: 48px;
  height: 48px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.nenhum-resultado {
  text-align: center;
  padding: 2rem 0;
  color: #4b5563;
}

.grid-operadoras {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.card-operadora {
  background-color: white;
  border-radius: 0.5rem;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s ease;
}

.card-operadora:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
}

.card-titulo {
  font-weight: bold;
  font-size: 1.125rem;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.card-info {
  font-size: 0.875rem;
  color: #4b5563;
}

.label {
  font-weight: 500;
}

.paginacao {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.botao-paginacao {
  display: flex;
  align-items: center;
  background-color: var(--color-primary);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.botao-paginacao:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.botao-paginacao:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
}

.icon-esquerda,
.icon-direita {
  margin: 0 0.25rem;
}

.info-pagina {
  color: #374151;
}
</style>
