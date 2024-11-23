document.addEventListener('DOMContentLoaded', (event) => {
    // Função para atualizar o preço total
    function updateTotalPrice(price, quantityInput, totalPriceDisplay, finalQuantityInput) {
        const quantity = parseInt(quantityInput.value)
        const total = parseFloat(price.replace(',', '.')) * quantity
        totalPriceDisplay.textContent = total.toFixed(2)
        finalQuantityInput.value = quantity  // Atualiza o valor do formulário
    }

    // Verificação e configuração do preço do produto
    const priceProduct = document.getElementById('priceProduct')
    if (priceProduct) {
        const price = priceProduct.dataset.price
        const quantityInput = document.getElementById('quantify')
        const totalPriceDisplay = document.getElementById('total-price')
        const finalQuantityInput = document.getElementById('final-quantity')
        const increaseButton = document.getElementById('increase')
        const decreaseButton = document.getElementById('decrease')

        // Botões de aumentar e diminuir a quantidade
        if (increaseButton && decreaseButton) {
            increaseButton.addEventListener('click', () => {
                quantityInput.value = parseInt(quantityInput.value) + 1
                updateTotalPrice(price, quantityInput, totalPriceDisplay, finalQuantityInput)
            })

            decreaseButton.addEventListener('click', () => {
                if (parseInt(quantityInput.value) > 1) {
                    quantityInput.value = parseInt(quantityInput.value) - 1
                    updateTotalPrice(price, quantityInput, totalPriceDisplay, finalQuantityInput)
                }
            })
        }

        // Atualiza o total inicialmente
        updateTotalPrice(price, quantityInput, totalPriceDisplay, finalQuantityInput)
    }

    // Outras funcionalidades que não dependem de priceProduct
    // (Adicione aqui qualquer outro código que você deseja executar)
    
    console.log("Script carregado e outras funcionalidades prontas para serem executadas.")
})



document.querySelectorAll('.update-cart').forEach(button => {
    button.addEventListener('click', ()=>{
        const productId = this.getAttribute('data-product-id')
        const action = this.getAttribute('data-action')
        const quantifyElement = document.getElementById(`quantify-${productId}`)
        const subtotalElement = document.getElementById(`subtotal-${productId}`)
        const totalElement = document.getElementById('total')

        fetch(`/cart/update/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', 
                'X-CSRFToken': '{{csrf_token}}',
            },
            body: JSON.stringify({action: action})
        }).then(response => {
            if (!response.ok){
                throw new Error('Erro ao atualizar o carrinho')
            }
            return response.json
        }).then(data => {
            quantifyElement.textContent = data.quantify
            subtotalElement.textContent = `R$ ${data.subtotal.toFixed(2)}`
            totalElement.textContent = `R$ ${data.total.toFixed(2)}`
        }).catch(error => {
            console.log(error)
            alert('Ocorreu um erro ao atualizar o carrinho')
        })
    })
})