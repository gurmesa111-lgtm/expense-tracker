const categories = {1: "Food", 2: "Transport", 3: "Housing",
    4: "Utilities", 5: "Shopping", 6: "Entertainment",
    7: "Health", 8: "Education", 9: "Others"};

const expenses = [{id: 1, amount: 300, categoryId: 2, date: "2026-10-16", description: "Travel"},
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
        actionCell.appendChild(button);
        row.appendChild(actionCell);

        body.appendChild(row);
    }
}

renderExpenses();
