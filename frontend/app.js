function setEmergency(amount) {
    document.getElementById("amount").value = amount;
  }
  
  async function requestLoan() {
    const income = document.getElementById("income").value;
    const expenses = document.getElementById("expenses").value;
    const amount = document.getElementById("amount").value;
  
    const payload = { income, expenses, amount };
  
    try {
      const res = await fetch("http://127.0.0.1:5000/predict_loan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
  
      const data = await res.json();
  
      if (data.error) {
        document.getElementById("result").innerHTML = `⚠️ ${data.error}`;
        return;
      }
  
      document.getElementById("result").innerHTML =
        `<b>Loan Status:</b> ${data.status}<br>` +
        `<b>Plan:</b> ${data.repayment}`;
  
      document.getElementById("coach").innerHTML =
        `💡 Coach says: ${data.coach}`;
    } catch (err) {
      document.getElementById("result").innerHTML = "❌ Error connecting to server.";
    }
  }
  