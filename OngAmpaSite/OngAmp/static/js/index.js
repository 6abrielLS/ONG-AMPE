// Arquivo: static/js/index.js

document.addEventListener("DOMContentLoaded", function () {
    console.log(">>> JS INICIADO: Buscando container...");

    const sliderContainer = document.querySelector(".parceiros-container");

    if (!sliderContainer) {
        console.error(">>> ERRO: Container .parceiros-container NÃO ENCONTRADO no HTML!");
        return;
    }

    console.log(">>> SUCESSO: Container encontrado.");

    // 1. GARANTIR OVERFLOW (Transbordamento)
    // Vamos clonar os itens várias vezes até termos certeza que é maior que a tela
    const items = Array.from(sliderContainer.children);
    const screenWidth = window.innerWidth;
    let currentContentWidth = sliderContainer.scrollWidth;

    // Clona até que o conteúdo seja pelo menos 3 vezes o tamanho da tela
    // Isso garante que sempre haverá espaço para rolar
    while (currentContentWidth < screenWidth * 3) {
        items.forEach((item) => {
            const clone = item.cloneNode(true);
            sliderContainer.appendChild(clone);
        });
        currentContentWidth = sliderContainer.scrollWidth;
        console.log(">>> Clonando itens... Largura atual: " + currentContentWidth + "px");
    }

    // 2. Configurações
    let scrollSpeed = 2; // Aumentei um pouco para ser visível
    
    // O ponto de reset é a largura dos itens ORIGINAIS (antes de clonarmos milhares de vezes)
    // Para simplificar: Vamos resetar quando rolar o tamanho do primeiro bloco de clones
    let firstSetWidth = 0;
    items.forEach(item => {
        // Soma a largura da imagem + o gap (estimado em 60px do seu CSS)
        firstSetWidth += item.offsetWidth + 60; 
    });

    console.log(">>> Ponto de Reset calculado em: " + firstSetWidth + "px");

    // 3. Função de Scroll
    let scrollInterval = setInterval(() => {
        // Se já rolamos o equivalente ao primeiro conjunto de imagens...
        if (sliderContainer.scrollLeft >= firstSetWidth) {
            // ...volte para 0 suavemente (quase invisível)
            console.log(">>> Resetando posição!");
            sliderContainer.scrollLeft -= firstSetWidth;
        } else {
            // Senão, continua andando
            sliderContainer.scrollLeft += scrollSpeed;
        }
    }, 20); // 20ms = ~50fps

    // Pausa ao passar o mouse (Debug: Desativei temporariamente para testar se roda)
    // sliderContainer.addEventListener("mouseenter", () => clearInterval(scrollInterval));
    // sliderContainer.addEventListener("mouseleave", () => { /* reativar interval */ });
});