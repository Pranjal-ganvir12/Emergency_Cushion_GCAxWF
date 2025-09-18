function setEmergency(amount) {
    document.getElementById("amount").value = amount;
  }
  
  async function requestLoan() {
    const payload = {
      income: document.getElementById("income").value,
      expenses: document.getElementById("expenses").value,
      amount: document.getElementById("amount").value
    };
  
    try {
      const res = await fetch("/predict_loan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
  
      const data = await res.json();
      if (data.error) {
        document.getElementById("result").innerText = "⚠️ " + data.error;
        return;
      }
  
      document.getElementById("result").innerText =
        `Loan Status: ${data.status}\nPlan: ${data.plan}`;
      document.getElementById("coach").innerText =
        `💡 Coach says: ${data.coach}`;
    } catch (e) {
      document.getElementById("result").innerText = "❌ Error connecting to server.";
    }
  }
  