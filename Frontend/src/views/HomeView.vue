<template>
  <div class="pagina-inicial">
    <div class="conteudo-central">
      <div class="cabecalho">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" fill="none" stroke="currentColor"
          stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
          class="lucide lucide-activity icone-principal">
          <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
        </svg>
        <h1 class="titulo-principal">Bem-vindo!</h1>
        <p class="subtitulo">Sistema de consulta de operadoras de saúde</p>
      </div>

      <div class="container-botao">
        <button @click="irParaOperadoras" class="botao-entrar">
          <span>Listar Operadoras</span>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icone-botao">
            <path d="M5 12h14" />
            <path d="m12 5 7 7-7 7" />
          </svg>
        </button>
      </div>

      <div class="cards-info">
        <div class="card">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="lucide lucide-search icone-card">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.3-4.3" />
          </svg>
          <h3 class="card-titulo">Busca Avançada</h3>
          <p class="card-texto">Encontre operadoras por nome, CNPJ ou registro</p>
        </div>
        <div class="card">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="lucide lucide-list icone-card">
            <line x1="8" x2="21" y1="6" y2="6" />
            <line x1="8" x2="21" y1="12" y2="12" />
            <line x1="8" x2="21" y1="18" y2="18" />
            <line x1="3" x2="3.01" y1="6" y2="6" />
            <line x1="3" x2="3.01" y1="12" y2="12" />
            <line x1="3" x2="3.01" y1="18" y2="18" />
          </svg>
          <h3 class="card-titulo">Listagem Completa</h3>
          <p class="card-texto">Acesse todas as operadoras cadastradas</p>
        </div>
        <div class="card">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor"
            stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            class="lucide lucide-info icone-card">
            <circle cx="12" cy="12" r="10" />
            <path d="M12 16v-4" />
            <path d="M12 8h.01" />
          </svg>
          <h3 class="card-titulo">Informações Detalhadas</h3>
          <p class="card-texto">Visualize dados completos de cada operadora</p>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function irParaOperadoras() {
  router.push('/operadoras')
}
</script>

<style>
:root {
  --color-primary: #4f46e5;
  --color-primary-dark: #4338ca;
}

.pagina-inicial {
  min-height: 100vh;
  background-color: #f9fafb;
  padding: 3rem 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.conteudo-central {
  max-width: 480px;
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.cabecalho {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.icone-principal {
  margin: 0 auto;
  color: var(--color-primary);
}

.titulo-principal {
  font-size: 2.25rem;
  font-weight: bold;
  color: #1f2937;
}

.subtitulo {
  font-size: 1.125rem;
  color: #4b5563;
}

.container-botao {
  margin-top: 2rem;
}

.botao-entrar {
  width: 100%;
  max-width: 260px;
  padding: 0.75rem 2rem;
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s ease;
  cursor: pointer;
  margin: 0 auto;
}

.botao-entrar:hover {
  background-color: var(--color-primary-dark);
}

.icone-botao {
  margin-left: 0.5rem;
}

.cards-info {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin-top: 3rem;
}

@media (min-width: 640px) {
  .cards-info {
    grid-template-columns: repeat(3, 1fr);
  }
}

.card {
  background-color: white;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.icone-card {
  display: block;
  margin: 0 auto 0.5rem;
  color: var(--color-primary);
}

.card-titulo {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.card-texto {
  font-size: 0.875rem;
  color: #4b5563;
}

.mensagem-info {
  background-color: #3b82f6;
  color: white;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  margin: 1rem;
  text-align: center;
}
</style>
