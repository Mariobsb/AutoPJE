const API = "http://localhost:8000";
const logEl = document.getElementById("log");

function append(line){
  const atBottom = Math.abs(logEl.scrollHeight - logEl.scrollTop - logEl.clientHeight) < 8;
  logEl.textContent += (line + "\n");
  if (atBottom) logEl.scrollTop = logEl.scrollHeight;
}

(async function connectLogs(){
  try{
    const ws = new WebSocket(API.replace("http","ws") + "/ws/logs");
    ws.onmessage = (ev)=> append(ev.data);
    ws.onopen = ()=> append("🔌 conectado ao stream de logs.");
    ws.onclose = ()=> append("⚠️ conexão de log encerrada.");
  }catch(e){ append("Erro ao conectar no log: " + e); }
})();

document.getElementById("btn-login").onclick = async ()=>{
  append("➡️ requisitando /api/login …");
  const res = await fetch(API + "/api/login", {method:"POST"});
  const data = await res.json();
  append("⏱ resposta: " + JSON.stringify(data));
};

document.getElementById("btn-clear").onclick = ()=>{
  logEl.textContent = "";
};
