// Espera que o conteúdo do documento seja completamente carregado
document.addEventListener('DOMContentLoaded', (event) => {
    // Função para atualizar o preço total baseado no preço unitário e na quantidade
    function updateTotalPrice(price, quantityInput, totalPriceDisplay, finalQuantityInput) {
        const quantity = parseInt(quantityInput.value) // Obtém a quantidade informada pelo usuário
        const total = parseFloat(price.replace(',', '.')) * quantity // Calcula o preço total (conversão de vírgula para ponto)
        totalPriceDisplay.textContent = total.toFixed(2) // Exibe o valor total formatado no display
        finalQuantityInput.value = quantity  // Atualiza o valor da quantidade no formulário para ser enviado
    }

    // Verificação e configuração do preço do produto
    const priceProduct = document.getElementById('priceProduct') // Obtém o elemento que contém o preço do produto
    if (priceProduct) { // Se o elemento existe, configura os valores necessários
        const price = priceProduct.dataset.price // Obtém o preço do produto do atributo 'data-price'
        const quantityInput = document.getElementById('quantity') // Obtém o campo de entrada da quantidade
        const totalPriceDisplay = document.getElementById('total-price') // Obtém o display do preço total
        const finalQuantityInput = document.getElementById('final-quantity') // Obtém o campo oculto da quantidade final
        const increaseButton = document.getElementById('increase') // Obtém o botão para aumentar a quantidade
        const decreaseButton = document.getElementById('decrease') // Obtém o botão para diminuir a quantidade

        // Verifica se os botões de aumentar e diminuir existem e adiciona eventos a eles
        if (increaseButton && decreaseButton) {
            increaseButton.addEventListener('click', () => {
                quantityInput.value = parseInt(quantityInput.value) + 1 // Aumenta a quantidade em 1
                updateTotalPrice(price, quantityInput, totalPriceDisplay, finalQuantityInput) // Atualiza o total
            })

            decreaseButton.addEventListener('click', () => {
                if (parseInt(quantityInput.value) > 1) { // Evita que a quantidade seja menor que 1
                    quantityInput.value = parseInt(quantityInput.value) - 1 // Diminui a quantidade em 1
                    updateTotalPrice(price, quantityInput, totalPriceDisplay, finalQuantityInput) // Atualiza o total
                }
            })
        }

        // Atualiza o total logo que a página é carregada
        updateTotalPrice(price, quantityInput, totalPriceDisplay, finalQuantityInput)
    }
})

// Seleciona todos os botões para atualizar o carrinho
document.querySelectorAll('.update-cart').forEach(button => {
    button.addEventListener('click', function () { // Use uma função tradicional para acessar `this`
        const productId = this.getAttribute('data-product-id') // Obtém o ID do produto
        const action = this.getAttribute('data-action') // Obtém a ação (aumentar ou diminuir)
        const quantityElement = document.getElementById(`quantity-${productId}`) // Obtém o elemento da quantidade
        const subtotalElement = document.getElementById(`subtotal-${productId}`) // Obtém o elemento do subtotal
        const totalElement = document.getElementById('total') // Obtém o elemento do total geral
    
        // Faz uma requisição para o servidor para atualizar o carrinho
        fetch(`/update_item/${productId}/`, {
            method: 'POST', // Define o método como POST
            headers: {
                'Content-Type': 'application/json', // Especifica que o corpo da requisição é JSON
                'X-CSRFToken': csrfToken, // Certifica-se de enviar o CSRF token (necessário para segurança em Django)
            },
            body: JSON.stringify({ action: action }) // Envia a ação como parte do corpo da requisição
        })
            .then(response => {
                if (!response.ok) { // Se a resposta não for bem-sucedida, lança um erro
                    throw new Error('Erro ao atualizar o carrinho')
                }
                return response.json() // Retorna a resposta como JSON
            })
            .then(data => {
                // Atualiza a quantidade, subtotal e total na página com os dados retornados
                quantityElement.textContent = data.quantity
                subtotalElement.textContent = `R$ ${data.subtotal.toFixed(2)}` // Formata o subtotal com 2 casas decimais
                totalElement.textContent = `R$ ${data.total.toFixed(2)}` // Formata o total com 2 casas decimais
            })
            .catch(error => {
                console.error(error); // Exibe o erro no console
                alert('Ocorreu um erro ao atualizar o carrinho.') // Exibe um alerta caso haja erro
            })
    })
})


function addItemToCart(){
    document.getElementById('addToCartForm').addEventListener('submit', async function (event) {
        event.preventDefault() // Impede o envio padrão do formulário

        const form = event.target
        const formData = new FormData(form)

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                },
            })

            if (response.ok) {
                // Exibir o modal
                const modal = new bootstrap.Modal(document.getElementById('addToCartModal'))
                modal.show()
            } else {
                alert('Erro ao adicionar ao carrinho. Tente novamente.')
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Ocorreu um erro. Tente novamente.')
        }
    })
}

function displayMessage(msg, classMsg){
    const divMsg = document.createElement('div')
    divMsg.textContent = msg
    divMsg.className = `alert alert-success ${classMsg}`
    document.body.appendChild(divMsg)

    setTimeout(()=>{
        divMsg.remove()
    }, 3000)
}

const btns = [...document.querySelectorAll('.remove-btn')]

btns.forEach(btn => {
    btn.addEventListener('click', (evt)=>{
        evt.preventDefault()

        const modal = new bootstrap.Modal(document.getElementById('removeToCartModal'))
        modal.show()

        const btnTarget = evt.target
        const productId = btnTarget.getAttribute('productId')
        
        confirmRemove = document.getElementById('confirmRemove')
        confirmRemove.addEventListener('click', async ()=>{
            try {
                const response = await fetch(`/remove_item/${productId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                })

                if (response.ok){
                    location.reload()
                } else {
                    alert('Erro ao remover item.')
                }
            } catch (error) {
                console.error('Error: ', error)
                alert("Ocorreu algum erro ao remover item!")
            }
        })
        noremove = document.getElementById('noRemove')
            noremove.addEventListener('click', ()=>{
                modal.hide()
            })
    })
})


const finalizeOrder = document.getElementById('finalizeOrder')
finalizeOrder.addEventListener('click', (evt)=>{
    evt.preventDefault()

    const btn = evt.target
    const confirmAuthentication = btn.getAttribute('confirmAuthentication')

    if (confirmAuthentication){
        let modal = new bootstrap.Modal(document.getElementById('loginUser'))
        modal.show()
    } else {
        console.log('ainda não')
    }
    
    
})