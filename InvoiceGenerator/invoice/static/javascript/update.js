// update.js

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const taxInput = document.getElementById('tax');
    const totalDueInput = document.getElementById('total_due');
    const subtotalInput = form.querySelector('input[name="subtotal"]');
    const itemCountInput = form.querySelector('input[name="item_count"]');
    const addBtn = document.getElementById('add');
    const resetBtn = document.getElementById('reset');
    const itemsContainer = document.getElementById('items-container');

    let itemCount = parseInt(itemCountInput.value) || 0;

    function calculateSubtotal() {
        let subtotal = 0;

        for (let i = 1; i <= itemCount; i++) {
            const quantityField = form.querySelector(`input[name="item_quantity_${i}"]`);
            const priceField = form.querySelector(`input[name="item_unit_price_${i}"]`);

            if (!quantityField || !priceField) continue;

            const quantity = parseFloat(quantityField.value) || 0;
            const unitPrice = parseFloat(priceField.value) || 0;

            subtotal += quantity * unitPrice;
        }

        subtotalInput.value = subtotal.toFixed(2);
        return subtotal;
    }

    function calculateTotal() {
        const subtotal = calculateSubtotal();
        const tax = parseFloat(taxInput.value) || 0;
        const total = subtotal + tax;
        totalDueInput.value = total.toFixed(2);
    }

    form.addEventListener('input', (e) => {
        if (
            e.target.name.startsWith('item_quantity_') ||
            e.target.name.startsWith('item_unit_price_') ||
            e.target.name === 'tax'
        ) {
            calculateTotal();
        }
    });

    function addItem() {
        itemCount++;
        const itemDiv = document.createElement('div');
        itemDiv.classList.add('item');

        itemDiv.innerHTML = `
            <label>Description</label><br>
            <input type="text" name="item_description_${itemCount}"><br><br>

            <label>Quantity</label><br>
            <input type="number" name="item_quantity_${itemCount}" min="0" step="1"><br><br>

            <label>Unit Price</label><br>
            <input type="number" name="item_unit_price_${itemCount}" min="0" step="0.01"><br><br>

            <label>Currency</label><br>
            <select name="item_currency_${itemCount}">
                <option value="USD" selected>USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
                <option value="TRY">TRY (₺)</option>
            </select><br><br>
        `;

        itemsContainer.appendChild(itemDiv);

        itemCountInput.value = itemCount;

        calculateTotal();
    }

    function removeItem() {
        if (itemCount > 1) {
            itemsContainer.removeChild(itemsContainer.lastElementChild);
            itemCount--;
            itemCountInput.value = itemCount;

            calculateTotal();
        }
    }

    addBtn.addEventListener('click', addItem);
    resetBtn.addEventListener('click', removeItem);

    // Initial calculation
    calculateTotal();
});
