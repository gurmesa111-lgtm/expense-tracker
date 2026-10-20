const categories = {1: "Food", 2: "Transport", 3: "Housing",
    4: "Utilities", 5: "Shopping", 6: "Entertainment",
    7: "Health", 8: "Education", 9: "Others"};

let expenses = [{id: 1, amount: 300, categoryId: 2, date: "2026-10-16", description: "Travel"},
    {id: 2, amount: 200, categoryId: 1, date: "2026-08-18", description: "Lunch"},
    {id: 3, amount: 2800, categoryId: 3, date: "2026-10-01", description: "Rent"},
    {id: 4, amount: 800, categoryId: 1, date: "2026-06-23", description: "Groceries"},
    {id: 5, amount: 700, categoryId: 5, date: "2026-05-09", description: "Clothing"}
];

const body = document.getElementById("expense-body");

function renderExpenses(){
    body.innerHTML = "";

    for(const expense of expenses){
        const row = document.createElement("tr");

        const dateCell = document.createElement("td");
        dateCell.textContent = expense.date;
        row.appendChild(dateCell);

        const categoryCell = document.createElement("td");
        categoryCell.textContent = categories[expense.categoryId];
        row.appendChild(categoryCell);

        const descriptionCell = document.createElement("td");
        descriptionCell.textContent = expense.description;
        row.appendChild(descriptionCell);

        const amountCell = document.createElement("td");
        amountCell.textContent = expense.amount.toFixed(2);
        amountCell.className = "amount";
        row.appendChild(amountCell);

        const actionCell = document.createElement("td");
        const button = document.createElement("button");
        button.className = "btn-delete";
        button.type = "button";
        button.textContent = "Delete";

        button.addEventListener("click", () => {
            expenses = expenses.filter((item) => item.id !== expense.id);
            renderAll();
        });

        actionCell.appendChild(button);
        row.appendChild(actionCell);

        body.appendChild(row);
    }
}

function renderDashboard(){
    let totalAmount = 0;
    let monthTotal = 0;
    const now = new Date();
    
    for(const expense of expenses){
        totalAmount += expense.amount;
    }
    const totalCard = document.getElementById("total-spending");
    totalCard.textContent = totalAmount.toFixed(2);

    const yearMonth = `${now.getFullYear()}-${String((now.getMonth() + 1)).padStart(2, "0")}`;
    const monthExpenses = expenses.filter((expense) => expense.date.startsWith(yearMonth));
    for(const monthExpense of monthExpenses){
        monthTotal += monthExpense.amount;
    }
    const monthCard = document.getElementById("month-spending");
    monthCard.textContent = monthTotal.toFixed(2);

    const monthLabel = document.getElementById("month-label");
    monthLabel.textContent = `${now.toLocaleString("en-US", { month: "long" })} ${now.getFullYear()} spending`;

    const count = expenses.length;
    const recordCard = document.getElementById("expense-count");
    recordCard.textContent = count;
    
}

const categorySpend = document.getElementById("category-list");
function renderCategoryTotals(){
    categorySpend.innerHTML = "";
    const totals = {};
    
    for(const expense of expenses){
        const name = categories[expense.categoryId];
        totals[name] = (totals[name] || 0) + expense.amount;
    }

    for(const categoryName in totals){
        const spending = document.createElement("li");
        spending.textContent = `${categoryName}: ${totals[categoryName].toFixed(2)}`;
        categorySpend.appendChild(spending);
    }
}

const biggestList = document.getElementById("biggest-list"); 
function renderBiggestExpenses(){
    biggestList.innerHTML = "";

    const sorted = [...expenses];
    sorted.sort((a, b) => b.amount - a.amount);
    const topThree = sorted.slice(0, 3);

    for(const expense of topThree){
        const item = document.createElement("li");              
        item.textContent = `${expense.description}: ${expense.amount.toFixed(2)}`;
        biggestList.appendChild(item);
    }
}

const form = document.getElementById("expense-form");
form.addEventListener("submit", (event) => {
    event.preventDefault();
    const newExpense = {};

    const id = Date.now();
    newExpense.id = id;

    const amountInput = document.getElementById("amount");
    newExpense.amount = Number(amountInput.value);

    const categoryInput = document.getElementById("category");
    newExpense.categoryId = Number(categoryInput.value);

    const dateInput = document.getElementById("date");
    newExpense.date = dateInput.value;

    const descriptionInput = document.getElementById("description");
    newExpense.description = descriptionInput.value || categories[newExpense.categoryId];

    expenses.push(newExpense);
    form.reset();
    renderAll();
});

function renderAll(){
    renderExpenses();
    renderDashboard();
    renderCategoryTotals();
    renderBiggestExpenses();
}

renderAll();
