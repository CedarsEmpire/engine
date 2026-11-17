<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
  <title>Engine Five Dashboard</title>
  <style>
    body { font-family: sans-serif; margin: 20px; }
    .region { margin: 10px 0; }
  </style>
</head>
<body>
  <h1>Engine Five Dashboard</h1>
  
  <div>
    <h2>AI Workers</h2>
    <p>Target: €2500 / 24h</p>
    <p>Status: <span id="ai-status">Idle</span></p>
  </div>
  
  <div>
    <h2>Human Tasks</h2>
    <p>Reward: €15 per task</p>
    <p>Pending: <span id="human-pending">0</span></p>
  </div>
  
  <div>
    <h2>Regions</h2>
    <div class="region">Region 1: <button id="r1-btn">Enable</button></div>
    <div class="region">Region 2: <button id="r2-btn">Enable</button></div>
    <div class="region">Region 3: <button id="r3-btn">Enable</button></div>
    <div class="region">Region 4: <button id="r4-btn">Enable</button></div>
    <div class="region">Region 5: <button id="r5-btn">Enable</button></div>
  </div>
  
  <div>
    <h2>Payouts (Crypto only)</h2>
    <p>Status: <span id="payout-status">No pending payouts</span></p>
  </div>

  <script>
    // Basic JS to connect to your engine/
    const regions = [1,2,3,4,5];
    regions.forEach(r => {
      document.getElementById(`r${r}-btn`).onclick = () => {
        // Call engine/central_hub.py to toggle region
        fetch(`/api/toggle-region/${r}`)
          .then(res => res.json())
          .then(data => alert(`Region ${r} ${data.enabled ? 'Enabled' : 'Disabled'}`));
      };
    });
  </script>
</body>
</html>
