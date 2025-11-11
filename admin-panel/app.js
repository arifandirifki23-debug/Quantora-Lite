let token = null;
const apiBase = location.origin;
document.getElementById("btnLogin").addEventListener("click", async () => {
  const u = document.getElementById("username").value;
  const p = document.getElementById("password").value;
  const r = await fetch(apiBase + "/admin/login", {method:"POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({username: u, password: p})});
  const j = await r.json();
  document.getElementById("loginRes").innerText = JSON.stringify(j, null,2);
  if (j.ok){
    token = j.token;
    document.getElementById("loginBox").style.display = "none";
    document.getElementById("panel").style.display = "block";
    loadUsers();
  }
});
async function loadUsers(){
  const r = await fetch(apiBase + "/admin/users", {headers: {"Authorization": "Bearer " + token}});
  const j = await r.json();
  document.getElementById("users").innerText = JSON.stringify(j, null, 2);
}
document.getElementById("grantBtn").addEventListener("click", async () => {
  const uid = document.getElementById("g_user").value;
  const days = document.getElementById("g_days").value;
  if (!uid) { alert("user_id required"); return; }
  const r = await fetch(apiBase + "/admin/grant", {method:"POST", headers: {"Content-Type":"application/json","Authorization":"Bearer "+token}, body: JSON.stringify({user_id:uid, days:days})});
  const j = await r.json();
  document.getElementById("grantRes").innerText = JSON.stringify(j, null,2);
  loadUsers();
});
document.getElementById("loadLogs").addEventListener("click", async () => {
  const r = await fetch(apiBase + "/admin/logs", {headers: {"Authorization": "Bearer " + token}});
  const j = await r.json();
  document.getElementById("logs").innerText = JSON.stringify(j, null,2);
});
document.getElementById("btnLogout").addEventListener("click", () => {
  token = null;
  document.getElementById("loginBox").style.display = "block";
  document.getElementById("panel").style.display = "none";
});
