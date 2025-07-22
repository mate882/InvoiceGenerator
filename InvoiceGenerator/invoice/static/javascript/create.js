let itemCount = 1;

function addItem() {
    itemCount++;
    const container = document.getElementById('items-container');
    const newItem = document.createElement('div');
    newItem.classList.add('item');
    newItem.innerHTML = `
        <label for="item_description_${itemCount}">Description</label><br>
        <input type="text" id="item_description_${itemCount}" name="item_description_${itemCount}"><br><br>

        <label for="item_quantity_${itemCount}">Quantity</label><br>
        <input type="number" id="item_quantity_${itemCount}" name="item_quantity_${itemCount}" min="0" step="1"><br><br>

        <label for="item_unit_price_${itemCount}">Unit Price</label><br>
        <input type="number" id="item_unit_price_${itemCount}" name="item_unit_price_${itemCount}" min="0" step="0.01"><br><br>

        <label for="item_currency_${itemCount}">Currency</label><br>
        <select id="item_currency_${itemCount}" name="item_currency_${itemCount}">
            <option value="USD" selected>USD ($)</option>
            <option value="EUR">EUR (€)</option>
            <option value="GBP">GBP (£)</option>
            <option value="TRY">TRY (₺)</option>
        </select><br><br>
    `;
    container.appendChild(newItem);
    document.getElementById('item-count').value = itemCount;

    // Attach event listeners for new inputs right away
    addListenersForItem(itemCount);
}

function removeItem() {
    if (itemCount > 1) {
        const container = document.getElementById('items-container');
        container.removeChild(container.lastElementChild);
        itemCount--;
        document.getElementById('item-count').value = itemCount;
        calculateTotals();
    }
}

function addListenersForItem(i) {
    const qtyInput = document.getElementById(`item_quantity_${i}`);
    const priceInput = document.getElementById(`item_unit_price_${i}`);
    const currencySelect = document.getElementById(`item_currency_${i}`);

    if (qtyInput) qtyInput.addEventListener('input', calculateTotals);
    if (priceInput) priceInput.addEventListener('input', calculateTotals);
    if (currencySelect) currencySelect.addEventListener('change', calculateTotals);
}

function calculateTotals() {
    let subtotal = 0;
    let currency = null;

    for (let i = 1; i <= itemCount; i++) {
        const qtyInput = document.getElementById(`item_quantity_${i}`);
        const priceInput = document.getElementById(`item_unit_price_${i}`);
        const currencySelect = document.getElementById(`item_currency_${i}`);

        if (!qtyInput || !priceInput || !currencySelect) continue;

        const qty = parseFloat(qtyInput.value) || 0;
        const price = parseFloat(priceInput.value) || 0;
        const curr = currencySelect.value;

        if (currency === null) {
            currency = curr;
        } else if (currency !== curr) {
            alert('Warning: Different currencies detected in items. Please use the same currency for all items.');
            return;
        }

        subtotal += qty * price;
    }

    const taxInput = document.getElementById('tax');
    const tax = taxInput ? parseFloat(taxInput.value) || 0 : 0;
    const totalDue = subtotal + tax;

    document.getElementById('subtotal').value = subtotal.toFixed(2);
    document.getElementById('total_due').value = totalDue.toFixed(2);
}

document.addEventListener('DOMContentLoaded', () => {
    // Add listeners for first item on page load
    addListenersForItem(1);

    // Add listener for tax input
    const taxInput = document.getElementById('tax');
    if (taxInput) taxInput.addEventListener('input', calculateTotals);

    // Add listeners for add and reset buttons
    document.getElementById('add').addEventListener('click', addItem);
    document.getElementById('reset').addEventListener('click', removeItem);

    // Calculate totals once on page load
    calculateTotals();
});
